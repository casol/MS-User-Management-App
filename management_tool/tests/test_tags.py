import datetime
import random

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.template import Context, Template
from management_tool.templatetags.bizz_fuzz import get_bizz_fuzz
User = get_user_model()


class EligibleTempletTagTest(TestCase):
    """Test eligible template tag."""

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='YoungUser',
                                 email='u@u.com',
                                 password='foo',
                                 birth_date=datetime.date.today(),
                                 random_number=random.randint(1, 100))
        User.objects.create_user(username='OldUser',
                                 email='u2@u.com',
                                 password='foo',
                                 birth_date=datetime.date(1955, 12, 1),
                                 random_number=random.randint(1, 100))

    def test_get_eligible_tag_for_allowed_user(self):
        user_list = User.objects.filter(id=2)
        out = Template(
            "{% load eligible %}"
            "{% for user in user_list %}"
            "{{ user.birth_date|calculate_age }}"
            "{% endfor %}"
        ).render(Context({
            'user_list': user_list
        }))
        self.assertEqual(out, "Allowed", msg='Should return Allowed')

    def test_get_eligible_tag_for_blocked_user(self):
        user_list = User.objects.filter(id=1)
        out = Template(
            "{% load eligible %}"
            "{% for user in user_list %}"
            "{{ user.birth_date|calculate_age }}"
            "{% endfor %}"
        ).render(Context({
            'user_list': user_list
        }))
        self.assertEqual(out, "Blocked", msg='Should return Blocked')

    def test_get_eligible_tag_for_user_list(self):
        user_list = User.objects.all()
        out = Template(
            "{% load eligible %}"
            "{% for user in user_list %}"
            "{{ user.birth_date|calculate_age }},"
            "{% endfor %}"
        ).render(Context({
            'user_list': user_list
        }))
        self.assertEqual(out, "Blocked,Allowed,",
                         msg='Should return Blocked, Allowed')

    def test_get_eligible_tag_for_empty_context(self):
        out = Template(
            "{% load eligible %}"
            "{% for user in user_list %}"
            "{{ user.birth_date|calculate_age }}"
            "{% endfor %}"
        ).render(Context())
        self.assertEqual(out, '', msg='Should return empty string')

    def test_get_eligible_tag_for_wrong_argument(self):
        out = Template(
            "{% load eligible %}"
            "{% for user in user_list %}"
            "{{ user.birth_date|calculate_age }}"
            "{% endfor %}"
        ).render(Context({'date': 'a_string'}))
        self.assertEqual(out, '', msg='Should return empty string')


class BizzFuzzTempletTagTest(TestCase):
    """Test bizz fuzz template tag."""

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(
            username='User',
            email='u@u.com',
            password='foo',
            birth_date=datetime.date.today(),
            random_number=1)
        User.objects.create_user(
            username='UserBizz',
            email='u2@u.com',
            password='foo',
            birth_date=datetime.date(1945, 2, 1),
            random_number=78)
        User.objects.create_user(
            username='UserFuzz',
            email='u3@u.com',
            password='foo',
            birth_date=datetime.date(1985, 3, 22),
            random_number=100)
        User.objects.create_user(
            username='UserBizzFuzz',
            email='u4@u.com',
            password='foo',
            birth_date=datetime.date(2000, 1, 1),
            random_number=15)

    def test_get_bizzfuzz_tag_for_non_user(self):
        user = User.objects.filter(id=1)
        out = Template(
            "{% load bizz_fuzz %}"
            "{% for u in user %}"
            "{{ u.random_number|get_bizz_fuzz }}"
            "{% endfor %}"
        ).render(Context({
            'user': user
        }))
        self.assertEqual(out,
                         str(get_bizz_fuzz(1)),
                         msg='Should return random number')

    def test_get_bizzfuzz_tag_for_bizz_user(self):
        user = User.objects.filter(id=2)
        out = Template(
            "{% load bizz_fuzz %}"
            "{% for u in user %}"
            "{{ u.random_number|get_bizz_fuzz }}"
            "{% endfor %}"
        ).render(Context({
            'user': user
        }))
        self.assertEqual(out,
                         str(get_bizz_fuzz(78)),
                         msg='Should return Bizz')

    def test_get_bizzfuzz_tag_for_fuzz_user(self):
        user = User.objects.filter(id=3)
        out = Template(
            "{% load bizz_fuzz %}"
            "{% for u in user %}"
            "{{ u.random_number|get_bizz_fuzz }}"
            "{% endfor %}"
        ).render(Context({
            'user': user
        }))
        self.assertEqual(out,
                         str(get_bizz_fuzz(100)),
                         msg='Should return Fuzz')

    def test_get_bizzfuzz_tag_for_bizzfuzz_user(self):
        user = User.objects.filter(id=4)
        out = Template(
            "{% load bizz_fuzz %}"
            "{% for u in user %}"
            "{{ u.random_number|get_bizz_fuzz }}"
            "{% endfor %}"
        ).render(Context({
            'user': user
        }))
        self.assertEqual(out,
                         str(get_bizz_fuzz(15)),
                         msg='Should return BuzzFizz')

    def test_get_bizzfuzz_tag_for_empty_context(self):
        out = Template(
            "{% load bizz_fuzz %}"
            "{% for u in user %}"
            "{{ u.random_number|get_bizz_fuzz }}"
            "{% endfor %}"
        ).render(Context())
        self.assertEqual(out, '', msg='Should return empty string')

    def test_get_bizzfuzz_tag_for_wrong_argument(self):
        out = Template(
            "{% load bizz_fuzz %}"
            "{% for u in user %}"
            "{{ u.random_number|get_bizz_fuzz }}"
            "{% endfor %}"
        ).render(Context({'date': 'a_string'}))
        self.assertEqual(out, '', msg='Should return empty string')
