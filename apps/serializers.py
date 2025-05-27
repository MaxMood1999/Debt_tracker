from datetime import datetime

from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework.fields import CharField, IntegerField, BooleanField, SerializerMethodField
from datetime import datetime

from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from apps.models import User, Debt
from apps.models import Debt


class DebtModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password',  "username"]
        model = Debt
        fields = 'contact', 'debt_amount', 'description', 'is_my_debt', 'due_date',

    def validate_due_date(self, value):
        if value < datetime.now():
            raise ValidationError("Due date cannot be in the past")
        return value


        }


class OverdueDebtSerializer(ModelSerializer):
    contact_id = IntegerField(source='contact_id')
    contact_name = CharField(source='contact_name')
    is_overdue = BooleanField(source='is_overdue')
    days_until_due = SerializerMethodField()
    class Meta:
        model = Debt
        fields = ['id', 'contact_id', 'contact_name',
                  'debt_amount', 'is_overdue', 'days_until_due',
                  'description', 'is_my_debt', 'created_at', 'due_date',
                  'is_paid_back'

        ]
    def get_is_overdue(self, obj):
        return not obj.is_paid_back and obj.due_date < datetime.now(obj.due_date.tzinfo)

    def get_days_until_due(self, obj):
        difference_time = obj.due_date - datetime.now(obj.due_date.tzinfo)
        return difference_time.days

