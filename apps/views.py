from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Payment
from .serializers import PaymentSerializer

@extend_schema(tags=['payment'])
class TheirPaymentsView(APIView):
    serializer_class = PaymentSerializer
    def get(self, request):
        payments = Payment.objects.all()
        serializer = PaymentSerializer(payments, many=True)
        return Response({
            "success": True,
            "data": {
                "payments": serializer.data
            }
        },)


