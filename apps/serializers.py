from datetime import date

from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from apps.models import Debt


class DebtModelSerializer(ModelSerializer):
    class Meta:
        model = Debt
        fields = 'contact', 'debt_amount', 'description', 'is_my_debt', 'due_date',

    def validate_due_date(self, value):
        if value < date.today():
            raise ValidationError("Due date cannot be in the past")
        return value

