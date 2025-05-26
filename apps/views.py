from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.views import APIView
from apps.models import Debt, Contact
from apps.serializers import DebtModelSerializer, ContactUpdateSerializer


@extend_schema(tags=['debt']
               )
class DebtCreateAPIView(CreateAPIView):
    queryset = Debt.objects.all()
    serializer_class = DebtModelSerializer


@extend_schema(tags=['Contact'])
class UpdateContactView(UpdateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactUpdateSerializer