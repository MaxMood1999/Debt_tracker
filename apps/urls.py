from django.urls import path

from apps.views import DebtCreateAPIView, DebtDeleteAPIView

urlpatterns = [
    path('', DebtCreateAPIView.as_view()),

    path('debt/delete/<int:id>/', DebtDeleteAPIView.as_view(), name='debt-delete'),
]
