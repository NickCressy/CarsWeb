from django.db import models
from django.contrib.auth.models import User

class Car(models.Model):
    LIST_TYPE_CHOICES = [
        ('owned', 'Owned'),
        ('wanted', 'Wanted'),
    ]

    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    list_type = models.CharField(max_length=10, choices=LIST_TYPE_CHOICES)

    def __str__(self):
        return f"{self.name} ({self.list_type})"