from django.urls import path

urlpatterns = [
    path('auth/register', RegisterView.as_view(), name='auth-register'),

]