from django.db import models

class User(models.Model):
    YEARS = [(str(year), str(year)) for year in range(1990, 2026)]

    # Oylar tanlovi
    MONTHS = [
        ('1', 'Yanvar'), ('2', 'Fevral'), ('3', 'Mart'), ('4', 'Aprel'),
        ('5', 'May'), ('6', 'Iyun'), ('7', 'Iyul'), ('8', 'Avgust'),
        ('9', 'Sentabr'), ('10', 'Oktabr'), ('11', 'Noyabr'), ('12', 'Dekabr')
    ]

    # Kunlar (1-31)
    DAYS = [(str(day), str(day)) for day in range(1, 32)]

    first_name = models.CharField(max_length=16)
    last_name = models.CharField(max_length=16)
    birth_year = models.CharField(max_length=4,choices=YEARS)
    birth_month = models.CharField(max_length=2,choices=MONTHS)
    birth_days = models.CharField(max_length=2,choices=DAYS)
    password = models.CharField(max_length=255)
    

    def __str__(self):
        return self.first_name




