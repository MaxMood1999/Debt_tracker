from django.urls import path

from apps.views import RegisterView, OverdueDebtListApiView
from apps.views import DebtCreateAPIView

urlpatterns = [
    path('auth/register', RegisterView.as_view(), name='auth-register'),
    path("debts/overdue", OverdueDebtListApiView.as_view(), name="debt-overdue"),

    path('', DebtCreateAPIView.as_view()),
]