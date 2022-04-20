from django.views import View
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import TweetCreateForm
from .models import Tweet
from rest_framework.views import APIView
from .serializers import (TweetSerializer, TweetActionSerializer, TweetCreateSerializer)
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.conf import settings


class HomeView(View):
    template = 'pages/home.html'
    def get(self, request, *args, **kwargs):
        return render(request, self.template, context={})

class TweetCreateView2(View):
    '''add logic to only allow users to create tweets'''
    template = 'components/form.html'
    success_url = reverse_lazy('tweets:all')
    def get(self, request, *args, **kwargs):
        form = TweetCreateForm()
        ctx = {'form':form}
        return render(request, self.template, context=ctx)
        
    def post(self, request, *args, **kwargs):
        user = request.user
        is_ajax = request.META.get("HTTP_X_REQUESTED_WITH") == 'XMLHttpRequest'
        if not user.is_authenticated:
            user = None
            if is_ajax:
                return JsonResponse({}, status=401)
            return redirect(settings.LOGIN_URL)
        else:
            form = TweetCreateForm(request.POST)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.user = user
                obj.save()
                if is_ajax:
                    return JsonResponse(obj.serialize(), status=201)
                else:
                    ctx = {'form': obj}
                    return redirect(self.success_url)
            else:
                if is_ajax:
                    return JsonResponse(form.errors, status=400)
                else:
                    ctx = {'form':form}
                    return render(request, self.template, context=ctx, status=400)
                
       

class TweetRepoView2(View):
    ''' REST API '''
    def get(self, request, *args, **kwargs):
        qs = Tweet.objects.all()
        tweets = [item.serialize() for item in qs]
        data = {
            'response': tweets
        }
        return JsonResponse(data, status=200)

class TweetRepoView(APIView):
    ''' DRF API '''
    def get(self, request, *args, **kwargs):
        qs = Tweet.objects.all()
        serializer = TweetSerializer(qs, many=True)
        return Response(serializer.data, status=200)
            
        

class TweetCreateView(APIView):
    '''DRF VIEW '''
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        serializer = TweetCreateSerializer(data=request.POST)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user = request.user)
            return Response(serializer.data, status=201)
        return Response({}, status = 400)


class TweetDeleteView(APIView):
    '''DRF API'''
    permission_classes = [IsAuthenticated]
    def delete(self, request, tweet_id, *args, **kwargs):
        qs = Tweet.objects.filter(id=tweet_id)
        if not qs.exists():
            return Response({}, status=404)
        else:
            obj = qs.filter(user = request.user)
            if obj.exists():
                obj.delete()
                return Response({'msg':'Tweet Deleted'}, status=200)
            else:
                return Response({'msg': 'Not authorized to delete this tweet'},status=403)
    

class TweetDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, tweet_id, *args, **kwargs):
        qs = Tweet.objects.filter(id = tweet_id)
        if not qs.exists():
            return Response({}, status=404)
        else:
            obj = qs.first()
            serializer = TweetSerializer(obj)
            return Response(serializer.data, status=200)


class TweetActionView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        serializer = TweetActionSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
            tweet_id = data.get('id')
            content = data.get('content')
            action = data.get('action')
            #print(action)
            qs = Tweet.objects.filter(id=tweet_id)
            if not qs.exists():
                return Response({}, status=404)
            else:
                obj = qs.first()
                if action == 'like':
                    obj.likes.add(request.user)
                    serializer = TweetSerializer(obj)
                    return Response(serializer.data, status=200)
                elif action == 'unlike':
                    obj.likes.remove(request.user)
                    serializer = TweetSerializer(obj)
                    return Response(serializer.data, status=200)
                elif action == 'retweet':
                    new_tweet = Tweet.objects.create(user=request.user, content=content, parent=obj)
                    serializer = TweetSerializer(new_tweet)
                    return Response(serializer.data, status=201)
                

        
                
        
    