from django.urls import path, include
from .views import HomeView,TweetCreateView, TweetRepoView, TweetDeleteView, TweetDetailView, TweetActionView

app_name = 'tweets'

urlpatterns = [
    path('', TweetRepoView.as_view()),
    path('action/', TweetActionView.as_view()),
    path('create/', TweetCreateView.as_view(), name='create'),
    path('<int:tweet_id>/', TweetDetailView.as_view()),
    path('<int:tweet_id>/delete/', TweetDeleteView.as_view()),
    ]