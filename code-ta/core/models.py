"""
Database models.
"""
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

import uuid

class UserManager(BaseUserManager):
    """Manager for users"""

    def create_user(self, name, password=None, **extra_fields):
        """Create, save and return a new user"""
        if not name:
            raise ValueError('User must have a name.')

        user = self.model(name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, name, password):
        """Create and return a new superuser."""
        user = self.create_user(name, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user

class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=200)
    utorid = models.CharField(max_length=10)
    user_role = models.CharField(max_length=2)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'user_id'

    def __str__(self):
        return f"User(user_id={self.user_id}, name={self.name}, utorid={self.utorid}, user_role={self.user_role}"
    
    class Meta:
        indexes = [
            models.Index(fields=['user_id'], name='user_id_idx'),
            models.Index(fields=['utorid'], name='utorid_idx'),
        ]
