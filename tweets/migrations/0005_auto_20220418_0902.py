# Generated by Django 2.2 on 2022-04-18 09:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0004_tweet_parent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tweetlikes',
            name='tweet',
        ),
        migrations.RemoveField(
            model_name='tweetlikes',
            name='user',
        ),
        migrations.DeleteModel(
            name='Tweet',
        ),
        migrations.DeleteModel(
            name='TweetLikes',
        ),
    ]
