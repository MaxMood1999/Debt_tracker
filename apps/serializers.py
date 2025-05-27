from datetime import datetime

from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework.authtoken.models import Token
from rest_framework.fields import CharField, IntegerField, BooleanField, SerializerMethodField
from rest_framework.serializers import ModelSerializer
from rest_framework.views import APIView


from apps.models import User, Debt


class RegisterSerializer(ModelSerializer):
    password = CharField(max_length=10, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'username']

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            full_name=validated_data['full_name'],
            phone_number=validated_data['phone_number'],
            password=validated_data['password'],
            username=validated_data['username']
        )
        return user

    def to_representation(self, info):
        token, created = Token.objects.get_or_create(user=info)
        return {
            "success": True,
            "data": {
                "user": {
                    "id": info.id,
                    "email": info.email,
                    "full_name": info.full_name,
                    "phone_number": info.phone_number,
                },
                "token": token.key
            }
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

