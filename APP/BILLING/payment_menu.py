from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import questionary
from datetime import datetime
from APP.DATABASE.db import DB
import getpass

console = Console()

class BillingManager:

    def __init__(self):
        self.db = DB()

    def calculate_food_total(self, user_id):
        orders = self.db.read("orders.json")
        total = 0

        if not isinstance(orders, list):
            return 0

        for order in orders:
            if str(order.get("user_id")) == str(user_id):
                total += order.get("total", 0)

        return total

    def calculate_booking_total(self, user_id):
        bookings = self.db.read("booking.json")
        total = 0

        if not isinstance(bookings, list):
            return 0

        for b in bookings:
            if str(b.get("user_id")) == str(user_id):
                total += 500

        return total

    def show_bill(self, user_id):

        orders = self.db.read("orders.json")
        bookings = self.db.read("booking.json")

        food_total = self.calculate_food_total(user_id)
        booking_total = self.calculate_booking_total(user_id)

        subtotal = food_total + booking_total

        if subtotal == 0:
            console.print("[bold red]❌ No Bill Found[/bold red]")
            return 0

        gst = subtotal * 0.18
        total = subtotal + gst

        mobile = input("Enter Mobile Number: ")
        gst_number = "22AAAAA0000A1Z5"

        header = f"""
📱 Mobile: {mobile}
🧾 GST No: {gst_number}
📅 Date: {datetime.now().strftime("%Y-%m-%d")}
⏰ Time: {datetime.now().strftime("%H:%M:%S")}
"""
        console.print(Panel(header, title="Customer Details", border_style="green"))

        console.print("[bold cyan]🧾 Order Details[/bold cyan]")

        user_orders = [o for o in orders if str(o.get("user_id")) == str(user_id)]

        if user_orders:
            for order in user_orders:
                table = Table(title=f"Order ID: {order.get('order_id')}", show_lines=True)

                table.add_column("Item")
                table.add_column("Qty")
                table.add_column("Price")

                for item in order.get("items", []):
                    table.add_row(
                        item.get("name", ""),
                        str(item.get("qty", "")),
                        f"₹{item.get('price', '')}"
                    )

                console.print(Panel(table, border_style="cyan"))

                console.print(
                    f"[yellow]Date:[/yellow] {order.get('date', 'N/A')}  "
                    f"[yellow]Time:[/yellow] {order.get('time', 'N/A')}"
                )
        else:
            console.print("[red]No Orders Found[/red]")

        console.print("\n[bold magenta]🪑 Booking Details[/bold magenta]")

        user_bookings = [b for b in bookings if str(b.get("user_id")) == str(user_id)]

        if user_bookings:
            table = Table(show_lines=True)
            table.add_column("Table No")
            table.add_column("Slot")
            table.add_column("Date")
            table.add_column("Time")

            for b in user_bookings:
                table.add_row(
                    str(b.get("table_no")),
                    b.get("slot", ""),
                    b.get("date", ""),
                    b.get("time", "")
                )

            console.print(Panel(table, border_style="magenta"))
        else:
            console.print("[red]No Booking Found[/red]")

        
        table = Table(title="📊 Billing Summary", show_lines=True)
        table.add_column("Type")
        table.add_column("Amount (₹)")

        table.add_row("Food Orders 🍽️", str(food_total))
        table.add_row("Table Booking 🪑", str(booking_total))
        table.add_row("Subtotal", str(subtotal))
        table.add_row("GST (18%)", str(round(gst, 2)))
        table.add_row("TOTAL 💵", str(round(total, 2)))

        console.print(Panel(table))

        return total

    
    def clear_user_booking(self, user_id):
        data = self.db.read("booking.json")
        new_data = [b for b in data if str(b.get("user_id")) != str(user_id)]
        self.db.write("booking.json", new_data)

    from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import questionary
from datetime import datetime
from APP.DATABASE.db import DB
import getpass

console = Console()

