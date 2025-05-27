from datetime import datetime

from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.models import Debt
from apps.serializers import RegisterSerializer, OverdueDebtSerializer


# Create your views here.

@extend_schema(
    tags=["Register Post"],
    request=RegisterSerializer,
    responses={201: RegisterSerializer}
)
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
