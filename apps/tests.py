from django.test import TestCase

# Create your tests here.

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework import status
from datetime import timedelta
from apps.models import Contact, Debt, User
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.urls import reverse

class RegisterUserAPITestCase(APITestCase):
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





class LoginAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='user@example.com',
            username='testuser',
            full_name='Some name',
            password='securePassword123',
            phone_number='+998936160099'
        )
        self.url = reverse('login')

    def test_login_success(self):
        response = self.client.post(self.url, {
            "email": "user@example.com",
            "password": "securePassword123"
        }, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['data']['user']['email'], "user@example.com")
        self.assertIn("token", response.data['data'])

    def test_login_wrong_password(self):
        response = self.client.post(self.url, {
            "email": "user@example.com",
            "password": "wrongPassword"
        }, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.data['success'])
        self.assertIn('errors', response.data)

    def test_login_non_existing_user(self):
        response = self.client.post(self.url, {
            "email": "nouser@example.com",
            "password": "anything"
        }, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.data['success'])
        self.assertIn('errors', response.data)




class OverdueDebtAPITestCase(APITestCase):

    def setUp(self):
        # Create a contact
        self.contact = Contact.objects.create(name="Alice Johnson")

        # Past due (overdue) debt
        self.overdue_debt = Debt.objects.create(
            contact=self.contact,
            debt_amount=200.00,
            description="Borrowed money",
            created_at=timezone.now() - timedelta(days=10),
            due_date=timezone.now() - timedelta(days=5),
            is_my_debt=True,
            is_paid_back=False,
            is_overdue=True
        )

        # Future debt (not overdue)
        self.future_debt = Debt.objects.create(
            contact=self.contact,
            debt_amount=100.00,
            description="Not yet due",
            created_at=timezone.now(),
            due_date=timezone.now() + timedelta(days=5),
            is_my_debt=True,
            is_paid_back=False,
            is_overdue=False
        )

        # Paid debt (not overdue)
        self.paid_debt = Debt.objects.create(
            contact=self.contact,
            debt_amount=150.00,
            description="Already paid",
            created_at=timezone.now(),
            due_date=timezone.now() - timedelta(days=3),
            is_my_debt=False,
            is_paid_back=True,
            is_overdue=False
        )

    def test_get_overdue_debts(self):
        url = '/debts/overdue'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('success', response.data)
        self.assertTrue(response.data['success'])

        debts = response.data['data']['debts']
        self.assertEqual(len(debts), 1)

        debt = debts[0]
        self.assertEqual(debt['contact_name'], "Alice Johnson")
        self.assertEqual(float(debt['debt_amount']), 200.00)
        self.assertEqual(debt['is_paid_back'], False)
        self.assertEqual(debt['is_overdue'], True)
        self.assertLess(debt['days_until_due'], 0)

