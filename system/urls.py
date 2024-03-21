from django.urls import path

from .views import (ProfileUpdateView, ProfileDetailView, ProfileListView,
                    UserRegisterView, UserLoginView, UserLogoutView, UserPasswordChangeView)

app_name = 'system'

urlpatterns = [

    path('user/list/', ProfileListView.as_view(), name='profile_list'),
    path('user/<str:slug>/', ProfileDetailView.as_view(), name='profile_detail'),
    path('user/<str:slug>/edit/', ProfileUpdateView.as_view(), name='profile_edit'),

    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(redirect_authenticated_user=True,), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),

    path('password-change/', UserPasswordChangeView.as_view(), name='password_change'),

]
