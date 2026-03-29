from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import questionary
from APP.DATABASE.db import DB
import random

console = Console()

class MenuManager:

    def __init__(self):
        self.db = DB()

   
    def view_menu(self):
        menu = self.db.read("menu.json")

        if not menu:
            console.print("[bold red]❌ Menu is empty[/bold red]")
            return

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

            table.add_column("ID", justify="center")
            table.add_column("Item Name", justify="left")
            table.add_column("Half (₹)", justify="center")
            table.add_column("Full (₹)", justify="center")

            for item in items:

                if cat == "dessert":
                    half = "-"
                    full = f"₹{item.get('price', item.get('full_price', 0))}"

                elif "half_price" in item:
                    half = f"₹{item['half_price']}"
                    full = f"₹{item['full_price']}"


                else:
                    half = "-"
                    full = f"₹{item.get('price', item.get('full_price', 0))}"

                table.add_row(
                    str(item["id"]),
                    item["name"],
                    half,
                    full
                )

            console.print(Panel(table, border_style="cyan"))
  
    def add_item(self):
        menu = self.db.read("menu.json")

        name = input("Enter Item Name: ")

        category = input("Enter Category (veg/nonveg/dessert): ").lower()

        if category not in ["veg", "nonveg", "dessert"]:
            console.print("[bold red]❌ Invalid Category[/bold red]")
            return

        has_half = input("Does item have half/full? (y/n): ").lower()

        if has_half == "y":
            half_price = input("Enter Half Price: ")
            full_price = input("Enter Full Price: ")

            if not (half_price.isdigit() and full_price.isdigit()):
                console.print("[bold red]❌ Invalid price[/bold red]")
                return

            item = {
                "id": random.randint(100, 999),
                "name": name,
                "category": category,
                "half_price": int(half_price),
                "full_price": int(full_price)
            }

        else:
            price = input("Enter Price: ")

            if not price.isdigit():
                console.print("[bold red]❌ Invalid price[/bold red]")
                return

            item = {
                "id": random.randint(100, 999),
                "name": name,
                "category": category,
                "price": int(price)
            }

        menu.append(item)
        self.db.write("menu.json", menu)

        console.print(Panel(f"✅ Item Added: {name}", style="green"))

    def update_item(self):
        menu = self.db.read("menu.json")
        self.view_menu()

        item_id = input("Enter Item ID to update: ")

        item = next((i for i in menu if str(i["id"]) == item_id), None)

        if not item:
            console.print("[bold red]❌ Item ID does not exist[/bold red]")
            return

        new_name = input("Enter new name: ")
        item["name"] = new_name

        new_cat = input("Enter Category (veg/nonveg/dessert): ").lower()
        if new_cat in ["veg", "nonveg", "dessert"]:
            item["category"] = new_cat

        if "half_price" in item:
            half = input("Enter Half Price: ")
            full = input("Enter Full Price: ")

            if half.isdigit() and full.isdigit():
                item["half_price"] = int(half)
                item["full_price"] = int(full)
        else:
            price = input("Enter Price: ")
            if price.isdigit():
                item["price"] = int(price)

        self.db.write("menu.json", menu)

        console.print("[bold green]✅ Item Updated[/bold green]")

    def delete_item(self):
        menu = self.db.read("menu.json")
        self.view_menu()

        item_id = input("Enter Item ID to delete: ")

        item = next((i for i in menu if str(i["id"]) == item_id), None)

        if not item:
            console.print("[bold red]❌ Item ID does not exist[/bold red]")
            return

        menu.remove(item)
        self.db.write("menu.json", menu)

        console.print("[bold red]❌ Item Removed[/bold red]")

    def search_item(self):
        menu = self.db.read("menu.json")

        item_id = input("Enter Item ID to search: ")

        item = next((i for i in menu if str(i["id"]) == item_id), None)

        if not item:
            console.print("[bold red]❌ Item ID does not exist[/bold red]")
            return

        table = Table(title="🔍 Item Found", show_lines=True)
        table.add_column("ID", justify="center")
        table.add_column("Item Name", justify="left")
        table.add_column("Price (₹)", justify="right")

        if "half_price" in item:
            price = f"Half ₹{item['half_price']} | Full ₹{item['full_price']}"
        elif "full_price" in item:
            price = f"₹{item['full_price']}"
        else:
            price = f"₹{item.get('price', 0)}"

        table.add_row(str(item["id"]), item["name"], price)

        console.print(Panel(table, border_style="green"))



def menu_menu(view_only=False):
    manager = MenuManager()

    while True:
        if view_only:
            choice = questionary.select(
                "📋 Menu",
                choices=[
                    "📖 View Menu",
                    "🔙 Back"
                ]
            ).ask()
        else:
            choice = questionary.select(
                "📋 Menu Management",
                choices=[
                    "📖 View Menu",
                    "🔍 Search Item",
                    "➕ Add Item",
                    "✏️ Update Item",
                    "❌ Remove Item",
                    "🔙 Back"
                ]
            ).ask()

        if choice == "📖 View Menu":
            manager.view_menu()

        elif choice == "🔍 Search Item":
            manager.search_item()

        elif choice == "➕ Add Item":
            manager.add_item()

        elif choice == "✏️ Update Item":
            manager.update_item()

        elif choice == "❌ Remove Item":
            manager.delete_item()

        elif choice == "🔙 Back":
            break