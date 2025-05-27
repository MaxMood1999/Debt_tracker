from drf_spectacular.utils import extend_schema
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status
from apps.models import Contact, Debt
from apps.serializers import ContactSerializer, DebtModelSerializer


@extend_schema(tags=['Contacts'])
class ContactRetrieveAPIView(RetrieveAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def get_object(self):
        try:
            return super().get_object()
        except NotFound:
            raise NotFound(detail={
                "success": False,
                "message": "Contact not found",
                "error_code": "CONTACT_NOT_FOUND"
            })

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            "success": True,
            "data": {
                "contact": serializer.data
            }
        }, status=status.HTTP_200_OK)


@extend_schema(tags=['Contacts'])
class ContactCreateAPIView(CreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as exc:
            return Response({
                "success": False,
                "message": "Validation failed",
                "error_code": "VALIDATION_FAILED",
                "errors": exc.detail
            }, status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)
        return Response({
            "success": True,
            "data": {
                "contact": serializer.data
            }
        }, status=status.HTTP_201_CREATED)


@extend_schema(tags=['debt'])
class DebtCreateAPIView(CreateAPIView):
    queryset = Debt.objects.all()
    serializer_class = DebtModelSerializer

