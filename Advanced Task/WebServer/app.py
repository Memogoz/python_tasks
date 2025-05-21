from flask import Flask, jsonify, request
from datetime import datetime
from data import (
    menu, orders, generate_uuid, get_pizza_by_id, add_pizza_to_menu,
    delete_pizza_from_menu, create_new_order, get_order_by_id, cancel_order
)
from auth import admin_required

app = Flask(__name__)

# --- Helper Function for JSON Response ---
def success_response(data, status_code=200):
    return jsonify({"success": True, "data": data}), status_code

def error_response(message, status_code=400):
    return jsonify({"success": False, "error": message}), status_code

# --- Customer API Endpoints ---

@app.route('/menu', methods=['GET'])
def list_menu():
    """
    List the available pizzas on the menu.
    GET /menu
    """
    return success_response(list(menu.values()))

@app.route('/order', methods=['POST'])
def create_order():
    """
    Create a new order.
    POST /order
    Request Body:
    {
        "items": [
            {"pizza_id": "pizza1", "quantity": 1},
            {"pizza_id": "pizza2", "quantity": 2}
        ]
    }
    """
    data = request.get_json()
    if not data or 'items' not in data:
        return error_response("Missing 'items' in request body", 400)

    items = data['items']
    if not isinstance(items, list) or not all(isinstance(item, dict) and 'pizza_id' in item and 'quantity' in item for item in items):
        return error_response("Invalid 'items' format. Expected a list of objects with 'pizza_id' and 'quantity'.", 400)

    order_items_with_details = []
    for item in items:
        pizza = get_pizza_by_id(item['pizza_id'])
        if not pizza:
            return error_response(f"Pizza with ID '{item['pizza_id']}' not found.", 404)
        if not isinstance(item['quantity'], int) or item['quantity'] <= 0:
            return error_response(f"Invalid quantity for pizza ID '{item['pizza_id']}'. Quantity must be a positive integer.", 400)
        order_items_with_details.append({
            "pizza_id": pizza['pizza_id'],
            "name": pizza['name'],
            "price": pizza['price'],
            "quantity": item['quantity']
        })

    order_id = generate_uuid()
    orders[order_id] = {
        "order_id": order_id,
        "items": order_items_with_details,
        "status": "pending",
        "timestamp": datetime.now().isoformat()
    }
    return success_response(orders[order_id], 201)

@app.route('/order/<order_id>', methods=['GET'])
def check_order_status(order_id):
    """
    Check the status of an order.
    GET /order/{order_id}
    """
    order = get_order_by_id(order_id)
    if not order:
        return error_response(f"Order with ID '{order_id}' not found.", 404)
    return success_response(order)

@app.route('/order/<order_id>', methods=['DELETE'])
def cancel_customer_order(order_id):
    """
    Cancel an order if its status is not 'ready_for_delivery' or 'delivered'.
    DELETE /order/{order_id}
    """
    order = get_order_by_id(order_id)
    if not order:
        return error_response(f"Order with ID '{order_id}' not found.", 404)

    if order['status'] in ["ready_for_delivery", "delivered"]:
        return error_response(f"Order cannot be cancelled. Status is '{order['status']}'.", 403)

    if cancel_order(order_id):
        return success_response({"message": f"Order with ID '{order_id}' cancelled successfully."})
    return error_response("Failed to cancel order.", 500) # Should not happen with current logic


# --- Admin API Endpoints ---

@app.route('/admin/menu', methods=['POST'])
@admin_required
def add_pizza():
    """
    Add a new pizza to the menu (Admin only).
    POST /admin/menu
    Request Body:
    {
        "name": "Pizza Name",
        "description": "Pizza Description",
        "price": 15.00
    }
    Requires X-Admin-Token header.
    """
    data = request.get_json()
    if not data or not all(k in data for k in ['name', 'description', 'price']):
        return error_response("Missing required fields: 'name', 'description', 'price'", 400)

    name = data['name']
    description = data['description']
    price = data['price']

    if not isinstance(name, str) or not name.strip():
        return error_response("Invalid 'name'. Must be a non-empty string.", 400)
    if not isinstance(description, str) or not description.strip():
        return error_response("Invalid 'description'. Must be a non-empty string.", 400)
    if not isinstance(price, (int, float)) or price <= 0:
        return error_response("Invalid 'price'. Must be a positive number.", 400)

    new_pizza = add_pizza_to_menu(name, description, price)
    return success_response(new_pizza, 201)

@app.route('/admin/menu/<pizza_id>', methods=['DELETE'])
@admin_required
def delete_pizza(pizza_id):
    """
    Delete a pizza from the menu (Admin only).
    DELETE /admin/menu/{pizza_id}
    Requires X-Admin-Token header.
    """
    if delete_pizza_from_menu(pizza_id):
        return success_response({"message": f"Pizza with ID '{pizza_id}' deleted successfully."})
    return error_response(f"Pizza with ID '{pizza_id}' not found.", 404)

@app.route('/admin/order/<order_id>', methods=['DELETE'])
@admin_required
def cancel_admin_order(order_id):
    """
    Cancel an order regardless of its status (Admin only).
    DELETE /admin/order/{order_id}
    Requires X-Admin-Token header.
    """
    order = get_order_by_id(order_id)
    if not order:
        return error_response(f"Order with ID '{order_id}' not found.", 404)

    if cancel_order(order_id):
        return success_response({"message": f"Order with ID '{order_id}' cancelled by admin."})
    return error_response("Failed to cancel order.", 500) # Should not happen with current logic

@app.route('/admin/orders', methods=['GET'])
@admin_required
def list_all_orders():
    """
    List all orders (Admin only).
    GET /admin/orders
    Requires X-Admin-Token header.
    """
    return success_response(list(orders.values()))

@app.route('/admin/order/<order_id>/status', methods=['PUT'])
@admin_required
def update_order_status(order_id):
    """
    Update the status of an order (Admin only).
    PUT /admin/order/{order_id}/status
    Request Body:
    {
        "status": "preparing"
    }
    Requires X-Admin-Token header.
    """
    data = request.get_json()
    if not data or 'status' not in data:
        return error_response("Missing 'status' in request body.", 400)

    new_status = data['status']
    valid_statuses = ["pending", "preparing", "ready_for_delivery", "delivered", "cancelled"]
    if new_status not in valid_statuses:
        return error_response(f"Invalid status. Allowed statuses: {', '.join(valid_statuses)}", 400)

    order = get_order_by_id(order_id)
    if not order:
        return error_response(f"Order with ID '{order_id}' not found.", 404)

    order['status'] = new_status
    return success_response(order)


if __name__ == '__main__':
    app.run(debug=True, port=5000)