
from rest_framework.serializers import ModelSerializer
from apps.models import Debt




class SummaryModelSerializer(ModelSerializer):
    class Meta:
        model = Debt
        fields = 'contact',"debt_amount","is_my_debt","is_paid_back","is_overdue"