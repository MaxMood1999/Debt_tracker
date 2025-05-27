from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.models import Debt
from apps.serializers import RegisterSerializer, OverdueDebtSerializer, LoginSerializer
from apps.serializers import DebtModelSerializer, MyDebtSerializer


@extend_schema(tags=['Debt']
               )
class DebtCreateAPIView(CreateAPIView):
    queryset = Debt.objects.all()
    serializer_class = DebtModelSerializer

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


@extend_schema(
    tags=["Login"],
    request=LoginSerializer,
    responses={200: {
        "type": "object",
        "properties": {
            "success": {"type": "boolean"},
            "data": {
                "type": "object",
                "properties": {
                    "user": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "integer"},
                            "email": {"type": "string"},
                            "full_name": {"type": "string"},
                        }
                    },
                    "token": {"type": "string"},
                }
            }
        }
    }}
)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "success": True,
                "data": {
                    "user": {
                        "id": user.id,
                        "email": user.email,
                        "full_name": user.full_name,
                    },
                    "token": token.key
                }
            }, status=status.HTTP_200_OK)

        return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
@extend_schema(tags=['Debt'])
class MyDebtAPIView(ListAPIView):
    serializer_class = MyDebtSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Debt.objects.filter(is_my_debt=True, contact__user=self.request.user).order_by('-created_at')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "success": True,
            "data": {
                "debts": serializer.data
            }
        })
