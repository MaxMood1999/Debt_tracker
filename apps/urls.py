from django.urls import path

from apps.views import DebtCreateAPIView, PaymentListView

urlpatterns = [
    path('', DebtCreateAPIView.as_view()),
    path('payments/my-payments',PaymentListView.as_view())
]