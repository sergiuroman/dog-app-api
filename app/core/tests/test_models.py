from django.test import TestCase
from unittest.mock import patch
from django.contrib.auth import get_user_model
from core import models


def sample_user(email='test@gmail.com', password='pass123'):
    """create a sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'test159@gmail.com'
        password = 'pass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = 'test62@GMail.com'
        user = get_user_model().objects.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@gnma.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)

    def test_recipe_str(self):
        """Test the dog string representation"""
        dog = models.Dog.objects.create(
            user=sample_user(),
            name='Dog name number1',
            description='the description of the dog',
            location='Piezisa nr 15 cluj napoca',
            size='medium',
            age='junior',
            purpose='adopt'
        )

        self.assertEqual(str(dog), dog.name)

    @patch('uuid.uuid4')
    def test_dog_file_name_uuid(self, mock_uuid):
        """test image is save din the correct location"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.dog_image_file_path(None, 'myimage.jpg')
        exp_path = f'uploads/recipe/{uuid}.jpg'
        self.assertEqual(file_path,exp_path)
