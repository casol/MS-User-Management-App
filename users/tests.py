import datetime
import random

from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class UsersManagersTests(TestCase):
    """Test user and superuser creation."""

    def test_create_user(self):
        random_nr = random.randint(1, 100)
        user = User.objects.create_user(username='TestNormal',
                                        email='normal@user.com',
                                        password='foo',
                                        birth_date=datetime.date.today(),
                                        random_number=random_nr)
        self.assertEqual(user.username, 'TestNormal')
        self.assertEqual(user.email, 'normal@user.com')
        self.assertEqual(user.birth_date, datetime.date.today())
        self.assertEqual(user.random_number, random_nr)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(ValueError):
            User.objects.create_user(username='')
        with self.assertRaises(TypeError):
            User.objects.create_user(email='')
        with self.assertRaises(ValueError):
            User.objects.create_user(username='', email='', password="foo")

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser('TestSuper',
                                                   'super@user.com',
                                                   'foo')
        self.assertEqual(admin_user.email, 'super@user.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                username='TestSuper', email='super@user.com',
                password='foo', is_superuser=False)


class CustomUserTest(TestCase):
    """Test custom user model."""

    @classmethod
    def setUpTestData(cls):
        """Setup a user objects."""
        user = User.objects.create(username='TestUser',
                                   password='foo',
                                   birth_date=datetime.date.today(),
                                   random_number=random.randint(1, 100))

    def test_email_date_label(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field('email').verbose_name
        self.assertEqual(field_label, 'email')

    def test_email_max_length(self):
        user = User.objects.get(id=1)
        max_length = user._meta.get_field('email').max_length
        self.assertEquals(max_length, 70)

    def test_birth_date_label(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field('birth_date').verbose_name
        self.assertEqual(field_label, 'birth date')

    def test_random_number_label(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field('random_number').verbose_name
        self.assertEqual(field_label, 'random number')
