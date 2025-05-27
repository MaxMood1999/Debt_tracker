from datetime import datetime

from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.generics import CreateAPIView
from apps.models import Debt
from apps.serializers import RegisterSerializer, OverdueDebtSerializer


# Create your views here.
from apps.serializers import DebtModelSerializer, DebtSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Debt
from .serializers import DebtSerializer
from datetime import datetime
@extend_schema(tags=['debt'])
class DebtCreateAPIView(CreateAPIView):
    queryset = Debt.objects.all()
    serializer_class = DebtModelSerializer

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
