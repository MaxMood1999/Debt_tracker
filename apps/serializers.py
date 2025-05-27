from datetime import date, datetime
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer, CharField, IntegerField, DateField

from apps.models import Debt, Payment

class DebtModelSerializer(ModelSerializer):
    class Meta:
        model = Debt
        fields = ['contact', 'debt_amount', 'description', 'is_my_debt', 'due_date']

    def validate_due_date(self, value):
        if value < datetime.now():
            raise ValidationError("Due date cannot be in the past")
        return value



class PaymentSerializer(ModelSerializer):
    contact_name = CharField(source='debt.contact.name', read_only=True)
    original_debt_id = IntegerField(source='debt.id', read_only=True)

    class Meta:
        model = Payment
        fields = ['id', 'original_debt_id', 'contact_name', 'paid_amount', 'payment_description', 'was_my_debt', 'payment_date']

    def validate_payment_date(self, value):
        if value < date.today():
            raise ValidationError("Payment date cannot be in the past")
        return value