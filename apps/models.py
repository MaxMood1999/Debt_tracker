from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.db.models import CharField, Model, ForeignKey, CASCADE, DateField
from django.db.models.fields import DecimalField, DateTimeField, BooleanField




class CustomUserManager(UserManager):
    def _create_user_object(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given username must be set")
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.


        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        return user

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email, email, and password.
        """
        user = self._create_user_object(email, password, **extra_fields)
        user.save(using=self._db)
        return user

    async def _acreate_user(self, email, password, **extra_fields):
        """See _create_user()"""
        user = self._create_user_object(email, password, **extra_fields)
        await user.asave(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    create_user.alters_data = True

    async def acreate_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return await self._acreate_user(username, email, password, **extra_fields)

    acreate_user.alters_data = True

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user( email, password, **extra_fields)

    create_superuser.alters_data = True

    async def acreate_superuser(
        self, email, password=None, **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return await self._acreate_user( email, password, **extra_fields)

    acreate_superuser.alters_data = True

class User(AbstractUser):
    balance = DecimalField(max_digits=10, decimal_places=2, default=0)
    USERNAME_FIELD = 'email'
    email = CharField(max_length=255, unique=True)
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

class Contact(Model):
    user = ForeignKey('apps.User', on_delete=CASCADE)
    name = CharField(max_length=255)
    phone_number = CharField(max_length=255)
    created_at = DateTimeField(auto_now_add=True)

class Debt(Model):
    contact = ForeignKey('apps.Contact', on_delete=CASCADE)
    debt_amount = DecimalField(max_digits=10, decimal_places=2)
    description = CharField(max_length=255)
    created_at = DateTimeField(auto_now_add=True)
    due_date = DateField()
    is_my_debt = BooleanField(default=False)
    is_paid_back = BooleanField(default=False)
    paid_back_date = DateTimeField(null=True, blank=True)
    is_overdue = BooleanField(default=False)


class Payment(models.Model):
    debt = ForeignKey('apps.Debt', on_delete=CASCADE, related_name='payments')
    paid_amount = DecimalField(max_digits=10, decimal_places=2)
    payment_description = CharField(max_length=255)
    payment_date = DateTimeField(auto_now_add=True)