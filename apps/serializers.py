from datetime import datetime
from rest_framework import serializers
from apps.models import Contact
from rest_framework.exceptions import ValidationError

from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework.authtoken.models import Token
from rest_framework.fields import CharField, IntegerField, BooleanField, SerializerMethodField
from rest_framework.serializers import ModelSerializer
from apps.models import Debt, Contact
from rest_framework.views import APIView

class ContactSerializer(serializers.ModelSerializer):

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
        model = Contact
        fields = '__all__'
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
