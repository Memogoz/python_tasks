#!/usr/bin/env python3 

import subprocess
import argparse
import sys

import argparse
import requests
import json

# --- Configuration ---
BASE_URL = "http://127.0.0.1:5000" # Ensure this matches your Flask server's address and port

# --- Helper Functions for API Calls ---

def _handle_response(response):
    """Handles API responses, printing success or error messages."""
    try:
        data = response.json()
    except json.JSONDecodeError:
        print(f"Error: Server returned non-JSON response. Status: {response.status_code}, Content: {response.text}")
        return

    if response.status_code >= 200 and response.status_code < 300:
        if data.get('success'):
            print("Success:")
            print(json.dumps(data.get('data'), indent=2))
        else:
            print(f"Error: {data.get('error', 'Unknown error')}")
    else:
        print(f"API Error (Status: {response.status_code}): {data.get('error', 'Unknown error')}")

def list_menu(args):
    """Fetches and displays the pizza menu."""
    print("Fetching menu...")
    try:
        response = requests.get(f"{BASE_URL}/menu")
        _handle_response(response)
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server. Is the Flask server running?")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def create_order(items_str):
    """
    Creates a new order.
    items_str format: "pizza_id:quantity,pizza_id:quantity"
    Example: "pizza1:1,pizza3:2"
    """
    print("Creating order...")
    items = []
    try:
        for item_pair in items_str.split(','):
            pizza_id, quantity_str = item_pair.split(':')
            items.append({"pizza_id": pizza_id.strip(), "quantity": int(quantity_str.strip())})
    except ValueError:
        print("Error: Invalid items format. Use 'pizza_id:quantity,pizza_id:quantity'.")
        return

    payload = {"items": items}
    try:
        response = requests.post(f"{BASE_URL}/order", json=payload)
        _handle_response(response)
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server. Is the Flask server running?")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def check_order_status(order_id):
    """Checks the status of a specific order."""
    print(f"Checking status for order ID: {order_id}...")
    try:
        response = requests.get(f"{BASE_URL}/order/{order_id}")
        _handle_response(response)
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server. Is the Flask server running?")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def cancel_customer_order(order_id):
    """Cancels a customer order if its status allows."""
    print(f"Attempting to cancel customer order ID: {order_id}...")
    try:
        response = requests.delete(f"{BASE_URL}/order/{order_id}")
        _handle_response(response)
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server. Is the Flask server running?")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def add_pizza(name, description, price, admin_token):
    """Adds a new pizza to the menu (admin only)."""
    print(f"Adding pizza '{name}' (admin action)...")
    headers = {"X-Admin-Token": admin_token}
    payload = {"name": name, "description": description, "price": price}
    try:
        response = requests.post(f"{BASE_URL}/admin/menu", headers=headers, json=payload)
        _handle_response(response)
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server. Is the Flask server running?")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def delete_pizza(pizza_id, admin_token):
    """Deletes a pizza from the menu (admin only)."""
    print(f"Deleting pizza ID: {pizza_id} (admin action)...")
    headers = {"X-Admin-Token": admin_token}
    try:
        response = requests.delete(f"{BASE_URL}/admin/menu/{pizza_id}", headers=headers)
        _handle_response(response)
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server. Is the Flask server running?")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def cancel_admin_order(order_id, admin_token):
    """Cancels an order regardless of status (admin only)."""
    print(f"Attempting to cancel order ID: {order_id} (admin action)...")
    headers = {"X-Admin-Token": admin_token}
    try:
        response = requests.delete(f"{BASE_URL}/admin/order/{order_id}", headers=headers)
        _handle_response(response)
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server. Is the Flask server running?")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def list_all_orders(admin_token):
    """Lists all orders (admin only)."""
    print("Listing all orders (admin action)...")
    headers = {"X-Admin-Token": admin_token}
    try:
        response = requests.get(f"{BASE_URL}/admin/orders", headers=headers)
        _handle_response(response)
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server. Is the Flask server running?")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def update_order_status(order_id, status, admin_token):
    """Updates the status of an order (admin only)."""
    print(f"Updating status for order ID: {order_id} to '{status}' (admin action)...")
    headers = {"X-Admin-Token": admin_token}
    payload = {"status": status}
    try:
        response = requests.put(f"{BASE_URL}/admin/order/{order_id}/status", headers=headers, json=payload)
        _handle_response(response)
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server. Is the Flask server running?")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# --- Main CLI Logic ---

