# users/urls.py
from django.urls import path

from apps.views import SummaryListAPIView


urlpatterns = [
      path("summary/list<int:pk>",SummaryListAPIView.as_view(),name="summary-list"),
]
