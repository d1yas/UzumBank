import requests
import json
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "API orqali barcha foydalanuvchilarni olish"

    def handle(self, *args, **kwargs):
        url = "http://127.0.0.1:8000/user/allusers/"  # URL ni to‘g‘riladik
        response = requests.get(url)

        if response.status_code == 200:
            users = response.json()
            self.stdout.write(self.style.SUCCESS(json.dumps(users, indent=2)))
        else:
            self.stdout.write(self.style.ERROR(f"Xatolik: {response.status_code} - {response.text}"))
