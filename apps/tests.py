

import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from apps.models import Debt, Contact, User


@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def debt():
    user = User.objects.create(
        id = 1,
        password=1,
        is_superuser=False,
        is_staff=True,
        is_active=True,
        balance=0,
        email="aa@gmail.com"
    )
    contact = Contact.objects.create(
        id = 1,
        name = "Ali",
        phone_number = "90239023",
        user = user
    )

    return Debt.objects.create(
     debt_amount = 120 ,
     description = "ksmlkerelrme",
     is_my_debt = True,
     is_paid_back = True,
     is_overdue = True,
     contact = contact,
     due_date = "2025-12-12"
    )

class TestDebtList:
    @pytest.mark.django_db
    def test_debt_list(self,client,debt):
        url = reverse("debt-list", kwargs={'pk': 1})
        response = client.get(url)
        assert response.status_code == 200
        results = response.data[0].get("data").get("debts")
        assert float(results["debt_amount"]) == float(debt.debt_amount)
        assert results["description"] == debt.description
        assert results["is_my_debt"] == debt.is_my_debt
        assert results["is_paid_back"] == debt.is_paid_back
        assert results["contact"] == debt.contact.id
        assert results["due_date"] == debt.due_date

