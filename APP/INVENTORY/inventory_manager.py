from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import questionary
from APP.DATABASE.db import DB
import random

console = Console()

class InventoryManager:

    def __init__(self):
        self.db = DB()

    def view_stock(self):
        inventory = self.db.read("inventory.json")

        if not inventory:
            console.print("[bold red]❌ Inventory Empty[/bold red]")
            return

        table = Table(title="📦 INVENTORY STOCK", show_lines=True)

        table.add_column("ID", justify="center")
        table.add_column("Item", justify="left")
        table.add_column("Quantity", justify="center")

        for item in inventory:
            table.add_row(str(item["id"]), item["name"], str(item["qty"]))

        console.print(Panel(table, border_style="cyan"))


    def add_item(self):
        inventory = self.db.read("inventory.json")

        name = input("Enter Item Name: ")
        qty = input("Enter Quantity: ")

        if not qty.isdigit():
            console.print("[bold red]❌ Invalid quantity[/bold red]")
            return

        item = {
            "id": random.randint(100, 999),
            "name": name,
            "qty": int(qty)
        }

        inventory.append(item)
        self.db.write("inventory.json", inventory)

        console.print(Panel(f"✅ Item Added: {name}", style="green"))


    def update_item(self):
        inventory = self.db.read("inventory.json")
        self.view_stock()

        item_id = input("Enter Item ID to update: ")

        for item in inventory:
            if str(item["id"]) == item_id:
                new_qty = input("Enter new quantity: ")

                if not new_qty.isdigit():
                    console.print("[bold red]❌ Invalid quantity[/bold red]")
                    return

                item["qty"] = int(new_qty)
                self.db.write("inventory.json", inventory)

                console.print("[bold green]✅ Item Updated[/bold green]")
                return

        console.print("[bold red]❌ Item not found[/bold red]")


    def remove_item(self):
        inventory = self.db.read("inventory.json")
        self.view_stock()

        item_id = input("Enter Item ID to remove: ")

        for item in inventory:
            if str(item["id"]) == item_id:
                inventory.remove(item)
                self.db.write("inventory.json", inventory)

                console.print("[bold red]❌ Item Removed[/bold red]")
                return

        console.print("[bold red]❌ Item not found[/bold red]")


    def low_stock(self):
        inventory = self.db.read("inventory.json")

        low_items = [item for item in inventory if item["qty"] < 5]

        if not low_items:
            console.print("[bold green]✅ No low stock items[/bold green]")
            return

        table = Table(title="⚠️ LOW STOCK ALERT", show_lines=True)

        table.add_column("Item")
        table.add_column("Quantity")

        for item in low_items:
            table.add_row(item["name"], str(item["qty"]))

        console.print(Panel(table, border_style="red"))



def inventory_menu():
    manager = InventoryManager()

    while True:
        choice = questionary.select(
            "📦 Inventory Menu",
            choices=[
                "📊 View Stock",
                "➕ Add Item",
                "✏️ Update Item",
                "❌ Remove Item",
                "⚠️ Low Stock Alert",
                "🔙 Back"
            ]
        ).ask()

        if choice == "📊 View Stock":
            manager.view_stock()

        elif choice == "➕ Add Item":
            manager.add_item()

        elif choice == "✏️ Update Item":
            manager.update_item()

        elif choice == "❌ Remove Item":
            manager.remove_item()

        elif choice == "⚠️ Low Stock Alert":
            manager.low_stock()

        elif choice == "🔙 Back":
            break