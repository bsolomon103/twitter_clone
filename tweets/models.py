from django.db import models
import random
from django.conf import settings

User = settings.AUTH_USER_MODEL

class TweetLikes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    tweet = models.ForeignKey('Tweet', on_delete=models.CASCADE)
    time_stamp = models.DateTimeField(auto_now_add=True)
    

class Tweet(models.Model):
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)
    content = models.TextField(blank=True, null=True)
    image = models.FileField(upload_to='images/', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='tweet_user', blank=True, through=TweetLikes)
    time_stamp = models.DateTimeField(auto_now_add=True)
    
    @property
    def is_retweet(self):
       return self.parent != None
    
    class Meta:
        ordering = ['-id']
    
    def __getitem__(self, key):
        if key == 'content':
            return self.content
    
    def __setitem__(self, key, data):
        if key == 'content':
    
            self.content = data
            
   
       
     
    
    





