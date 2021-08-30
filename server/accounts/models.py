from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password):
        user = self.model(
            email=email,
            password=password,
            is_staff=False,
            is_superuser=False,
        )

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password):
        user = self.model(
            email=email,
            password=password,
            is_superuser=True,
            is_staff=True,
        )

        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, db_index=True)
    is_staff = models.BooleanField(
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        default=True,
        help_text=_('Designates whether this user should be treated as active.'),
    )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """Return the full name for the user."""
        return self.email

    def get_short_name(self):
        """Return the short name for the user."""
        return self.email
