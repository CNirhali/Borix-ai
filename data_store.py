import uuid
from typing import List, Dict

# In-memory storage for the dry run.
# In a real app, this would be a database like PostgreSQL or MongoDB.

orders_db = []

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
        "customer_identifier": customer_identifier
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
            return order
    return None
