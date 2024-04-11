from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.authtoken.models import Token

from watchlist_app.api import serializers
from watchlist_app import models

class StreamPlatformTestCase(APITestCase):

    def setUp(self):                                 #access user token for login
        self.user=User.objects.create_user(username="example", password="Password@123")
        self.token=Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token '+self.token.key)
        # print("sarthak")
        self.stream=models.StreamPlatform.objects.create(name="Netflix",about="#1 platform",website="https://www.netflix.com")

    def test_streamplatform_create(self):
        data={
            "name":"Netflix",
            "about":"#1 Streaming platform",
            "website":"https://www.netflix.com"
        }
        response=self.client.post(reverse('streamplatformvs-list'),data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_streamplatform_list(self):
        response=self.client.get(reverse('streamplatformvs-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_streamplatform_ind(self):
        response=self.client.get(reverse('streamplatformvs-detail', args=(self.stream.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class WatchListTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="example", password="Password@123")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.stream = models.StreamPlatform.objects.create(name="Netflix", about="#1 platform",website="https://www.netflix.com")
        self.watchlist=models.WatchList.objects.create(platform=self.stream, title="Example Movie", storyline="Example Movie", active=True)

    def test_watchlist_create(self):
        data={
            "platform":self.stream,
            "title":"Example movie",
            "storyline":"Example story",
            "active":True
        }
        response=self.client.post(reverse('movie-list-api-view-class'),data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_watchlist_list(self):
        response=self.client.get(reverse('movie-list-api-view-class'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_watchlist_ind(self):
        response=self.client.get(reverse('movie-details',args=(self.watchlist.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class ReviewTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="example", password="Password@123")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.stream = models.StreamPlatform.objects.create(name="Netflix", about="#1 platform",website="https://www.netflix.com")
        self.watchlist=models.WatchList.objects.create(platform=self.stream, title="Example Movie", storyline="Example Movie", active=True)
        self.watchlist2 = models.WatchList.objects.create(platform=self.stream, title="Example Movie",storyline="Example Movie",active=True)
        self.review=models.Review.objects.create(review_user=self.user,rating=5,description="Great movie!",watchlist=self.watchlist2,active=True)

    def test_review_create(self):
        data={
            "review_user":self.user,
            "rating":5,
            "description":"Great movie!",
            "watchlist":self.watchlist,
            "active":True
        }
        response=self.client.post(reverse('review-create',args=(self.watchlist.id,)),data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(reverse('review-create', args=(self.watchlist.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_review_create_unauth(self):
        data={
            "review_user": self.user,
            "rating": 5,
            "description": "Great movie!",
            "watchlist": self.watchlist,
            "active": True
        }
        self.client.force_authenticate(user=None)
        response = self.client.post(reverse('review-create', args=(self.watchlist.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_review_update(self):
        data = {
            "review_user": self.user,
            "rating": 4,
            "description": "Great movie!-Updated",
            "watchlist": self.watchlist,
            "active": False
        }
        response = self.client.put(reverse('review-detail', args=(self.review.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_list(self):
        response=self.client.get(reverse('review-list',args=(self.watchlist.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_indlist(self):
        response = self.client.get(reverse('review-detail', args=(self.review.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_user(self):
        response=self.client.get('/watch/reviews/?username'+self.user.username)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
# Create your tests here.
