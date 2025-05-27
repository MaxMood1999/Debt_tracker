from django.test import TestCase

# Create your tests here.

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

class RegisterUserAPITestCase(APITestCase):0
    def setUp(self):
        self.url = reverse('auth-register')
        self.user_data = {
            "email": "user@example.com",
            "password": "password",
            "full_name": "example_username",
            "phone_number": "+998901234567"
        }

    def test_register_user_successfully(self):
        response = self.client.post(self.url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("token", response.data["data"])
        self.assertEqual(response.data["data"]["user"]["email"], self.user_data["email"])
        self.assertEqual(response.data["data"]["user"]["full_name"], self.user_data["full_name"])
        self.assertEqual(response.data["data"]["user"]["phone_number"], self.user_data["phone_number"])


from django.test import TestCase
from django.utils import timezone
from decimal import Decimal
from apps.models import Debt, Contact, User  # apps.User ni import qilamiz


class DebtModelTest(TestCase):
    def setUp(self):

        self.user = User.objects.create(
            username='testuser',
            email='test@example.com',

        )


        self.contact = Contact.objects.create(
            user=self.user,
            name="John Doe",
            phone_number="1234567890"
        )


        self.debt = Debt.objects.create(
            contact=self.contact,
            debt_amount=Decimal('1000.50'),
            description="Test debt",
            due_date=timezone.now() + timezone.timedelta(days=10),
            is_my_debt=True,
            is_paid_back=False,
            is_overdue=False
        )

    def test_debt_creation(self):

        debt = Debt.objects.get(id=self.debt.id)
        self.assertEqual(debt.contact, self.contact)
        self.assertEqual(debt.debt_amount, Decimal('1000.50'))
        self.assertEqual(debt.description, "Test debt")
        self.assertTrue(debt.created_at)
        self.assertEqual(debt.is_my_debt, True)
        self.assertEqual(debt.is_paid_back, False)
        self.assertEqual(debt.is_overdue, False)

    def test_contact_foreign_key(self):

        debt = Debt.objects.get(id=self.debt.id)
        self.assertEqual(debt.contact.name, "John Doe")

        self.contact.delete()
        self.assertFalse(Debt.objects.filter(id=self.debt.id).exists())

    def test_debt_amount_decimal(self):

        debt = Debt.objects.get(id=self.debt.id)
        self.assertEqual(debt.debt_amount, Decimal('1000.50'))
        self.assertIsInstance(debt.debt_amount, Decimal)

    def test_description_max_length(self):

        max_length = Debt._meta.get_field('description').max_length
        self.assertEqual(max_length, 255)

    def test_due_date_and_overdue(self):

        overdue_debt = Debt.objects.create(
            contact=self.contact,
            debt_amount=Decimal('500.75'),
            description="Overdue debt",
            due_date=timezone.now() - timezone.timedelta(days=1),
            is_my_debt=False,
            is_paid_back=False,
            is_overdue=True
        )
        self.assertTrue(overdue_debt.is_overdue)
        self.assertLess(overdue_debt.due_date, timezone.now())

    def test_default_values(self):

        debt = Debt.objects.create(
            contact=self.contact,
            debt_amount=Decimal('200.00'),
            description="Default values debt",
            due_date=timezone.now() + timezone.timedelta(days=5)
        )
        self.assertFalse(debt.is_my_debt)
        self.assertFalse(debt.is_paid_back)
        self.assertFalse(debt.is_overdue)
    def test_string_representation(self):
        """Debt ob'ektining string ko'rinishini tekshirish"""
        debt = Debt.objects.get(id=self.debt.id)
        expected_str = f"Debt object ({debt.id})"  # Haqiqiy string ko'rinishiga moslashtirildi
        self.assertEqual(str(debt), expected_str)