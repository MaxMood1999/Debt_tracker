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

