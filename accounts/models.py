
# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # We don't need to add username, password, email, etc.
    # AbstractUser already has them.

    USER_TYPE_CHOICES = (
        ('admin', 'Admin'),
        ('distributor', 'Distributor'),
    )

    # Our custom field
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='distributor')

    def __str__(self):
        return self.username
