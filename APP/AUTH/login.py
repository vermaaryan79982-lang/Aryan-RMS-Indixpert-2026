from APP.DATABASE.db import DB
from APP.LOGS.error_handler import ErrorHandler
from rich.console import Console
import getpass
import random

console = Console()

class Login:

    def __init__(self):
        self.db = DB()
        self.logger = ErrorHandler()

      
        self.questions = [
            {
                "question": "What is the color of sky?",
                "options": ["a) Blue", "b) Red", "c) Green"],
                "answer": "a"
            },
            {
                "question": "2 + 2 = ?",
                "options": ["a) 3", "b) 4", "c) 5"],
                "answer": "b"
            },
            {
                "question": "Capital of India?",
                "options": ["a) Delhi", "b) Mumbai", "c) Kolkata"],
                "answer": "a"
            }
        ]

    def security_question(self):
        q = random.choice(self.questions)

        console.print("\n[bold yellow]🔐 Security Check[/bold yellow]")
        console.print(q["question"])

        for opt in q["options"]:
            console.print(opt)

        ans = input("Enter answer (a/b/c): ").lower()

        return ans == q["answer"]

    def forgot_password(self):
        try:
            console.print("\n[bold cyan]🔁 Forgot Password[/bold cyan]")

            email = input("Enter your email: ")
            users = self.db.read("users.json")

            for user in users:
                if user["email"] == email:

                    # OTP generate
                    otp = str(random.randint(1000, 9999))
                    console.print(f"[bold yellow]📩 OTP Sent: {otp}[/bold yellow]")

                    user_otp = input("Enter OTP: ")

                    if user_otp == otp:
                        new_pass = getpass.getpass("Enter new password: ")
                        user["password"] = new_pass

                        self.db.write("users.json", users)

                        console.print("[bold green]✅ Password Reset Successful[/bold green]")
                        return
                    else:
                        console.print("[bold red]❌ Wrong OTP[/bold red]")
                        return

            console.print("[bold red]❌ Email not found[/bold red]")

        except Exception as e:
            self.logger.log(str(e))
            console.print("[bold red]❌ Error occurred[/bold red]")

    def login_user(self):
        try:
            while True:
                console.print("\n[bold cyan]🔐 LOGIN MENU[/bold cyan]")
                console.print("1. Login")
                console.print("2. Forgot Password")
                console.print("3. Exit")

                choice = input("Enter choice: ")

                if choice == "1":
                    email = input("Enter Email: ")
                    password = getpass.getpass("Enter Password: ")

                    if not self.security_question():
                        console.print("[bold red]❌ Security Check Failed[/bold red]")
                        return None

                    users = self.db.read("users.json")

                    for user in users:
                        if user["email"] == email and user["password"] == password:
                            console.print("[bold green]✅ Login Successful[/bold green]")
                            return user

                    console.print("[bold red]❌ Invalid Credentials[/bold red]")

                elif choice == "2":
                    self.forgot_password()

                elif choice == "3":
                    return None

                else:
                    console.print("[bold red]❌ Invalid Choice[/bold red]")

        except Exception as e:
            self.logger.log(str(e))
            console.print("[bold red]❌ Error occurred[/bold red]")
            return None