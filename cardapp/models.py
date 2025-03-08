from django.db import models
from usersapp.models import User
from datetime import timedelta, date


class Card(models.Model):
    card_holder = models.ForeignKey(User, on_delete=models.CASCADE,related_name='cardholder')
    # one = models.OneToOneField(User, on_delete=models.CASCADE,related_name='one')
    card_number = models.CharField(max_length=16, unique=True)
    card_pin_code = models.CharField(max_length=4)
    expired_date = models.DateField()  # auto_now_add olib tashlandi
    money = models.FloatField(default=0)

    def save(self, *args, **kwargs):
        if not self.expired_date:
            self.expired_date = date.today() + timedelta(days=5 * 365)  # 5 yil qo‘shish
        super().save(*args, **kwargs)

    @property
    def is_expired(self):
        return date.today() > self.expired_date  # True yoki False qaytaradi

    @property
    def is_active(self):
        return not self.is_expired  # True bo‘lsa, aktiv


class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    courses = models.ManyToManyField(Course, related_name='students')

    def __str__(self):
        return self.user.username


