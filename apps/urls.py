from django.urls import path
from apps.views import UpdateContactView

urlpatterns = [
    path('contact-update/<int:id>', UpdateContactView.as_view(), name='contact-update'),
]
