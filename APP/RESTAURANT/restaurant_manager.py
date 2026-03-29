from rich.console import Console
from rich.panel import Panel

console = Console()

class RestaurantManager:

    def show_about(self):

        data = """
🍽️ Restaurant Name: Indixpert Restaurant

📍 Location: India

⭐ Rating: 4.5 / 5

🕒 Timing:
Morning: 9 AM - 12 PM
Afternoon: 1 PM - 5 PM
Evening: 6 PM - 11 PM

📞 Contact: 6287606576

💡 About:
Welcome to Indixpert Restaurant!
We provide the best quality food with excellent service.
Enjoy your meal with us 😍
"""

        console.print(Panel(data, title="🏨 About Restaurant", border_style="green"))