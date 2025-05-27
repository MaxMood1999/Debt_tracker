from apps.views import DebtCreateAPIView, TheirDebtsView
from django.urls import path

from apps.views import RegisterView, OverdueDebtListApiView


urlpatterns = [
    path('auth/register', RegisterView.as_view(), name='auth-register'),
    path("debts/overdue", OverdueDebtListApiView.as_view(), name="debt-overdue"),


]

urlpatterns += [
    path('debts/their-debts', TheirDebtsView.as_view(), name='their-debts'),
]

