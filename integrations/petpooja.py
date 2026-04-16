from .base import BasePOSAdapter
from typing import Dict, Any
import datetime
import uuid

class PetPoojaAdapter(BasePOSAdapter):
    """
    Mock adapter for PetPooja POS integration.
    This demonstrates formatting the data into PetPooja's 'Save Order' JSON schema
    and mocking the API request.
    """
    
    def __init__(self):
        # In a real app, these would come from env vars or DB configs
        self.app_key = "mock_petpooja_app_key"
        self.app_secret = "mock_petpooja_app_secret"
        self.restaurant_id = "test_cafe_durga_001"
    
    def push_order(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert Borix internal order format to PetPooja's 'SaveOrder' schema.
        """
        # 1. Map items to PetPooja schema
        petpooja_items = []
        for item in order_data.get('items', []):
            petpooja_items.append({
                "itemid": f"item_{item['name'].lower().replace(' ', '_')}",
                "itemname": item["name"],
                "quantity": str(item["quantity"]),
                "price": str(item["price"]),
                "tax": "0" # Mock tax
            })
            
        # mock total
        subtotal = sum([item["price"] * item["quantity"] for item in order_data.get('items', [])])

        # 2. Build the exact PetPooja structure
        payload = {
            "orderinfo": {
                "OrderInfo": {
                    "Restaurant": {
                        "details": {
                            "res_name": "Cafe Durga",
                            "address": "Mock Address",
                            "contact_information": "9999999999",
                            "restID": self.restaurant_id
                        }
                    },
                    "Customer": {
                        "details": {
                            "name": "Customer X",
                            "phone": "9999999999"
                        }
                    },
                    "Order": {
                        "details": {
                            "orderID": str(uuid.uuid4())[:10], # Petpooja expects a unique ID
                            "borix_id": order_data['id'],
                            "order_status": "New",
                            "total": str(subtotal),
                            "items": petpooja_items,
                            "created_on": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                    }
                }
            }
        }
        
        # 3. MOCK SENDING REQUEST
        print(f"[PetPoojaAdapter] Pushing order {order_data['id']} to PetPooja...")
        print(f"[PetPoojaAdapter] Payload schema constructed successfully for {len(petpooja_items)} items.")
        
        # Pretend we got a successful 200 OK from Petpooja
        return {
            "success": True,
            "message": "Order successfully pushed to PetPooja DB",
            "pos_order_id": payload["orderinfo"]["OrderInfo"]["Order"]["details"]["orderID"]
        }
