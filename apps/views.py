import logging
from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.models import Debt, Payment
from apps.serializers import DebtModelSerializer, PaymentSerializer

logger = logging.getLogger(__name__)

@extend_schema(tags=['debt'])
class DebtCreateAPIView(CreateAPIView):
    queryset = Debt.objects.all()
    serializer_class = DebtModelSerializer





@extend_schema(tags=['payment'])
class PaymentListView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentSerializer

    def get(self, request):
        payments = Payment.objects.filter(debt__contact__user=request.user)
        for payment in payments:
            logger.debug(f"Payment ID: {payment.id}, payment_date: {payment.payment_date}, type: {type(payment.payment_date)}")
        serializer = PaymentSerializer(payments, many=True)
        return Response({
            "success": True,
            "data": {
                "payments": serializer.data
            }
        }, status=status.HTTP_200_OK)