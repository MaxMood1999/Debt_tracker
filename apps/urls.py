from django.urls import path
from apps.views import DebtCreateAPIView, MarkDebtPaidAPIView

urlpatterns = [
    path('', DebtCreateAPIView.as_view()),
    path('debts/<int:id>/mark-paid', MarkDebtPaidAPIView.as_view(), name='debt-mark-paid'),
]