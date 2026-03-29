
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import questionary
from APP.DATABASE.db import DB
import datetime

console = Console()

class BookingManager:

    def __init__(self):
        self.db = DB()

    def validate_user(self, user_id):
        users = self.db.read("users.json")
        for user in users:
            if str(user["id"]) == str(user_id):
                return True
        return False


    def get_valid_date(self):
        today = datetime.date.today()
        date_input = input("Enter Booking Date (YYYY-MM-DD): ")

        try:
            user_date = datetime.datetime.strptime(date_input, "%Y-%m-%d").date()

            if user_date < today:
                console.print("[bold red]❌ Past date not allowed[/bold red]")
                return None

            if user_date > today + datetime.timedelta(days=10):
                console.print("[bold red]❌ Only 10 days allowed[/bold red]")
                return None

            return str(user_date)

        except:
            console.print("[bold red]❌ Invalid format[/bold red]")
            return None

    def is_slot_valid(self, slot, booking_date):
        now = datetime.datetime.now()
        today = str(datetime.date.today())

        if booking_date == today:
            hour = now.hour
            if slot == "morning" and hour >= 12:
                return False
            if slot == "afternoon" and hour >= 17:
                return False
            if slot == "evening" and hour >= 22:
                return False

        return True

    def is_booked(self, data, table, slot, date):
        for b in data:
            if (
                str(b["table"]) == str(table)
                and b["slot"] == slot
                and b["date"] == date
            ):
                return True
        return False

    def show_tables(self, date):
        data = self.db.read("booking.json")

        if not isinstance(data, list):
            data = []

        table = Table(title=f"🪑 BOOKINGS ({date})", show_lines=True)
        table.add_column("Table")
        table.add_column("Morning")
        table.add_column("Afternoon")
        table.add_column("Evening")

        for i in range(1, 11):
            row = []
            for slot in ["morning", "afternoon", "evening"]:
                if self.is_booked(data, str(i), slot, date):
                    row.append("❌ Booked")
                else:
                    row.append("✅ Available")
            table.add_row(str(i), *row)

        console.print(Panel(table, border_style="cyan"))


    def book_table(self, user_id):

        if not self.validate_user(user_id):
            console.print("[bold red]❌ Invalid User ID[/bold red]")
            return

        date = self.get_valid_date()
        if not date:
            return

        data = self.db.read("booking.json")

        if not isinstance(data, list):
            data = []

        self.show_tables(date)

        # ================= 👤 USER INFO =================
        name = input("👤 Enter Name: ")
        mobile = input("📱 Enter Mobile No: ")

        try:
            people = int(input("👥 Total People: "))
        except:
            console.print("[red]Invalid number[/red]")
            return

        # ================= 🪑 TABLE CAPACITY =================
        tables = {
            1:2, 2:4, 3:6, 4:4, 5:2,
            6:6, 7:4, 8:2, 9:6, 10:4
        }

        # ================= SHOW TABLE CAPACITY =================
        t = Table(title="🪑 TABLE SEATING INFO", show_lines=True)
        t.add_column("Table", style="yellow")
        t.add_column("Chairs", style="green")

        for k, v in tables.items():
            t.add_row(str(k), str(v))

        console.print(Panel(t, border_style="cyan"))

        # ================= 🤖 SUGGESTION =================
        suggested = [t for t, c in tables.items() if c >= people]

        console.print(Panel(
            f"[bold magenta]🤖 Suggested Tables for {people} people:[/bold magenta]\n"
            f"{suggested if suggested else 'No single table available'}",
            border_style="magenta"
        ))

        try:
            table_no = int(input("👉 Select Table No: "))
        except:
            console.print("[red]Invalid table[/red]")
            return

        # ================= SLOT =================
        slot = questionary.select(
            "Select Slot:",
            choices=["morning", "afternoon", "evening"]
        ).ask()

        if not self.is_slot_valid(slot, date):
            console.print("[bold red]⏰ Slot over[/bold red]")
            return

        if self.is_booked(data, table_no, slot, date):
            console.print("[bold red]❌ Already Booked[/bold red]")
            return

        # ================= VALIDATION =================
        if people > tables.get(table_no, 0):
            console.print("[red]❌ Exceeds table capacity[/red]")
            return

        # ================= PRICE =================
        price_per_person = 100
        total_price = people * price_per_person

        import random
        booking_id = random.randint(1000, 9999)

        # ================= SAVE =================
        booking = {
            "id": booking_id,
            "name": name,
            "mobile": mobile,
            "table": str(table_no),
            "people": people,
            "slot": slot,
            "user_id": str(user_id),
            "date": date,
            "time": datetime.datetime.now().strftime("%I:%M %p"),
            "price": total_price,
            "payment_status": "Pending"
        }

        data.append(booking)
        self.db.write("booking.json", data)

        # ================= OUTPUT =================
        console.print(Panel(
            f"[bold green]✅ BOOKING CONFIRMED[/bold green]\n\n"
            f"🆔 ID      : {booking_id}\n"
            f"👤 Name    : {name}\n"
            f"📱 Mobile  : {mobile}\n"
            f"🪑 Table   : {table_no} ({tables[table_no]} chairs)\n"
            f"👥 People  : {people}\n"
            f"🕒 Slot    : {slot}\n"
            f"💰 Total   : ₹{total_price}",
            border_style="green"
        ))
    def cancel_booking(self, user_id):
        data = self.db.read("booking.json")

        if not isinstance(data, list):
            data = []


        date = input("Enter Booking Date to Cancel (YYYY-MM-DD): ")
        table_no = input("Enter Table No: ")

        slot = questionary.select(
            "Select Slot to Cancel:",
            choices=["morning", "afternoon", "evening"]
        ).ask()

        new_data = []
        found = False

        for b in data:
            if (
                str(b["user_id"]) == str(user_id)
                and str(b["table"]) == str(table_no)
                and b["slot"] == slot
                and b["date"] == date
            ):
                found = True
                continue
            new_data.append(b)

        if found:
            self.db.write("booking.json", new_data)
            console.print("[bold red]❌ Booking Cancelled[/bold red]")
        else:
            console.print("[bold red]❌ No booking found[/bold red]")

    def view_booking_history(self, user_id):

        bookings = self.db.read("booking.json") 

        if not isinstance(bookings, list):
            bookings = []

        user_id = str(user_id)

        user_bookings = [
            b for b in bookings
            if str(b.get("user_id")) == user_id 
        ]

        if not user_bookings:
            console.print("[bold red]❌ No bookings found[/bold red]")
            return

        table = Table(
            title="🪑 Your Booking History",
            show_lines=True
        )

        table.add_column("Table", style="yellow")
        table.add_column("Slot", style="green")
        table.add_column("Date", style="cyan")
        table.add_column("status", style="magenta")

        for b in user_bookings:
            table.add_row(
                str(b.get("table")), 
                b.get("slot"),
                b.get("date"),
                b.get("payment-status", "pending")
            )

        console.print(Panel(table, border_style="green"))

def booking_menu(user_id):

    manager = BookingManager()

    while True:
        choice = questionary.select(
            "🪑 Booking Menu",
            choices=[
                "📊 View Tables",
                "🪑 Book Table",
                "📜 View Booking History",
                "❌ Cancel Booking",
                "🔙 Back"
            ]
        ).ask()

        if choice == "📊 View Tables":
            date = manager.get_valid_date()
            if date:
                manager.show_tables(date)

        elif choice == "🪑 Book Table":
            manager.book_table(user_id)

        elif choice == "📜 View Booking History":
            manager.view_booking_history(user_id)

        elif choice == "❌ Cancel Booking":
            manager.cancel_booking(user_id)

        elif choice == "🔙 Back":
            break



