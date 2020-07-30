from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status
from core.models import Tag
from recipe.serializers import TagSerializer


TAGS_URL = reverse('recipe:tag-list')


class PublicTagsAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to retrieve tags"""
        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsAPITest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='locnt@dev.com',
            password='password'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """Test retrieve tags"""
        Tag.objects.create(user=self.user, name='Vegan')
        Tag.objects.create(user=self.user, name='Megan')
        res = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by('-name')
        serialier = TagSerializer(tags, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serialier.data)

    def test_tags_limited_to_user(self):
        """Test that tags returned are for a authenticated user"""
        user2 = get_user_model().objects.create_user(
            email='locnt2@dev.com',
            password='password'
        )
        Tag.objects.create(user=user2, name='Vegan')
        tag = Tag.objects.create(user=self.user, name='Megan')
        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)
