from rest_framework import generics
from apps.models import Contact
from apps.serializer import ContactSerializer


class ContactRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView

from apps.models import Debt
from apps.serializers import DebtModelSerializer

class ContactCreateAPIView(generics.CreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

@extend_schema(tags=['debt']
               )
class DebtCreateAPIView(CreateAPIView):
    queryset = Debt.objects.all()
    serializer_class = DebtModelSerializer

