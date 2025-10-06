# accounts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/admin/', views.admin_dashboard_view, name='admin_dashboard'),
    path('dashboard/distributor/', views.distributor_dashboard_view, name='distributor_dashboard'),
    path('password-reset/', views.password_reset_request_view, name='password_reset_request'),
    path('password-reset/otp/', views.password_reset_otp_view, name='password_reset_otp'),

]

