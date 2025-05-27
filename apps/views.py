from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status
from apps.models import Contact, Debt
from apps.serializers import ContactSerializer, DebtModelSerializer


@extend_schema(tags=['contacts'])
class ContactRetrieveAPIView(RetrieveAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        custom_response = {
            "success": True,
            "data": {
                "contact": serializer.data
            }
        }
        return Response(custom_response, status=status.HTTP_200_OK)


@extend_schema(tags=['contacts'])
class ContactCreateAPIView(CreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        custom_response = {
            "success": True,
            "data": {
                "contact": serializer.data
            }
        }
        return Response(custom_response, status=status.HTTP_201_CREATED)


@extend_schema(tags=['debt']
               )
class DebtCreateAPIView(CreateAPIView):
    queryset = Debt.objects.all()
    serializer_class = DebtModelSerializer

