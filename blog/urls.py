from django.urls import path
from .views import (
    NewsListViews,
    NewsCreateViews,
    NewsDetailViews,HttpRequestPage,
)

app_name = 'blog'

urlpatterns = [
    path('', NewsListViews.as_view(), name='news_list'),
    path('<int:pk>', NewsDetailViews.as_view(), name='news_detail'),
    path('create/', NewsCreateViews.as_view(), name='news_create'),
    path('request/', HttpRequestPage.as_view(), name='news_request'),

]
