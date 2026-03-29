from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import questionary
import random
from datetime import datetime
from APP.DATABASE.db import DB
from APP.LOGS.error_handler import ErrorHandler

console = Console()


class OrderManager:

    def __init__(self):
        self.db = DB()
        self.logger = ErrorHandler()


    def view_menu(self):
        try:
            menu = self.db.read("menu.json")

            categories = {
                "veg": [],
                "nonveg": [],
                "dessert": []
            }

            for item in menu:
                cat = item.get("category", "veg").lower()
                if cat in categories:
                    categories[cat].append(item)

            for cat, items in categories.items():

                if not items:
                    continue

                table = Table(title=f"🍽️ {cat.upper()} MENU", show_lines=True)
                table.add_column("ID")
                table.add_column("Item")
                table.add_column("Price ₹")

                for item in items:
                    if "half_price" in item:
                        price = f"H ₹{item['half_price']} | F ₹{item['full_price']}"
                    else:
                        price = f"₹{item.get('price', item.get('full_price', 0))}"

                    table.add_row(str(item["id"]), item["name"], price)

                console.print(Panel(table, border_style="cyan"))

        except Exception as e:
            self.logger.log(str(e))

    def place_order(self, user_id):
        try:
            menu = self.db.read("menu.json")
            self.view_menu()

            items = []
            total = 0

            while True:
                item_id = input("Enter Item ID (0 to stop): ")

                if item_id == "0":
                    break

                item = next((i for i in menu if str(i["id"]) == item_id), None)

                if not item:
                    console.print("[bold red]❌ Item ID does not exist[/bold red]")
                    continue

                qty = int(input("Enter Quantity: "))

                if "half_price" in item:
                    choice = input("Type (h=Half / f=Full): ").lower()

                    if choice == "h":
                        price = item["half_price"]
                        size = "Half"
                    else:
                        price = item["full_price"]
                        size = "Full"
                else:
                    price = item.get("price", item.get("full_price", 0))
                    size = "Full"

                items.append({
                    "name": item["name"],
                    "price": price,
                    "qty": qty,
                    "size": size
                })

                total += price * qty

            if not items:
                console.print("[red]❌ No items selected[/red]")
                return

            orders = self.db.read("orders.json")

            order = {
                "order_id": random.randint(1000, 9999),
                "user_id": user_id,
                "mobile": user_id,
                "items": items,
                "total": total,
                "status": "Pending",
                "paid": False,
                "date": datetime.now().strftime("%Y-%m-%d"),
                "time":datetime.now().strftime("%H:%M:%S")
            }

            orders.append(order)
            self.db.write("orders.json", orders)

            console.print(Panel(f"✅ Order Placed ₹{total}", style="green"))

        except Exception as e:
            self.logger.log(str(e))

    def view_orders(self, user_id):
        try:
            orders = self.db.read("orders.json")

            found = False
            for order in orders:
                if order["user_id"] == user_id:

                    table = Table(title=f"🧾 Order #{order['order_id']}", show_lines=True)
                    table.add_column("Item")
                    table.add_column("Size Excess (EXCL. GST)")
                    table.add_column("Qty")
                    table.add_column("Price")

                    for item in order["items"]:
                        table.add_row(
                            item["name"],
                            item.get("size", "Full"),
                            str(item["qty"]),
                            f"₹{item['price']}"
                        )

                    console.print(Panel(table, border_style="yellow"))
                    console.print(f"[bold green]Total: ₹{order['total']}[/bold green]\n")

                    found = True

            if not found:
                console.print("[red]❌ No orders found[/red]")

        except Exception as e:
            self.logger.log(str(e))


    def add_item_to_order(self, user_id):
        orders = self.db.read("orders.json")
        menu = self.db.read("menu.json")

        oid = input("Enter Order ID: ")

        for order in orders:
            if str(order["order_id"]) == oid and order["user_id"] == user_id:

                self.view_menu()
                item_id = input("Enter Item ID: ")

                item = next((i for i in menu if str(i["id"]) == item_id), None)

                if not item:
                    console.print("[bold red]❌ Item ID does not exist[/bold red]")
                    return

                qty = int(input("Enter Quantity: "))

                if "half_price" in item:
                    choice = input("Type (h=Half / f=Full): ").lower()

                    if choice == "h":
                        price = item["half_price"]
                        size = "Half"
                    else:
                        price = item["full_price"]
                        size = "Full"
                else:
                    price = item.get("price", item.get("full_price", 0))
                    size = "Full"

                order["items"].append({
                    "name": item["name"],
                    "price": price,
                    "qty": qty,
                    "size": size
                })

                order["total"] += price * qty
                self.db.write("orders.json", orders)

                console.print("[green]✅ Item Added[/green]")
                return

        console.print("[red]❌ Order not found[/red]")

    def remove_item_from_order(self, user_id):
        orders = self.db.read("orders.json")

        oid = input("Enter Order ID: ")

        for order in orders:
            if str(order["order_id"]) == oid and order["user_id"] == user_id:

                for i, item in enumerate(order["items"]):
                    print(f"{i+1}. {item['name']} ({item.get('size','Full')}) x{item['qty']}")

                idx = int(input("Select item number to remove: ")) - 1

                removed = order["items"].pop(idx)
                order["total"] -= removed["price"] * removed["qty"]

                self.db.write("orders.json", orders)

                console.print("[red]❌ Item Removed[/red]")
                return

        console.print("[red]❌ Order not found[/red]")

    def view_all_orders(self):
        orders = self.db.read("orders.json")

        for order in orders:
            console.print(Panel(str(order), border_style="cyan"))

    def update_status(self):
        orders = self.db.read("orders.json")

        oid = input("Enter Order ID: ")

        for order in orders:
            if str(order["order_id"]) == oid:
                status = input("Enter Status (Preparing/Done): ")
                order["status"] = status

                self.db.write("orders.json", orders)
                console.print("[green]✅ Updated[/green]")
                return

        console.print("[red]❌ Not found[/red]")

    def view_orders(self, user_id):
        orders = self.db.read("orders.json")

        user_orders = [o for o in orders if o["user_id"] == user_id]

        if not user_orders:
            console.print("[red]❌ No orders found[/red]")
            return

        for order in user_orders:
            table = Table(title=f"🧾 Order #{order['order_id']}", show_lines=True)

            table.add_column("Item")
            table.add_column("Qty")
            table.add_column("Price")

            for item in order["items"]:
                table.add_row(
                    item["name"],
                    str(item["qty"]),
                    f"₹{item['price']}"
                )

            console.print(Panel(table, border_style="cyan"))
            console.print(f"[bold yellow]Date:[/bold yellow] {order['date']}  ⏰ {order['time']}")
            console.print(f"[bold green]Total: ₹{order['total']}[/bold green]\n")



def order_menu(user_id=None):
    manager = OrderManager()

    while True:
        choice = questionary.select(
            "🛒 Order Menu",
            choices=[
                "📋 View Menu",
                "🛒 Place Order",
                "📦 View Orders",
                "➕ Add Item to Order",
                "❌ Remove Item from Order",
                "🔙 Back"
            ]
        ).ask()

        if choice == "📋 View Menu":
            manager.view_menu()

        elif choice == "🛒 Place Order":
            manager.place_order(user_id)

        elif choice == "📦 View Orders":
            manager.view_orders(user_id)

        elif choice == "➕ Add Item to Order":
            manager.add_item_to_order(user_id)

        elif choice == "❌ Remove Item from Order":
            manager.remove_item_from_order(user_id)

        elif choice == "🔙 Back":
            break