from apps.views import DebtCreateAPIView, TheirDebtsView
from django.urls import path
urlpatterns = [
    path('', DebtCreateAPIView.as_view()),
]

urlpatterns += [
    path('debts/their-debts', TheirDebtsView.as_view(), name='their-debts'),
]

