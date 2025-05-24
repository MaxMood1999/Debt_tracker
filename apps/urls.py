from django.urls import path
from apps.views import ContactRetrieveAPIView, ContactCreateAPIView

urlpatterns = [
    path('contacts/<int:pk>', ContactRetrieveAPIView.as_view()),
    path('contacts/', ContactCreateAPIView.as_view())
]