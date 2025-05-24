from django.contrib.auth import get_user_model
from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from apps.models import User


class RegisterSerializer(ModelSerializer):
    password = CharField(max_length=10, write_only=True)
    class Meta:
        model = User
        fields = ['email', 'password', 'full_name', 'phone_number', "username"]

    def create(self, validated_data):
        user = User.objects.create_user(
            email = validated_data['email'],
            full_name = validated_data['full_name'],
            phone_number = validated_data['phone_number'],
            password = self.validated_data['password'],
            username = self.validated_data['username']
        )
        return user
    def present(self, info):
        token = RefreshToken.for_user(info)
        return {
            "success": True,
            "data" : {
                "user" : {
                    "id": info.id,
                    "email": info.email,
                    "full_name": info.full_name,
                    "phone_number": info.phone_number,

                },
                "token": str(token.access_token)
            }

        }