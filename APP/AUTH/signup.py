import re
import random
from APP.DATABASE.db import DB
from APP.LOGS.error_handler import ErrorHandler
from rich.console import Console
import getpass

console = Console()

class Signup:

    def __init__(self):
        self.db = DB()
        self.logger = ErrorHandler()

    def generate_id(self):
        return str(random.randint(100000, 999999))

    def validate_name(self, name):
        return bool(re.match(r'^[A-Za-z ]+$', name))

    def validate_email(self, email):
        return bool(re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email))



    def validate_aadhar(self, aadhar):
        return bool(re.match(r'^\d{12}$', aadhar))

    def validate_pan(self, pan):
        return bool(re.match(r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$', pan))

    def validate_qualification(self, qual):
        allowed = ["10th", "12th", "graduate", "postgraduate"]
        return qual.lower() in allowed

    def signup_user(self):
        try:
            console.print("[bold cyan]📝 SIGNUP[/bold cyan]")


            name = input("Enter Name: ")
            if not self.validate_name(name):
                console.print("[bold red]❌ Invalid Name[/bold red]")
                return

            email = input("Enter Email: ")
            if not self.validate_email(email):
                console.print("[bold red]❌ Invalid Email[/bold red]")
                return

            users = self.db.read("users.json")

            for user in users:
                if user["email"] == email:
                    console.print("[bold red]❌ Email already exists[/bold red]")
                    return


            password = getpass.getpass("Enter Password: ")



  
            aadhar = input("Enter Aadhar Number (12 digit): ")
            if not self.validate_aadhar(aadhar):
                console.print("[bold red]❌ Invalid Aadhar Number[/bold red]")
                return


            pan = input("Enter PAN Number (ABCDE1234F): ")
            if not self.validate_pan(pan):
                console.print("[bold red]❌ Invalid PAN Number[/bold red]")
                return


            qualification = input("Enter Qualification (10th/12th/Graduate/PostGraduate): ")
            if not self.validate_qualification(qualification):
                console.print("[bold red]❌ Minimum 10th required[/bold red]")
                return


            address = input("Enter Address: ")


            state = input("Enter State: ")

         
            country = input("Enter Country: ")

           
            bike = input("Do you ride a bike? (y/n): ").lower()

            license_no = None
            if bike == "y":
                license_no = input("Enter Driving License Number: ")

            # 🔥 USER DATA

            user_data = {
                "id": self.generate_id(),
                "name": name,
                "email": email,
                "password": password,
                "aadhar": aadhar,
                "pan": pan,
                "qualification": qualification,
                "address": address,
                "state": state,
                "country": country,
                "bike": bike,
                "license": license_no,
                "role": "staff"
            }

            users.append(user_data)
            self.db.write("users.json", users)

            console.print("[bold green]✅ Signup Successful[/bold green]")

        except Exception as e:
            self.logger.log(str(e))
            console.print("[bold red]❌ Error occurred[/bold red]")

