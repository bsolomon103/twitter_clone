from rest_framework import serializers
from .models import Tweet
from django.conf import settings

max_len = settings.MAX_TWEET_LENGTH
tweet_action_options = settings.TWEET_ACTION_OPTIONS

class TweetCreateSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()
    
    class Meta:
        model = Tweet
        fields = ['id','content','likes']
    
    def get_likes(self, obj):
        return obj.likes.count()
    
    
    def validate_content(self, content):
        if len(content) > max_len:
            raise serializers.ValidationError('Tweet length exceeded '+ str(max_len) +' characters.')
        else:
            return content

class TweetSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)
    parent = TweetCreateSerializer(read_only=True)
    
    class Meta:
        model = Tweet
        fields = ['id','content','likes','is_retweet','parent']
    
    def get_likes(self, obj):
        return obj.likes.count()
    
    
    

            
class TweetActionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    content = serializers.CharField(allow_blank=True, required=False)
    action = serializers.CharField()
    
    def validate_action(self, value):
        value = value.lower().strip()
        if value not in tweet_action_options:
            raise serializers.ValidationError('Action not permitted')
        else:
            return value


            



    
    