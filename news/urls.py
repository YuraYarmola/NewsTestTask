from django.urls import path
from .views import TrendingNewsView

urlpatterns = [
    path('api/trending-news/', TrendingNewsView.as_view(), name='trending-news'),
]
