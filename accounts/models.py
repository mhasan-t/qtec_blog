from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator
from django.db import models


class User(AbstractUser):
    full_name = models.CharField(
        verbose_name="Full Name", max_length=255, null=False)

    # user_type : 0 = Admin, 1 = Author, 2 = Normal Users
    user_type = models.IntegerField(
        default=2, validators=[MaxValueValidator(3)])

    REQUIRED_FIELDS = ['full_name', 'email']

    def __str__(self) -> str:
        return f'{self.full_name} - {self.email} ({self.username})'
