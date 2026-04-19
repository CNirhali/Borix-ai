from fastapi import FastAPI, Request, Form, Response
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os

from nlp_engine import extract_intent
from data_store import add_order, get_all_orders, update_order_status, get_customer_profile, update_customer_region
from integrations import get_pos_adapter

app = FastAPI(title="Borix Order MVP")

# Allow CORS for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Endpoints
@app.post("/api/chat")
async def handle_chat(request: Request):
    data = await request.json()
    message = data.get("message", "")
    
    # Process message using our mock NLP engine
    result = extract_intent(message)
    
    # If we successfully extracted items, create an order
    if result["success"] and len(result["items"]) > 0:
        add_order(customer_message=message, parsed_items=result["items"])
        
    return {
        "reply": result["response"],
        "success": result["success"]
    }

@app.get("/api/orders")
async def fetch_orders():
    orders = get_all_orders()
    return {"orders": orders}

@app.get("/api/customer/{identifier}")
async def get_customer(identifier: str):
    profile = get_customer_profile(identifier)
    # Calculate INR value locally for the frontend
    inr_value = (profile["normal_coins"] * 0.5) + (profile["blockchain_coins"] * 3.0)
    
    return {
        "profile": profile,
        "inr_value": round(inr_value, 2)
    }

@app.post("/api/customer/{identifier}/set_region")
async def set_customer_region(identifier: str, request: Request):
    data = await request.json()
    new_region = data.get("region")
    profile = update_customer_region(identifier, new_region)
    return {"success": True, "profile": profile}

@app.post("/api/orders/{order_id}/status")
async def update_status(order_id: str, request: Request):
    data = await request.json()
    new_status = data.get("status")
    order = update_order_status(order_id, new_status)
    if order:
        return {"success": True, "order": order}
    return {"success": False, "error": "Order not found"}

@app.post("/api/orders/{order_id}/push_pos")
async def push_order_to_pos(order_id: str, request: Request):
    # Retrieve the order
    orders = get_all_orders()
    target_order = next((o for o in orders if o["id"] == order_id), None)
    
    if not target_order:
        return {"success": False, "error": "Order not found"}
        
    data = await request.json()
    pos_name = data.get("pos_name", "petpooja")
    adapter = get_pos_adapter(pos_name)
    
    if not adapter:
        return {"success": False, "error": f"POS adapter '{pos_name}' not found."}
        
    try:
        # Push the order via chosen adapter
        response = adapter.push_order(target_order)
        if response.get("success"):
            # Update local datastore
            target_order["pos_pushed"] = True
            target_order["pos_order_id"] = response.get("pos_order_id")
            return {"success": True, "pos_response": response}
        else:
            return {"success": False, "error": "Failed to push order to POS."}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/api/webhooks/whatsapp")
async def whatsapp_webhook(Body: str = Form(...), From: str = Form(...)):
    # Run NLP extraction
    result = extract_intent(Body)
    if result["success"] and len(result["items"]) > 0:
        add_order(customer_message=Body, parsed_items=result["items"], source="whatsapp", customer_identifier=From)
        reply = result["response"]
    else:
        reply = result["response"]
    
    # Return TwiML response
    twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{reply}</Message>
</Response>"""
    return Response(content=twiml, media_type="application/xml")

@app.post("/api/webhooks/telegram")
async def telegram_webhook(request: Request):
    data = await request.json()
    message = data.get("message", {})
    text = message.get("text", "")
    chat_id = message.get("chat", {}).get("id", "")
    
    if not text:
        return {"ok": True}
        
    result = extract_intent(text)
    if result["success"] and len(result["items"]) > 0:
        add_order(customer_message=text, parsed_items=result["items"], source="telegram", customer_identifier=str(chat_id))
        reply = result["response"]
    else:
        reply = result["response"]
        
    return {
        "method": "sendMessage",
        "chat_id": chat_id,
        "text": reply
    }

# Mount static files at the root
# Ensure the static directory exists
os.makedirs("static", exist_ok=True)
app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
