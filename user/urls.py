from django.contrib.auth import views as acc
from django.urls import path

from user.views import register, verify_email, update_profile_contacts, update_profile_info

app_name = 'user'

urlpatterns = [
    path('register', register, name='register'),
    path('user/verify/', verify_email, name='verify_email'),
    path('profile/update/info', update_profile_info, name='update_user_info'),
    path('profile/update/contacts', update_profile_contacts, name='update_user_profile'),
]

urlpatterns += [
    path('login', acc.LoginView.as_view(), name='login'),
    path('logout', acc.LogoutView.as_view(), name='logout'),
]
