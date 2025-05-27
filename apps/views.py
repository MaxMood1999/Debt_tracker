from datetime import datetime

from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.generics import CreateAPIView
from apps.models import Debt
from apps.serializers import RegisterSerializer, OverdueDebtSerializer

from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView

from apps.models import Contact
from apps.serializers import ContactSerializer


@extend_schema(tags=["Contacts"])
class ContactDeleteView(GenericAPIView):
    serializer_class = ContactSerializer

    def get_queryset(self):
        return Contact.objects.all()

# Create your views here.
from apps.serializers import DebtSerializer, DebtSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Debt
from .serializers import DebtSerializer
from datetime import datetime
@extend_schema(tags=['debt'])
class DebtCreateAPIView(CreateAPIView):
    queryset = Debt.objects.all()
    serializer_class = DebtSerializer

@extend_schema(tags=["Register Post"])
class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user =  serializer.save()
            return Response(serializer.to_representation(user), status=status.HTTP_201_CREATED)
        return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["Debt Overdue"])
class OverdueDebtListApiView(APIView):
    def post(self, request, *args, **kwargs):
        now = datetime.now()
        overdue_debts = Debt.objects.filter(is_paid_back=False, due_date__lte=now)
        serializer = OverdueDebtSerializer(overdue_debts, many=True)
        return  Response({
            "success": True,
            "data": {
                "debts": serializer.data,
            }
        }, status=status.HTTP_200_OK)

class TheirDebtsView(APIView):
    def get(self, request):
        debts = Debt.objects.filter(is_my_debt=False)
        for debt in debts:
            is_overdue = datetime.now() > debt.due_date and not debt.is_paid_back
            if debt.is_overdue != is_overdue:
                debt.is_overdue = is_overdue
                debt.save()
        serializer = DebtSerializer(debts, many=True)
        return Response({
            "success": True,
            "data": {
                "debts": serializer.data
            }
        }, status=status.HTTP_200_OK)
    def delete(self, request, id):
        queryset = self.get_queryset()
        try:
            contact = queryset.get(pk=id)
        except Contact.DoesNotExist:
            return Response({
                "success": False,
                "message": "Contact not found"
            }, status=status.HTTP_404_NOT_FOUND)

        if contact.debts.filter(is_active=True).exists():
            return Response({
                "success": False,
                "message": "Cannot delete contact with active debts"
            }, status=status.HTTP_400_BAD_REQUEST)

        contact.delete()
        return Response({
            "success": True,
            "message": "Contact deleted successfully"
        }, status=status.HTTP_200_OK)

@extend_schema(tags=["Contacts"])
class ContactListView(APIView):
    @extend_schema(
        parameters=[
            OpenApiParameter(name='search', type=str, required=False, description='Search by contact name'),

        ],
        responses={200: ContactSerializer(many=True)}
    )
    def get(self, request):
        search = request.query_params.get('search', '')
        limit = int(request.query_params.get('limit', 50))
        offset = int(request.query_params.get('offset', 0))

        contacts = Contact.objects.filter(name__icontains=search)
        total = contacts.count()
        paginated_contacts = contacts[offset:offset + limit]

        serializer = ContactSerializer(paginated_contacts, many=True)
        return Response({
            'success': True,
            'data': {
                'contacts': serializer.data,
                'total': total
            }
        })

