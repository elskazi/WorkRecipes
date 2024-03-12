from django.urls import path
from .views import (
    NewsListViews,NewsCreateViews,NewsDetailViews,
    HttpRequestPage, NewsByCategoryListView
)

app_name = 'blog'

urlpatterns = [
    path('', NewsListViews.as_view(), name='news_list'),
    path('<str:slug>', NewsDetailViews.as_view(), name='news_details'),
    path('category/<str:slug>/', NewsByCategoryListView.as_view(), name='news_by_category' ),
    path('create/', NewsCreateViews.as_view(), name='news_create'),
    path('request/', HttpRequestPage.as_view(), name='news_request'),

]
