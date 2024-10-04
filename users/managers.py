from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email=None, password=None, username=None, **extra_fields):
        if not (email or username):
            raise ValidationError('Please provide either an email or username.')

        if email:
            email = self.normalize_email(email)
            if self.model.objects.filter(email=email).exists():
                raise ValidationError('A user with this email already exists.')

        if username and self.model.objects.filter(username=username).exists():
            raise ValidationError('A user with this username already exists.')

        if not username:
            if email:
                username = email.split('@')[0]

        user = self.model(username=username, **extra_fields)
        if email:
            user.email = email

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, username=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_active', True)

        return self._create_user(
            email, password, username, **extra_fields
        )

    def create_superuser(self, email=None, password=None, username=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)

        return self._create_user(
            email, password, username, **extra_fields
        )
