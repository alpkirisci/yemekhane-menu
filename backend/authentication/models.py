from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

# Custom User model
class User(AbstractUser):
    tshirt_color = models.CharField(max_length=50)

    def __str__(self):
        return self.username