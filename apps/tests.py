from django.test import TestCase

# Create your tests here.

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.utils import timezone
from apps.models import User, Contact, Debt, Payment
from decimal import Decimal
from datetime import date

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



class MarkDebtPaidAPIViewTest(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpassword123',
            username=None  # Assuming username is nullable
        )
        # Create a contact for the user
        self.contact = Contact.objects.create(
            user=self.user,
            name='Alice Johnson',
            phone_number='1234567890'
        )
        # Create a debt
        self.debt = Debt.objects.create(
            contact=self.contact,
            debt_amount=Decimal('150.50'),
            description='Lunch at restaurant',
            due_date=date(2024, 2, 15),
            is_my_debt=True,
            is_paid_back=False,
            is_overdue=False
        )
        self.client = APIClient()
        # Authenticate the client
        self.client.force_authenticate(user=self.user)
        self.url = reverse('debt-mark-paid', kwargs={'id': self.debt.id})

    def test_mark_debt_paid_success(self):
        """Test successful marking of a debt as paid."""
        payload = {'payment_description': 'Paid back via bank transfer'}
        response = self.client.put(self.url, payload, format='json')

        # Check response status and content
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['success'], True)
        self.assertIn('data', response.data)
        self.assertIn('debt', response.data['data'])
        self.assertIn('payment_record', response.data['data'])

        # Verify debt fields
        debt_data = response.data['data']['debt']
        self.assertEqual(debt_data['id'], self.debt.id)
        self.assertEqual(debt_data['contact_id'], self.contact.id)
        self.assertEqual(debt_data['contact_name'], 'Alice Johnson')
        self.assertEqual(float(debt_data['debt_amount']), 150.50)
        self.assertEqual(debt_data['description'], 'Lunch at restaurant')
        self.assertEqual(debt_data['is_my_debt'], True)
        self.assertEqual(debt_data['due_date'], '2024-02-15')
        self.assertTrue(debt_data['is_paid_back'])
        self.assertIsNotNone(debt_data['paid_back_date'])

        # Verify payment record
        payment_data = response.data['data']['payment_record']
        self.assertEqual(float(payment_data['paid_amount']), 150.50)
        self.assertEqual(payment_data['payment_description'], 'Paid back via bank transfer')
        self.assertIsNotNone(payment_data['payment_date'])

        # Verify database updates
        debt = Debt.objects.get(id=self.debt.id)
        self.assertTrue(debt.is_paid_back)
        self.assertIsNotNone(debt.paid_back_date)
        payment = Payment.objects.get(debt=debt)
        self.assertEqual(payment.paid_amount, Decimal('150.50'))
        self.assertEqual(payment.payment_description, 'Paid back via bank transfer')

    def test_mark_debt_paid_unauthenticated(self):
        """Test unauthenticated request returns 401."""
        self.client.force_authenticate(user=None)  # Remove authentication
        payload = {'payment_description': 'Paid back via bank transfer'}
        response = self.client.put(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['success'], False)
        self.assertEqual(response.data['error'], 'Authentication required')

    def test_mark_debt_paid_non_existent(self):
        """Test marking a non-existent debt returns 404."""
        url = reverse('debt-mark-paid', kwargs={'id': 999})
        payload = {'payment_description': 'Paid back via bank transfer'}
        response = self.client.put(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['success'], False)
        self.assertEqual(response.data['error'], 'Debt not found or not authorized')

    def test_mark_debt_paid_already_paid(self):
        """Test marking an already paid debt returns 400."""
        self.debt.is_paid_back = True
        self.debt.paid_back_date = timezone.now()
        self.debt.save()
        payload = {'payment_description': 'Paid back via bank transfer'}
        response = self.client.put(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['success'], False)
        self.assertEqual(response.data['error'], 'Debt is already paid')

    def test_mark_debt_paid_invalid_data(self):
        """Test invalid request data returns 400."""
        payload = {}  # Missing payment_description
        response = self.client.put(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['success'], False)
        self.assertIn('payment_description', response.data['error'])