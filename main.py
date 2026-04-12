from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os

from nlp_engine import extract_intent
from data_store import add_order, get_all_orders, update_order_status

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

@app.post("/api/orders/{order_id}/status")
async def update_status(order_id: str, request: Request):
    data = await request.json()
    new_status = data.get("status")
    order = update_order_status(order_id, new_status)
    if order:
        return {"success": True, "order": order}
    return {"success": False, "error": "Order not found"}

# Mount static files at the root
# Ensure the static directory exists
os.makedirs("static", exist_ok=True)
app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
