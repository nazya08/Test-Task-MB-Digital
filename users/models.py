from django.db import models
from django.contrib.auth.models import AbstractUser

from users.managers import CustomUserManager


class User(AbstractUser):
    username = models.CharField(
        'Username', max_length=64, unique=True, null=True, blank=True
    )
    email = models.EmailField('Email', unique=True, null=True, blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return f'{self.full_name} ({self.pk})'
