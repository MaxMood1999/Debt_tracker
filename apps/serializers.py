from datetime import date

from rest_framework.exceptions import ValidationError
from rest_framework.fields import SerializerMethodField
from rest_framework.generics import ListAPIView
from rest_framework.serializers import ModelSerializer

from apps.models import Debt


class DebtModelSerializer(ModelSerializer):
    contact_name = SerializerMethodField()
    class Meta:
        model = Debt
        fields = "id",'contact',"contact_name", 'debt_amount', 'description', 'is_my_debt',"created_at", 'due_date', "is_paid_back","is_overdue"

    def get_contact_name(self,obj):
        return obj.contact.name

    def validate_due_date(self, value):
        if value < date.today():
            raise ValidationError("Due date cannot be in the past")
        return value


class ContactDebtModelSerializer(ModelSerializer):
        class Meta:
            model = Debt
            fields = 'contact', "debt_amount", "is_my_debt", "is_paid_back", "is_overdue"









