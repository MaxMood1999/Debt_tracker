from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.models import Debt
from apps.serializers import DebtModelSerializer

@extend_schema(tags=['debt']
               )
class DebtCreateAPIView(CreateAPIView):
    queryset = Debt.objects.all()
    serializer_class = DebtModelSerializer



class DebtDeleteAPIView(DestroyAPIView):
    queryset = Debt.objects.all()
    serializer_class = DebtModelSerializer
    lookup_field = 'id'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {
                "success": True,
                "message": "Debt record deleted successfully"
            },
            status=status.HTTP_200_OK
        )