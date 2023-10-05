"""
Tests for models
"""
from django.test import TestCase
from django.contrib.auth import get_user_model

class ModelTests(TestCase):
    """Test models"""

    def test_create_user_with_successful(self):
        """Test creating user with a name is successful"""
        name = 'test'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            name=name,
            password=password,
        )

        self.assertEqual(user.name, name)
        self.assertTrue(user.check_password(password))
    
    def test_new_user_without_email_raises_error(self):
        """Test that creating auser without a name raises a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')
    
    def test_create_superuser(self):
        """Test creating a superuser"""
        user = get_user_model().objects.create_superuser(
            'test', 'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
