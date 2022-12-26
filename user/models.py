from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
# Helper class to create a user
class UserManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, password=None):
        if not email:
            raise ValueError("User must have an email address")

        if not username:
            raise ValueError("User must have an username")
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            username=username,
        )

        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, email, username, first_name, last_name, password):
        user = self.create_user(
            email,
            password=password,
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=255, unique=True, verbose_name="email")
    phone_no = models.CharField(max_length=30, null=True, blank=True)

    # Required
    date_joined = models.DateField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    objects = UserManager()
    # Useful when logging with email in django admin
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "username",
        "first_name",
        "last_name",
    ]  # removes email from REQUIRED_FIELDS

    def __str__(self):
        return self.email

    def has_perm(self, perm, object=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True
