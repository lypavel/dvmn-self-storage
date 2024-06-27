from django.contrib.auth import views as acc
from django.urls import path

from user.views import register, verify_email

app_name = 'user'

urlpatterns = [
    path('register', register, name='register'),
    path('user/verify/', verify_email, name='verify_email'),
]

urlpatterns += [
    path('login', acc.LoginView.as_view(), name='login'),
    path('logout', acc.LogoutView.as_view(), name='logout'),
]
