from django.forms import ModelForm,ValidationError
from .models import Tweet
from django.conf import settings

max_len = settings.MAX_TWEET_LENGTH

class TweetCreateForm(ModelForm):
    class Meta:
        model = Tweet
        fields = ['content']
    
    
    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) > max_len:
            raise ValidationError('Tweet length exceeeded ', max_len)
        else:
            return content
            