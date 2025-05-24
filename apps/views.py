from django.shortcuts import render
from django.views.generic import DetailView
from rest_framework import generics
from apps.models import Contact
from apps.serializer import ContactSerializer


class ContactRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


class ContactCreateAPIView(generics.CreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

