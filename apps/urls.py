from django.urls import path

from apps.views import DebtCreateAPIView, MyDebtAPIView

urlpatterns = [
    path('', DebtCreateAPIView.as_view(), name='debt-create'),
    path('my-debts/', MyDebtAPIView.as_view(), name='my-debts')
]