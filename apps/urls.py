from django.urls import path
from .views import TheirPaymentsView

urlpatterns = [
    path('payments/their-payments', TheirPaymentsView.as_view()),
]
