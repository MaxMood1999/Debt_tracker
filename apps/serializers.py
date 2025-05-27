from datetime import datetime
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from apps.models import Debt


class DebtModelSerializer(ModelSerializer):
    class Meta:
        model = Debt
        fields = 'contact', 'debt_amount', 'description', 'is_my_debt', 'due_date',

    def validate_due_date(self, value):
        if value < datetime.now():
            raise ValidationError("Due date cannot be in the past")
        return value


class MyDebtSerializer(serializers.ModelSerializer):
    contact_id = serializers.IntegerField(source='contact.id')
    contact_name = serializers.CharField(source='contact.name')
    debt_description = serializers.CharField(source='description')
    created_date = serializers.DateTimeField(source='created_at')
    days_until_due = serializers.SerializerMethodField()

    class Meta:
        model = Debt
        fields = [
            'id',
            'contact_id',
            'contact_name',
            'debt_amount',
            'debt_description',
            'is_my_debt',
            'created_date',
            'due_date',
            'is_paid_back',
            'is_overdue',
            'days_until_due',
        ]

    def get_days_until_due(self, obj):
        from datetime import date
        if obj.due_date:
            delta = (obj.due_date - date.today()).days
            return max(delta, 0)
        return None
