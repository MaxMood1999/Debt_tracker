from datetime import datetime
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import (ModelSerializer, Serializer, CharField,
                                        IntegerField, JSONField,
                                        BooleanField, DictField, DateTimeField,
                                        DateField)
from apps.models import Debt, Payment


class DebtModelSerializer(ModelSerializer):
    class Meta:
        model = Debt
        fields = 'contact', 'debt_amount', 'description', 'is_my_debt', 'due_date',

    def validate_due_date(self, value):
        if value < datetime.now():
            raise ValidationError("Due date cannot be in the past")
        return value


class PaymentSerializer(ModelSerializer):
    payment_date = DateTimeField(format='%Y-%m-%dT%H:%M:%SZ', read_only=True)

    class Meta:
        model = Payment
        fields = ['id', 'paid_amount', 'payment_description', 'payment_date']

class DebtSerializer(ModelSerializer):
    contact_name = CharField(source='contact.name', read_only=True)
    contact_id = IntegerField(source='contact.id', read_only=True)
    created_at = DateTimeField(read_only=True)
    due_date = DateField(read_only=True)  # CHANGED!
    paid_back_date = DateTimeField(read_only=True, allow_null=True)

    class Meta:
        model = Debt
        fields = ['id', 'contact_id', 'contact_name', 'debt_amount', 'description',
                  'is_my_debt', 'created_at', 'due_date', 'is_paid_back', 'paid_back_date']


class MarkPaidRequestSerializer(Serializer):
    payment_description = CharField(max_length=255)

class MarkPaidResponseSerializer(Serializer):
    success = BooleanField(default=True)
    data = DictField(child=JSONField())

    def create(self, validated_data):
        return validated_data