from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin
)

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True,
                                null=False, blank=False)
    contacts = models.ManyToManyField('self')
    avatar = models.ImageField(upload_to='avatars', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    @property
    def is_staff(self):
        return self.is_admin
