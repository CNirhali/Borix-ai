import re

# This is a mock AI engine for the "dry run" demo.
# In production, this would pass the `message` to CrewAI or Gemini with a structured schema prompt.

def extract_intent(message: str):
    message_lower = message.lower()
    
    items_found = []
    
    # Very basic regex rules for demo purposes (e.g., "2 cold coffee", "1 sandwich")
    
    # Find cold coffee mentions
    cc_match = re.search(r'(\d+)\s*(cold coffee|coffee)', message_lower)
    if cc_match:
        items_found.append({
            "name": "Cold Coffee",
            "quantity": int(cc_match.group(1)),
            "price": 120
        })
    elif "cold coffee" in message_lower:
        items_found.append({
            "name": "Cold Coffee",
            "quantity": 1,
            "price": 120
        })

    # Find sandwich mentions
    sw_match = re.search(r'(\d+)\s*(sandwich|sandwiches)', message_lower)
    if sw_match:
        items_found.append({
            "name": "Sandwich",
            "quantity": int(sw_match.group(1)),
            "price": 80
        })
    elif "sandwich" in message_lower:
         items_found.append({
            "name": "Sandwich",
            "quantity": 1,
            "price": 80
        })

    # Generate a confirming response
    if items_found:
        total_items = sum([item["quantity"] for item in items_found])
        summary = ", ".join([f"{item['quantity']} {item['name']}" for item in items_found])
        response_text = f"Got it! That's {summary}. Confirming your order..."
        return {
            "success": True,
            "items": items_found,
            "response": response_text
        }
    else:
        return {
            "success": False,
            "items": [],
            "response": "I didn't quite catch what you'd like to order. We have Cold Coffee and Sandwiches!"
        }
