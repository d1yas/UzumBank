from django.db import models

# Create your models here

from usersapp.models import User
from datetime import timedelta, date


class Card(models.Model):
    card_holder = models.ForeignKey(User, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=16,unique=True)
    card_pin_code = models.CharField(max_length=4)
    expired_date = models.DateField(auto_now_add=True)
    money = models.FloatField(default=0)

    @property
    def is_expired(self):
        expiration_date = self.expired_date + timedelta(days=5 * 365)  # Add 5 years
        return expiration_date
    @property
    def is_active(self):
        expiration_date = self.expired_date + timedelta(days=5 * 365)
        if expiration_date < date.today():
            return "Eskirgan"
        else:
            return "Active"

