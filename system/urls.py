from django.urls import path

from .views import (ProfileUpdateView, ProfileDetailView, ProfileListView,
                    UserRegisterView, UserLoginView, UserLogoutView)

app_name = 'system'

urlpatterns = [

    path('user/edit/', ProfileUpdateView.as_view(), name='profile_edit'),
    path('user/list/', ProfileListView.as_view(), name='profile_list'),
    path('user/<str:slug>/', ProfileDetailView.as_view(), name='profile_detail'),

    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),

]
