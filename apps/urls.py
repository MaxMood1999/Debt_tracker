from django.urls import path

from apps.views import RegisterView, OverdueDebtListApiView, LoginView
from apps.views import DebtCreateAPIView, MyDebtAPIView

urlpatterns = [
    path('auth/register', RegisterView.as_view(), name='auth-register'),
    path("debts/overdue", OverdueDebtListApiView.as_view(), name="debt-overdue"),
    path('auth/login', LoginView.as_view(), name='login')

    path('', DebtCreateAPIView.as_view(), name='debt-create'),
    path('my-debts/', MyDebtAPIView.as_view(), name='my-debts')
]