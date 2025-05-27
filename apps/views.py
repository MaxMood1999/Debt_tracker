from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.models import Debt
from apps.serializers import DebtModelSerializer, MyDebtSerializer


@extend_schema(tags=['Debt']
               )
class DebtCreateAPIView(CreateAPIView):
    queryset = Debt.objects.all()
    serializer_class = DebtModelSerializer


@extend_schema(tags=['Debt'])
class MyDebtAPIView(ListAPIView):
    serializer_class = MyDebtSerializer

    def get_queryset(self):
        return Debt.objects.filter(is_my_debt=True)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "success": True,
            "data": {
                "debts": serializer.data
            }
        })
