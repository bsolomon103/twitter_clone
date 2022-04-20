"""tweetme URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from tweets.views import HomeView,TweetCreateView, TweetRepoView, TweetDeleteView, TweetDetailView, TweetActionView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='all'),
    #path('create-tweet', TweetCreateView.as_view(), name='create'),
    #path('tweets-repo', TweetRepoView.as_view()),
    #path('tweets/delete/<int:tweet_id>', TweetDeleteView.as_view()),
    path('tweets/<int:tweet_id>', TweetDetailView.as_view()),
    #path('tweets/action', TweetActionView.as_view()),
    path('api/tweets/', include('tweets.urls')),
]