class BillingManager:

    def __init__(self):
        self.db = DB()

    def calculate_food_total(self, user_id):
        orders = self.db.read("orders.json")
        total = 0

        if not isinstance(orders, list):
            return 0

        for order in orders:
            if str(order.get("user_id")) == str(user_id):
                total += order.get("total", 0)

        return total

    def calculate_booking_total(self, user_id):
        bookings = self.db.read("booking.json")
        total = 0

        if not isinstance(bookings, list):
            return 0

        for b in bookings:
            if str(b.get("user_id")) == str(user_id):
                total += 500

        return total

    def show_bill(self, user_id):

        orders = self.db.read("orders.json")
        bookings = self.db.read("booking.json")

        food_total = self.calculate_food_total(user_id)
        booking_total = self.calculate_booking_total(user_id)

        subtotal = food_total + booking_total

        if subtotal == 0:
            console.print("[bold red]❌ No Bill Found[/bold red]")
            return 0

        gst = subtotal * 0.18
        total = subtotal + gst

        mobile = input("Enter Mobile Number: ")
        gst_number = "22AAAAA0000A1Z5"

        header = f"""
📱 Mobile: {mobile}
🧾 GST No: {gst_number}
📅 Date: {datetime.now().strftime("%Y-%m-%d")}
⏰ Time: {datetime.now().strftime("%H:%M:%S")}
"""
        console.print(Panel(header, title="Customer Details", border_style="green"))

        console.print("[bold cyan]🧾 Order Details[/bold cyan]")

        user_orders = [o for o in orders if str(o.get("user_id")) == str(user_id)]

        if user_orders:
            for order in user_orders:
                table = Table(title=f"Order ID: {order.get('order_id')}", show_lines=True)

                table.add_column("Item")
                table.add_column("Qty")
                table.add_column("Price")

                for item in order.get("items", []):
                    table.add_row(
                        item.get("name", ""),
                        str(item.get("qty", "")),
                        f"₹{item.get('price', '')}"
                    )

                console.print(Panel(table, border_style="cyan"))

                console.print(
                    f"[yellow]Date:[/yellow] {order.get('date', 'N/A')}  "
                    f"[yellow]Time:[/yellow] {order.get('time', 'N/A')}"
                )
        else:
            console.print("[red]No Orders Found[/red]")

        console.print("\n[bold magenta]🪑 Booking Details[/bold magenta]")

        user_bookings = [b for b in bookings if str(b.get("user_id")) == str(user_id)]

        if user_bookings:
            table = Table(show_lines=True)
            table.add_column("Table No")
            table.add_column("Slot")
            table.add_column("Date")
            table.add_column("Time")

            for b in user_bookings:
                table.add_row(
                    str(b.get("table_no")),
                    b.get("slot", ""),
                    b.get("date", ""),
                    b.get("time", "")
                )

            console.print(Panel(table, border_style="magenta"))
        else:
            console.print("[red]No Booking Found[/red]")

        
        table = Table(title="📊 Billing Summary", show_lines=True)
        table.add_column("Type")
        table.add_column("Amount (₹)")

        table.add_row("Food Orders 🍽️", str(food_total))
        table.add_row("Table Booking 🪑", str(booking_total))
        table.add_row("Subtotal", str(subtotal))
        table.add_row("GST (18%)", str(round(gst, 2)))
        table.add_row("TOTAL 💵", str(round(total, 2)))

        console.print(Panel(table))

        return total

    
    def clear_user_booking(self, user_id):
        data = self.db.read("booking.json")
        new_data = [b for b in data if str(b.get("user_id")) != str(user_id)]
        self.db.write("booking.json", new_data)

    def make_payment(self, user_id):

        bill_data = self.db.read("bill.json")
        if not isinstance(bill_data, list):
            bill_data = []

        food_total = self.calculate_food_total(user_id)
        booking_total = self.calculate_booking_total(user_id)

        if food_total + booking_total == 0:
            console.print("[bold red]❌ Nothing to pay[/bold red]")
            return

        total_amount = self.show_bill(user_id)
        if total_amount == 0:
            return

        method = questionary.select(
            "💳 Select Payment Method:",
            choices=["Cash", "UPI", "Card"]
        ).ask()

        if method == "Cash":
            console.print("[green]✅ Cash Payment Received[/green]")

        elif method == "Card":
            getpass.getpass("Enter Card Number: ")
            getpass.getpass("Enter CVV: ")
            console.print("[green]✅ Payment via Card[/green]")

        elif method == "UPI":
            console.print(Panel("📷 Scan QR"))
            input("Press Enter after scan...")
            getpass.getpass("Enter UPI PIN: ")
            console.print("[green]✅ Payment via UPI[/green]")

        # 🔹 Save bill
        bookings = self.db.read("booking.json")

        user_bookings = [
            b for b in bookings
            if str(b.get("user_id")) == str(user_id)
        ]

        bill_data.append({
            "user_id": user_id,
            "amount": total_amount,
            "method": method,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "time": datetime.now().strftime("%I:%M %p"),
            "bookings": user_bookings
        })

        self.db.write("bill.json", bill_data)

        # 🔹 Update booking status
        for b in bookings:
            if str(b.get("user_id")) == str(user_id):
                b["payment_status"] = "Paid"

        self.db.write("booking.json", bookings)

        # 🔹 Update orders as paid (IMPORTANT)
        orders = self.db.read("orders.json")

        for o in orders:
            if str(o.get("user_id")) == str(user_id):
                o["paid"] = True

        self.db.write("orders.json", orders)

        console.print(Panel("🎉 Payment Completed!", style="green"))
    def view_payment_history(self, user_id):
        data = self.db.read("bill.json")

        user_payments = [p for p in data if str(p.get("user_id")) == str(user_id)]

        if not user_payments:
            console.print("[red]❌ No Payment History Found[/red]")
            return

        table = Table(title="💰 Payment History", show_lines=True)

        table.add_column("Amount")
        table.add_column("Method")
        table.add_column("Date")
        table.add_column("Time")
        table.add_column("Status")

        for p in user_payments:
            table.add_row(
                f"₹{round(p.get('amount', 0), 2)}",
                p.get("method", ""),
                p.get("date", "N/A"),
                p.get("time", "N/A"),
                "Paid ✅"
            )

        console.print(Panel(table, border_style="green"))



