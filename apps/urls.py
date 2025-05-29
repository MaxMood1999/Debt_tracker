from django.urls import path

from apps.views import DebtCreateAPIView, DebtListAPIView

urlpatterns = [
    path('', DebtCreateAPIView.as_view()),
    path("debt/<int:pk>",DebtListAPIView.as_view(),name="debt-list"),
]