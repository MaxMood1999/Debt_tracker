from django.urls import path

from apps.views import DebtCreateAPIView, ContactRetrieveAPIView, ContactCreateAPIView

urlpatterns = [
    path('', DebtCreateAPIView.as_view()),
]

urlpatterns += [
    path('contacts/<int:pk>', ContactRetrieveAPIView.as_view()),
    path('contacts/', ContactCreateAPIView.as_view())
]