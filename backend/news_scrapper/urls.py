from django.urls import path
from .views import fetch_news, get_news, update_news_bias

urlpatterns = [
    path('scrape/', fetch_news, name="fetch_news"),
    path('news/', get_news, name="get_news"),
    path('news/<int:id>/update_bias/', update_news_bias, name="update_news_bias"),
]
