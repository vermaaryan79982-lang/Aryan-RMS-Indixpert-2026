from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import questionary
from APP.DATABASE.db import DB

console = Console()

class ReportManager:

    def __init__(self):
        self.db = DB()

    def total_sales(self):
        orders = self.db.read("orders.json")

        if not isinstance(orders, list):
            orders = []

        total = sum(o.get("total", 0) for o in orders)
        count = len(orders)

        table = Table(title="📊 SALES REPORT", show_lines=True)
        table.add_column("Metric")
        table.add_column("Value")

        table.add_row("Total Orders", str(count))
        table.add_row("Total Revenue (₹)", str(total))

        console.print(Panel(table, border_style="green"))


    def all_orders(self):
        orders = self.db.read("orders.json")

        if not isinstance(orders, list) or not orders:
            console.print("[bold red]❌ No orders found[/bold red]")
            return

        table = Table(title="📦 ALL ORDERS", show_lines=True)

        table.add_column("Order ID")
        table.add_column("User ID")
        table.add_column("Total ₹")
        table.add_column("Status")
        table.add_column("Paid")

        for order in orders:
            table.add_row(
                str(order.get("order_id")),
                str(order.get("user_id")),
                str(order.get("total")),
                order.get("status", "Pending"),
                "✅" if order.get("paid") else "❌"
            )

        console.print(Panel(table, border_style="cyan"))

    def booking_report(self):
        data = self.db.read("booking.json")

        if not isinstance(data, list) or len(data) == 0:
            console.print("[red]❌ No Booking Found[/red]")
            return

        table = Table(title="🪑 TABLE BOOKINGS REPORT", show_lines=True)

        table.add_column("ID")
        table.add_column("User ID")
        table.add_column("Table")
        table.add_column("People")
        table.add_column("Slot")
        table.add_column("Date")
        table.add_column("Amount")

        for b in data:
            table.add_row(
                str(b.get("id")),
                str(b.get("user_id")),
                str(b.get("table")),
                str(b.get("people")),
                b.get("slot"),
                b.get("date"),
                f"₹{b.get('price', 0)}"
            )

        console.print(Panel(table, border_style="yellow"))

    def user_spending(self):
        orders = self.db.read("orders.json")

        if not isinstance(orders, list):
            orders = []

        spending = {}

        for order in orders:
            uid = str(order.get("user_id"))
            spending[uid] = spending.get(uid, 0) + order.get("total", 0)

        if not spending:
            console.print("[red]❌ No Data Found[/red]")
            return

        table = Table(title="👤 USER SPENDING REPORT", show_lines=True)

        table.add_column("User ID")
        table.add_column("Total Spent ₹")

        for uid, amt in spending.items():
            table.add_row(uid, str(amt))

        console.print(Panel(table, border_style="magenta"))


def report_menu():
    manager = ReportManager()

    while True:
        choice = questionary.select(
            "📊 Reports Menu",
            choices=[
                "💰 Total Sales",
                "📦 All Orders",
                "🪑 Table Bookings",
                "👤 User Spending",
                "🔙 Back"
            ]
        ).ask()

        if choice == "💰 Total Sales":
            manager.total_sales()

        elif choice == "📦 All Orders":
            manager.all_orders()

        elif choice == "🪑 Table Bookings":
            manager.booking_report()

        elif choice == "👤 User Spending":
            manager.user_spending()

        elif choice == "🔙 Back":
            break