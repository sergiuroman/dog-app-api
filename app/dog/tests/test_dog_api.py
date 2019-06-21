from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
import tempfile
import os
from PIL import Image
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Dog

from dog.serializers import DogSerializer

DOG_URL = reverse('dog:dog-list')

def image_upload_url(dog_id):
    """return url for dog image upload"""
    return reverse('dog:dog-upload-image', args=[dog_id])

def sample_dog(user, **params):
    """Create and return a sample dog"""
    defaults = {
        'name': 'Dog unos',
        'description': 'una mia suta lei',
        'location': 'ny times square',
        'size': 'large',
        'age': 'senior',
        'purpose': 'lost'
    }
    defaults.update(params)

    return Dog.objects.create(user=user, **defaults)


class PublicDogApiTests(TestCase):
    """Test unauthenticated dog API access"""

    def setUp(self):
        self.client = APIClient()

    def test_required_auth(self):
        """Test the authentication is required"""
        res = self.client.get(DOG_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateDogApiTests(TestCase):
    """Test authenticated dog API access"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test12@gmail.com',
            'password'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_dogs(self):
        """Test retrieving list of dogs"""
        sample_dog(user=self.user)
        sample_dog(user=self.user)

        res = self.client.get(DOG_URL)

        recipes = Dog.objects.all().order_by('-id')
        serializer = DogSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_dogs_limited_to_user(self):
        """Test retrieving dogs for user"""
        user2 = get_user_model().objects.create_user(
            'other@gmail.com',
            'pass123'
        )
        sample_dog(user=user2)
        sample_dog(user=self.user)

        res = self.client.get(DOG_URL)

        recipes = Dog.objects.filter(user=self.user)
        serializer = DogSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        # self.assertEqual(res.data, serializer.data)

class DodImageUploadTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user('user@gmail.com','testpass')
        self.client.force_authenticate(self.user)
        self.dog=sample_dog(user=self.user)

    def tearDown(self):
        self.dog.image.delete()

    def test_upload_image_to_dog(self):
        """test uploading an image"""
        url=image_upload_url(self.dog.id)
        with tempfile.NamedTemporaryFile(suffix='.jpg') as ntf:
            img = Image.new('RGB',(10,10))
            img.save(ntf, format='JPEG')
            ntf.seek(0)
            res=self.client.post(url, {'image':ntf}, format='multipart')

        self.dog.refresh_from_db()
        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertIn('image',res.data)
        self.assertTrue(os.path.exists(self.dog.image.path))

    # def test_upload_img_bad_request(self):
    #     """test uploading a invalid img"""
    #     url = image_upload_url(self.dog.id)
    #     res = self.client.post(url, {'image:notimage'}, format='multipart')
    #     self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)


