from datetime import datetime
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer
from apps.models import Debt, Contact

class DebtModelSerializer(ModelSerializer):
    class Meta:
        model = Debt
        fields = 'contact', 'debt_amount', 'description', 'is_my_debt', 'due_date',

    def validate_due_date(self, value):
        if value < datetime.now():
            raise ValidationError("Due date cannot be in the past")
        return value


class DebtSerializer(serializers.ModelSerializer):
    contact_id = serializers.IntegerField(source='contact.id')
    contact_name = serializers.CharField(source='contact.name')
    days_until_due = serializers.SerializerMethodField()

    def get_days_until_due(self, obj):
        if obj.is_paid_back:
            return 0
        delta = obj.due_date - datetime.now()
        return delta.days

    class Meta:
        model = Debt
        fields = [
            'id', 'contact_id', 'contact_name', 'debt_amount', 'description',
            'is_my_debt', 'created_at', 'due_date', 'is_paid_back',
            'is_overdue', 'days_until_due'
        ]
