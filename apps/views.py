from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from apps.models import Debt, Payment
from apps.serializers import (DebtModelSerializer, MarkPaidRequestSerializer,
                              MarkPaidResponseSerializer, DebtSerializer,
                              PaymentSerializer)

@extend_schema(tags=['debt']
               )
class DebtCreateAPIView(CreateAPIView):
    queryset = Debt.objects.all()
    serializer_class = DebtModelSerializer


@extend_schema(tags=['debt'])
class MarkDebtPaidAPIView(APIView):
    @extend_schema(
        request=MarkPaidRequestSerializer,
        responses={200: MarkPaidResponseSerializer}
    )
    def put(self, request, id):
        # Check if user is authenticated
        if not request.user.is_authenticated:
            return Response(
                {"success": False, "error": "Authentication required"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        try:
            # Fetch the debt, ensuring it belongs to the authenticated user
            debt = Debt.objects.get(id=id, contact__user=request.user)
        except Debt.DoesNotExist:
            return Response(
                {"success": False, "error": "Debt not found or not authorized"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Check if debt is already paid
        if debt.is_paid_back:
            return Response(
                {"success": False, "error": "Debt is already paid"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validate request data
        serializer = MarkPaidRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"success": False, "error": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Update debt
        debt.is_paid_back = True
        debt.paid_back_date = timezone.now()
        debt.save()

        # Create payment record
        payment = Payment.objects.create(
            debt=debt,
            paid_amount=debt.debt_amount,
            payment_description=serializer.validated_data['payment_description']
        )

        # Prepare response
        debt_data = DebtSerializer(debt).data
        payment_data = PaymentSerializer(payment).data
        response_data = {
            "success": True,
            "data": {
                "debt": debt_data,
                "payment_record": payment_data
            }
        }

        return Response(response_data, status=status.HTTP_200_OK)