def billing_menu(user_id):

    billing = BillingManager()

    while True:
        choice = questionary.select(
            "💰 Billing Menu",
            choices=[
                "📊 View Bill",
                "💳 Make Payment",
                "📜 Payment History",
                "🔙 Back"
            ]
        ).ask()

        if choice == "📊 View Bill":
            billing.show_bill(user_id)

        elif choice == "💳 Make Payment":
            billing.make_payment(user_id)
        
        elif choice == "📜Payment History":
            billing.view_payment_history(user_id)
        elif choice == "🔙 Back":
            break
    def view_payment_history(self, user_id):
        data = self.db.read("bill.json")

        user_payments = [p for p in data if str(p.get("user_id")) == str(user_id)]

        if not user_payments:
            console.print("[red]❌ No Payment History Found[/red]")
            return

        table = Table(title="💰 Payment History", show_lines=True)

        table.add_column("Amount")
        table.add_column("Method")
        table.add_column("Date")
        table.add_column("Time")
        table.add_column("Status")

        for p in user_payments:
            table.add_row(
                f"₹{round(p.get('amount', 0), 2)}",
                p.get("method", ""),
                p.get("date", "N/A"),
                p.get("time", "N/A"),
                "Paid ✅"
            )

        console.print(Panel(table, border_style="green"))



def billing_menu(user_id):

    billing = BillingManager()

    while True:
        choice = questionary.select(
            "💰 Billing Menu",
            choices=[
                "📊 View Bill",
                "💳 Make Payment",
                "📜 Payment History",
                "🔙 Back"
            ]
        ).ask()

        if choice == "📊 View Bill":
            billing.show_bill(user_id)

        elif choice == "💳 Make Payment":
            billing.make_payment(user_id)
        
        elif choice == "📜Payment History":
            billing.view_payment_history(user_id)
        elif choice == "🔙 Back":
            break


