from django.test import TestCase

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
import pytest
from rest_framework.test import APIClient
from apps.models import Debt, Contact, User
from django.utils import timezone
from datetime import timedelta





@pytest.mark.django_db
def test_summary_list_api():
    client = APIClient()

    user = User.objects.create_user(username="testuser", password="12345", email="alisher@gmail.com")

    contact = Contact.objects.create(
        name="Test Contact",
        user=user
    )

    Debt.objects.create(
        contact=contact,
        debt_amount=100,
        is_my_debt=True,
        is_overdue=True,
        due_date=timezone.now() - timedelta(days=1)
    )
    Debt.objects.create(
        contact=contact,
        debt_amount=200,
        is_my_debt=False,
        is_overdue=False,
        due_date=timezone.now() + timedelta(days=10)
    )

    url = reverse("summary-list", kwargs={"pk": contact.id})  # URL name to‘g‘rilansin
    response = client.get(url)

    assert response.status_code == 200
    data = response.json()

    assert data["total_i_owe"] == 100.0
    assert data["total_they_owe"] == 200.0
    assert data["active_debts_count"] == 1
    assert data["overdue_debts_count"] == 1
