# from django.db import models
#
# # Create your models here.
#
#
# class UzumUser(models.Model):
#     name = models.CharField(max_length=32)
#     surname = models.CharField(max_length=32)
#     age = models.IntegerField()
#     email = models.EmailField()
#     phone = models.IntegerField(unique=True)
#
#
#
#     def __str__(self):
#         return self.name
# from django.db import models
#
# class User(models.Model):
#     username = models.CharField(max_length=100, unique=True)
#     password = models.CharField(max_length=255)
#     last_name = models.CharField(max_length=100, blank=True, null=True)  # Yangi maydon
#
#     def __str__(self):
#         return self.username




from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.username




