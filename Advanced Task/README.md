# Pizzeria CLI Client and Web Server

The `pizzas_cli.py` command-line tool allows you to interact with the Pizza Ordering API server. You can view the menu, place orders, check order status, and perform admin operations such as managing the menu and orders.

---

## Prerequisites

- Python 3.x
- `requests` library  
  Install with:
  ```bash
  pip install requests
  ```
- The Pizza API server must be running and accessible at `http://127.0.0.1:5000` (or update `BASE_URL` in the script if different).

    Run the API server ina new terminal with `python3 WebServer/app.py`

---

## Usage

Make the script executable (optional):

```bash
chmod +x pizzas_cli.py
```

Run the script with Python:

```bash
./pizzas_cli.py <command> [options]
```
or
```bash
python3 pizzas_cli.py <command> [options]
```

---

## Customer Commands

### View Menu

```bash
./pizzas_cli.py menu
```

### Create an Order

```bash
./pizzas_cli.py order create 'pizza_id:quantity,pizza_id:quantity'
```
Example:
```bash
./pizzas_cli.py order create 'pizza1:2,pizza3:1'
```

### Check Order Status

```bash
./pizzas_cli.py order status <order_id>
```

### Cancel an Order

```bash
./pizzas_cli.py order cancel <order_id>
```

---

## Admin Commands

All admin commands require the `--token` argument for authentication.

`ADMIN_TOKEN = "supersecretadmintoken123"`
### Add a Pizza

```bash
./pizzas_cli.py admin --token <ADMIN_TOKEN> add-pizza --name "Pizza Name" --description "Description" --price 12.99
```

### Delete a Pizza

```bash
./pizzas_cli.py admin --token <ADMIN_TOKEN> delete-pizza <pizza_id>
```

### Cancel Any Order

```bash
./pizzas_cli.py admin --token <ADMIN_TOKEN> cancel-order <order_id>
```

### List All Orders

```bash
./pizzas_cli.py admin --token <ADMIN_TOKEN> list-orders
```

### Update Order Status

```bash
./pizzas_cli.py admin --token <ADMIN_TOKEN> update-status <order_id> <status>
```
Where `<status>` is one of: `pending`, `preparing`, `ready_for_delivery`, `delivered`, `cancelled`

---

## Notes

- Replace `<ADMIN_TOKEN>`, `<order_id>`, `<pizza_id>`, etc., with actual values.
- For help on commands:
  ```bash
  ./pizzas_cli.py --help
  ./pizzas_cli.py <command> --help
  ```

---