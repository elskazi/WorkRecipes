from django.urls import path
from .views import (
    NewsListViews, NewsCreateViews, NewsUpdateView, NewsDetailViews, NewsDeleteView,
    HttpRequestPage, NewsByCategoryListView, CommentCreateView, NewsByTagListView
)

app_name = 'blog'

urlpatterns = [
    path('', NewsListViews.as_view(), name='news_list'),
    path('news/create/', NewsCreateViews.as_view(), name='news_create'),
    path('news/<str:slug>/', NewsDetailViews.as_view(), name='news_details'),
    path('news/<str:slug>/update/', NewsUpdateView.as_view(), name='news_update'),
    path('news/<str:slug>/delete/', NewsDeleteView.as_view(), name='news_delete'),
    path('category/<str:slug>/', NewsByCategoryListView.as_view(), name='news_by_category'),
    path('news/<int:pk>/comments/create/', CommentCreateView.as_view(), name='comment_create_view'),
    path('news/tags/<str:tag>/', NewsByTagListView.as_view(), name='news_by_tags'),

    path('request/', HttpRequestPage.as_view(), name='news_request'),

]
