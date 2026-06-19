from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('application/', views.ApplicationCreateView.as_view(), name='application'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('', views.UserLoginView.as_view(), name='home'),
]