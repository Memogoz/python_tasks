import uuid

# --- Data Structures ---
# Pizza:
# {
#   "pizza_id": "uuid",
#   "name": "string",
#   "description": "string",
#   "price": float
# }

# Order:
# {
#   "order_id": "uuid",
#   "items": [
#       {"pizza_id": "uuid", "quantity": int}
#   ],
#   "status": "pending" | "preparing" | "ready_for_delivery" | "delivered" | "cancelled",
#   "timestamp": "datetime_string"
# }

# In a real application, you'd have User data, but for this scope,
# we're focusing on customer/admin interactions without full user management.

# Admin Token (Hardcoded for simplicity, securely stored in a real app)
ADMIN_TOKEN = "supersecretadmintoken123"

# --- In-Memory Databases ---
menu = {
    "pizza1": {"pizza_id": "pizza1", "name": "Margherita", "description": "Classic cheese and tomato", "price": 10.00},
    "pizza2": {"pizza_id": "pizza2", "name": "Pepperoni", "description": "Spicy pepperoni and mozzarella", "price": 12.50},
    "pizza3": {"pizza_id": "pizza3", "name": "Veggie Delight", "description": "Mushrooms, onions, peppers, olives", "price": 11.00},
}

orders = {} # Stores order_id -> order_details

def generate_uuid():
    return str(uuid.uuid4())[:6]

def get_pizza_by_id(pizza_id):
    return menu.get(pizza_id)

def add_pizza_to_menu(name, description, price):
    pizza_id = generate_uuid()
    menu[pizza_id] = {
        "pizza_id": pizza_id,
        "name": name,
        "description": description,
        "price": price
    }
    return menu[pizza_id]

def delete_pizza_from_menu(pizza_id):
    if pizza_id in menu:
        del menu[pizza_id]
        return True
    return False

def create_new_order(items):
    order_id = generate_uuid()
    # Basic validation for pizza_ids
    for item in items:
        if not get_pizza_by_id(item['pizza_id']):
            return None # Invalid pizza ID
    orders[order_id] = {
        "order_id": order_id,
        "items": items,
        "status": "pending",
        "timestamp": "2025-05-20T18:30:00Z" # Placeholder, use actual datetime in app.py
    }
    return orders[order_id]

def get_order_by_id(order_id):
    return orders.get(order_id)

def update_order_status(order_id, new_status):
    if order_id in orders:
        orders[order_id]['status'] = new_status
        return True
    return False

def cancel_order(order_id):
    if order_id in orders:
        del orders[order_id]
        return True
    return False