def main():
    parser = argparse.ArgumentParser(description="Pizza Ordering CLI Client")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # --- Customer Commands ---
    # Menu
    menu_parser = subparsers.add_parser("menu", help="List the available pizzas on the menu.")
    menu_parser.set_defaults(func=list_menu)

    # Order
    order_parser = subparsers.add_parser("order", help="Manage customer orders.")
    order_subparsers = order_parser.add_subparsers(dest="order_command", help="Order commands")

    # Order Create
    order_create_parser = order_subparsers.add_parser("create", help="Create a new order.")
    order_create_parser.add_argument(
        "items",
        help="Comma-separated list of pizza_id:quantity pairs (e.g., 'pizza1:1,pizza3:2')"
    )
    order_create_parser.set_defaults(func=lambda args: create_order(args.items))

    # Order Status
    order_status_parser = order_subparsers.add_parser("status", help="Check the status of an order.")
    order_status_parser.add_argument("order_id", help="The ID of the order to check.")
    order_status_parser.set_defaults(func=lambda args: check_order_status(args.order_id))

    # Order Cancel (Customer)
    order_cancel_parser = order_subparsers.add_parser("cancel", help="Cancel an order (customer).")
    order_cancel_parser.add_argument("order_id", help="The ID of the order to cancel.")
    order_cancel_parser.set_defaults(func=lambda args: cancel_customer_order(args.order_id))

    # --- Admin Commands ---
    admin_parser = subparsers.add_parser("admin", help="Admin operations (requires --token).")
    admin_parser.add_argument("--token", required=True, help="Admin authentication token.")
    admin_subparsers = admin_parser.add_subparsers(dest="admin_command", help="Admin commands")

    # Admin Add Pizza
    admin_add_pizza_parser = admin_subparsers.add_parser("add-pizza", help="Add a new pizza to the menu.")
    admin_add_pizza_parser.add_argument("--name", required=True, help="Name of the pizza.")
    admin_add_pizza_parser.add_argument("--description", required=True, help="Description of the pizza.")
    admin_add_pizza_parser.add_argument("--price", type=float, required=True, help="Price of the pizza.")
    admin_add_pizza_parser.set_defaults(func=lambda args: add_pizza(args.name, args.description, args.price, args.token))

    # Admin Delete Pizza
    admin_delete_pizza_parser = admin_subparsers.add_parser("delete-pizza", help="Delete a pizza from the menu.")
    admin_delete_pizza_parser.add_argument("pizza_id", help="The ID of the pizza to delete.")
    admin_delete_pizza_parser.set_defaults(func=lambda args: delete_pizza(args.pizza_id, args.token))

    # Admin Cancel Order
    admin_cancel_order_parser = admin_subparsers.add_parser("cancel-order", help="Cancel an order regardless of its status.")
    admin_cancel_order_parser.add_argument("order_id", help="The ID of the order to cancel.")
    admin_cancel_order_parser.set_defaults(func=lambda args: cancel_admin_order(args.order_id, args.token))

    # Admin List All Orders
    admin_list_orders_parser = admin_subparsers.add_parser("list-orders", help="List all orders.")
    admin_list_orders_parser.set_defaults(func=lambda args: list_all_orders(args.token))

    # Admin Update Order Status
    admin_update_status_parser = admin_subparsers.add_parser("update-status", help="Update an order's status.")
    admin_update_status_parser.add_argument("order_id", help="The ID of the order to update.")
    admin_update_status_parser.add_argument("status", choices=["pending", "preparing", "ready_for_delivery", "delivered", "cancelled"],
                                            help="New status for the order.")
    admin_update_status_parser.set_defaults(func=lambda args: update_order_status(args.order_id, args.status, args.token))


    args = parser.parse_args()

    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()