from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email(self):
        """test creating user with an email"""
        email = 'test@x.com'
        pw = '123@123'
        user = get_user_model().objects.create_user(
            email=email,
            password=pw
        )

        self.assertEqual(user.email, email)

    def test_new_user_email_normalize(self):
        email = 'test@X.com'
        pw = '123@123'
        user = get_user_model().objects.create_user(
            email=email,
            password=pw
        )

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """test raise error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email=None,
                password='123'
            )

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            email='admin@x.com',
            password='123'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
