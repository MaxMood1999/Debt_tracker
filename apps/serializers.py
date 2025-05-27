from rest_framework import serializers
from apps.models import Contact

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'

class ContactQuerySerializer(serializers.Serializer):
    search = serializers.CharField(required=False, default='', help_text='Search by contact name')
    limit = serializers.IntegerField(required=False, default=50, help_text='Number of contacts to return')
    offset = serializers.IntegerField(required=False, default=0, help_text='Offset for pagination')
