from django.urls import path

from apps.views import DebtCreateAPIView

urlpatterns = [
    path('', DebtCreateAPIView.as_view()),
]