import uuid
from typing import List, Dict

# In-memory storage for the dry run.
# In a real app, this would be a database like PostgreSQL or MongoDB.

orders_db = []
customer_profiles = {
    "default_user": {
        "region": "India",
        "normal_coins": 0.0,
        "blockchain_coins": 0.0
    }
}

def get_customer_profile(identifier: str):
    if not identifier:
        identifier = "default_user"
    if identifier not in customer_profiles:
        customer_profiles[identifier] = {
            "region": "India",
            "normal_coins": 0.0,
            "blockchain_coins": 0.0
        }
    return customer_profiles[identifier]

def update_customer_region(identifier: str, region: str):
    profile = get_customer_profile(identifier)
    profile["region"] = region
    return profile

def add_coins(identifier: str, order_total_inr: float):
    # Base issuance: 1 coin per 100 INR spent
    coins_earned = round(order_total_inr / 100.0, 2)
    profile = get_customer_profile(identifier)
    
    blockchain_regions = ["El Salvador", "UAE", "USA"]
    
    if profile["region"] in blockchain_regions:
        profile["blockchain_coins"] += coins_earned
    else:
        profile["normal_coins"] += coins_earned
        
    return profile


def add_order(customer_message: str, parsed_items: List[Dict], source: str = "web", customer_identifier: str = None):
    order_id = str(uuid.uuid4())[:8]
    order = {
        "id": order_id,
        "customer_message": customer_message,
        "items": parsed_items,
        "status": "pending", # pending, confirmed, completed
        "payment_status": "unpaid",
        "pos_pushed": False,
        "pos_order_id": None,
        "source": source,
        "customer_identifier": customer_identifier or "default_user"
    }
    orders_db.append(order)
    return order

def get_all_orders():
    # Return reversed so newest are first
    return orders_db[::-1]

def update_order_status(order_id: str, status: str):
    for order in orders_db:
        if order["id"] == order_id:
            order["status"] = status
            
            # If completed, add loyalty coins
            if status == "completed" and order["payment_status"] != "paid":
                order_total = sum(item["price"] * item["quantity"] for item in order["items"])
                add_coins(order["customer_identifier"], order_total)
                order["payment_status"] = "paid"
                
            return order
    return None
