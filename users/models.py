import random

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser


def generate_random_number():
    return random.randint(1, 100)


class CustomUser(AbstractUser):
    """Custom user model."""

    email = models.EmailField(unique=True, blank=False, max_length=70)
    birth_date = models.DateField(null=True, blank=False)
    random_number = models.IntegerField(default=generate_random_number)

    def get_absolute_url(self):
        return reverse('user_details',
                       args=[str(self.username)])
