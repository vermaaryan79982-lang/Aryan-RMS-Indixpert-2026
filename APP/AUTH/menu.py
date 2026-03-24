from APP.AUTH.signup import Signup
from APP.AUTH.login import Login

from APP.MENU.menu_manager import menu_menu
from APP.ORDER.order_manager import order_menu
from APP.BOOKING.booking_manager import booking_menu
from APP.BILLING.payment_menu import billing_menu
from APP.REPORTS.report_manager import report_menu
from APP.INVENTORY.inventory_manager import inventory_menu

from rich.console import Console
from rich.panel import Panel
import questionary

console = Console()


class AuthMenu:

    def __init__(self):
        self.signup = Signup()
        self.login = Login()

    def start(self):
        while True:
            choice = questionary.select(
                "🔐 Welcome to RMS",
                choices=["Signup", "Login", "Exit"]
            ).ask()

            if choice == "Signup":
                self.signup.signup_user()

            elif choice == "Login":
                user = self.login.login_user()

                if user:
                    self.open_dashboard(user)

            elif choice == "Exit":
                break


    def open_dashboard(self, user):
        role = user["role"].lower()
        user_id = user.get("id")

        console.print(Panel(f"👤 Logged in as: {role.upper()}", style="bold yellow"))

        if role == "user":
            self.user_dashboard(user_id)

        elif role == "admin":
            self.admin_dashboard()

        elif role == "manager":
            self.manager_dashboard()

        elif role == "chef":
            self.chef_dashboard()

        elif role == "staff":
            self.staff_dashboard()

        elif role == "inventory":
            self.inventory_dashboard()

        else:
            console.print("[red]❌ Unknown Role[/red]")


    def user_dashboard(self, user_id):
        while True:
            console.print(Panel("🌟 USER DASHBOARD 🌟", style="cyan"))

            choice = questionary.select(
                "Choose Option:",
                choices=[
                    "🍽️ View Menu",
                    "🛒 Place Order",
                    "📦 My Orders",
                    "🪑 Book Table",
                    "💳 Pay Bill",
                    "🚪 Logout"
                ]
            ).ask()

            if choice == "🍽️ View Menu":
                menu_menu(view_only=True)

            elif choice == "🛒 Place Order":
                order_menu(user_id)

            elif choice == "📦 My Orders":
                order_menu(user_id)

            elif choice == "🪑 Book Table":
                booking_menu(user_id)

            elif choice == "💳 Pay Bill":
                billing_menu(user_id)

            elif choice == "🚪 Logout":
                break


    def admin_dashboard(self):
        while True:
            console.print(Panel("🛡️ ADMIN DASHBOARD 🛡️", style="red"))

            choice = questionary.select(
                "Choose Option:",
                choices=[
                    "➕ Manage Menu",
                    "📊 Reports",
                    "📦 Inventory",
                    "🚪 Logout"
                ]
            ).ask()

            if choice == "➕ Manage Menu":
                menu_menu()

            elif choice == "📊 Reports":
                report_menu()

            elif choice == "📦 Inventory":
                inventory_menu()

            elif choice == "🚪 Logout":
                break

  
    def manager_dashboard(self):
        while True:
            console.print(Panel("📊 MANAGER DASHBOARD 📊", style="green"))

            choice = questionary.select(
                "Choose Option:",
                choices=[
                    "📊 Reports",
                    "📦 Inventory",
                    "🚪 Logout"
                ]
            ).ask()

            if choice == "📊 Reports":
                report_menu()

            elif choice == "📦 Inventory":
                inventory_menu()

            elif choice == "🚪 Logout":
                break


    def chef_dashboard(self):
        from APP.ORDER.order_manager import OrderManager
        manager = OrderManager()

        while True:
            console.print(Panel("👨‍🍳 CHEF DASHBOARD 👨‍🍳", style="magenta"))

            choice = questionary.select(
                "Choose Option:",
                choices=[
                    "📦 View Orders",
                    "🔄 Update Status",
                    "🚪 Logout"
                ]
            ).ask()

            if choice == "📦 View Orders":
                manager.view_all_orders()

            elif choice == "🔄 Update Status":
                manager.update_status()

            elif choice == "🚪 Logout":
                break


    def staff_dashboard(self):
        while True:
            console.print(Panel("🛎️ STAFF DASHBOARD 🛎️", style="blue"))

            choice = questionary.select(
                "Choose Option:",
                choices=[
                    "📦 View Orders",
                    "🛒 Take Order",
                    "💰 Billing",
                    "🚪 Logout"
                ]
            ).ask()

            if choice == "📦 View Orders":
                order_menu()

            elif choice == "🛒 Take Order":
                order_menu()

            elif choice == "💰 Billing":
                billing_menu()

            elif choice == "🚪 Logout":
                break


    def inventory_dashboard(self):
        while True:
            console.print(Panel("📦 INVENTORY DASHBOARD 📦", style="yellow"))

            choice = questionary.select(
                "Choose Option:",
                choices=[
                    "📊 View Stock",
                    "➕ Add Item",
                    "✏️ Update Item",
                    "❌ Remove Item",
                    "⚠️ Low Stock",
                    "🚪 Logout"
                ]
            ).ask()

            if choice in [
                "📊 View Stock",
                "➕ Add Item",
                "✏️ Update Item",
                "❌ Remove Item",
                "⚠️ Low Stock"
            ]:
                inventory_menu()

            elif choice == "🚪 Logout":
                break


def start_menu():
    app = AuthMenu()
    app.start()