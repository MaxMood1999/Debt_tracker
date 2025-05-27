from django.urls import path
from apps.views import ContactDeleteView, ContactListView

urlpatterns = [
    path('contacts/<int:id>', ContactDeleteView.as_view(), name='delete-contact'),
    path('contacts/', ContactListView.as_view(), name='contact-list'),
]
