from django.urls import path

from .views import ProfileUpdateView, ProfileDetailView, ProfileListView

app_name = 'system'

urlpatterns = [

    path('user/edit/', ProfileUpdateView.as_view(), name='profile_edit'),
    path('user/list/', ProfileListView.as_view(), name='profile_list'),
    path('user/<str:slug>/', ProfileDetailView.as_view(), name='profile_detail'),

]
