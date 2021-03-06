from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('user/<str:username>/', views.profile_view, name='profile'),
    path('user/update/<str:username>/', views.profile_edit, name='edit-profile'),
    path('user/delete/<str:username>/', views.user_delete, name='user-delete'),
]