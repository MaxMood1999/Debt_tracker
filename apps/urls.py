from django.urls import path

from apps.views import DebtCreateAPIView, DebtListAPIView, ContactDebtListAPIView

urlpatterns = [
    path('', DebtCreateAPIView.as_view()),
    path("debt/<int:pk>",DebtListAPIView.as_view(),name="debt-list"),
    path("contact/debt/<int:pk>",ContactDebtListAPIView.as_view())
]
