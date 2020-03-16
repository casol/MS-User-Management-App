import datetime
import csv
import io

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.messages import get_messages

from users.forms import CustomUserCreationForm, CustomUserChangeForm

User = get_user_model()


class SignupViewTest(TestCase):
    """Test sign up view."""

    def test_get_view_url_exists_at_desired_location(self):
        response = self.client.get('/signup/')
        self.assertEqual(response.status_code, 200)

    def test_get_view_url_accessible_by_name(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)

    def test_get_view_uses_correct_template(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'management_tool/signup.html')

    def test_get_view_populates_form_into_context(self):
        response = self.client.get(reverse('signup'))
        self.assertIsInstance(response.context['user_form'],
                              CustomUserCreationForm)
        self.assertTrue(isinstance(response.context['user_form'],
                                   CustomUserCreationForm))

    def test_signup_form_validation_for_blank_items(self):
        form_data = {'username': '',
                     'email': '',
                     'birth_date': '',
                     'password': '',
                     'password2': ''}
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        for filed, error in form.errors.items():
            self.assertEqual(error,
                             ["This field is required."])

    def test_signup_form_is_valid(self):
        form_data = {'username': 'TestUser',
                     'email': 'test3@test31.com',
                     'birth_date': datetime.datetime.now(),
                     'password1': 'Pw4Newuser',
                     'password2': 'Pw4Newuser'}
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_signup_form_success(self):
        response = self.client.post('/signup/',
                                    {
                                        'username': 'TestUser',
                                        'email': 'test3@test31.com',
                                        'birth_date': datetime.datetime.now(),
                                        'password1': 'Pw4Newuser',
                                        'password2': 'Pw4Newuser'
                                    })
        self.assertEqual(response.status_code, 200)


class HomeViewTest(TestCase):
    """Test home view."""

    def test_get_view_url_exists_at_desired_location(self):
        response = self.client.get('/home/')
        self.assertEqual(response.status_code, 200)

    def test_get_view_url_accessible_by_name(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_get_view_uses_correct_template(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'management_tool/home.html')


class UserListViewTest(TestCase):
    """Test user list view."""
    def setUp(self):
        """Setup user for @login_required views."""
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com',
                                             'johnpassword')
        self.client.login(username='john', password='johnpassword')

    def test_get_view_url_exists_at_desired_location(self):
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, 200)

    def test_get_view_url_accessible_by_name(self):
        response = self.client.get(reverse('user_list'))
        self.assertEqual(response.status_code, 200)

    def test_get_view_uses_correct_template(self):
        response = self.client.get(reverse('user_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'management_tool/user_list.html')

    def test_get_view_for_anonymous_user_user(self):
        self.client.logout()
        response = self.client.get(reverse('user_list'))
        self.assertEqual(response.status_code, 302)

    def test_get_view_redirects_for_anonymous_user(self):
        self.client.logout()
        response = self.client.get(reverse('user_list'))
        self.assertRedirects(response, '/login/?next=/users/')

    def test_get_user_list(self):
        response = self.client.get(reverse('user_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['user_list']), 1)
        self.assertEqual(response.context['user_list'][0].username, 'john')


class UserDetailsViewTest(TestCase):
    """Test user details view."""

    def setUp(self):
        """Setup user for @login_required views."""
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com',
                                             'johnpassword')
        self.client.login(username='john', password='johnpassword')

    def test_get_view_url_exists_at_desired_location(self):
        response = self.client.get('/user/john/')
        self.assertEqual(response.status_code, 200)

    def test_get_view_url_accessible_by_name(self):
        response = self.client.get(reverse('user_details',
                                   kwargs={'username': self.user.username}))
        self.assertEqual(response.status_code, 200)

    def test_get_view_uses_correct_template(self):
        response = self.client.get(reverse('user_details',
                                   kwargs={'username': self.user.username}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'management_tool/user_details.html')

    def test_get_view_for_anonymous_user_user(self):
        self.client.logout()
        response = self.client.get(reverse('user_details',
                                   kwargs={'username': self.user.username}))
        self.assertEqual(response.status_code, 302)

    def test_get_view_redirects_for_anonymous_user(self):
        self.client.logout()
        response = self.client.get(reverse('user_details',
                                   kwargs={'username': self.user.username}))
        self.assertRedirects(response, '/login/?next=/user/john/')

    def test_get_user_details(self):
        response = self.client.get(reverse('user_details',
                                   kwargs={'username': self.user.username}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user_details'])
        self.assertEqual(response.context['user_details'].username, 'john')

    def test_get_user_details_get_absolute_url(self):
        response = self.client.get(self.user.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user_details'])
        self.assertEqual(response.context['user_details'].username, 'john')


class UserEditViewTest(TestCase):
    """Test user edit view."""

    def setUp(self):
        """Setup user for @login_required views."""
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com',
                                             'johnpassword')
        self.client.login(username='john', password='johnpassword')

    def test_get_view_url_exists_at_desired_location(self):
        response = self.client.get('/edit/')
        self.assertEqual(response.status_code, 200)

    def test_get_view_url_accessible_by_name(self):
        response = self.client.get(reverse('user_edit'))
        self.assertEqual(response.status_code, 200)

    def test_get_view_uses_correct_template(self):
        response = self.client.get(reverse('user_edit'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'management_tool/user_edit.html')

    def test_get_view_for_anonymous_user_user(self):
        self.client.logout()
        response = self.client.get(reverse('user_edit'))
        self.assertEqual(response.status_code, 302)

    def test_get_view_redirects_for_anonymous_user(self):
        self.client.logout()
        response = self.client.get(reverse('user_edit'))
        self.assertRedirects(response, '/login/?next=/edit/')

    def test_get_view_populates_form_into_context(self):
        response = self.client.get(reverse('user_edit'))
        self.assertIsInstance(response.context['user_form'],
                              CustomUserChangeForm)
        self.assertTrue(isinstance(response.context['user_form'],
                                   CustomUserChangeForm))

    def test_edit_form_validation_for_blank_items(self):
        form_data = {'username': '',
                     'birth_date': '',
                     'random_number': ''}
        form = CustomUserChangeForm(data=form_data)
        self.assertFalse(form.is_valid())
        for filed, error in form.errors.items():
            self.assertEqual(error,
                             ["This field is required."])

    def test_edit_form_error_messages_for_blank_items(self):
        response = self.client.post(reverse('user_edit'))
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn('Please correct the error below.', messages)

    def test_edit_form_is_valid(self):
        form_data = {'username': 'TestUser',
                     'birth_date': datetime.datetime.now(),
                     'random_number': '4'}
        form = CustomUserChangeForm(data=form_data)
        self.assertTrue(form.is_valid())


class UserDeleteViewTest(TestCase):
    """Test user edit view."""

    def setUp(self):
        """Setup user for @login_required views."""
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com',
                                             'johnpassword')
        self.client.login(username='john', password='johnpassword')

    def test_get_view_url_exists_at_desired_location(self):
        response = self.client.get('/delete/')
        self.assertEqual(response.status_code, 200)

    def test_get_view_url_accessible_by_name(self):
        response = self.client.get(reverse('user_delete'))
        self.assertEqual(response.status_code, 200)

    def test_get_view_uses_correct_template(self):
        response = self.client.get(reverse('user_delete'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'management_tool/user_delete.html')

    def test_get_view_for_anonymous_user_user(self):
        self.client.logout()
        response = self.client.get(reverse('user_delete'))
        self.assertEqual(response.status_code, 302)

    def test_get_view_redirects_for_anonymous_user(self):
        self.client.logout()
        response = self.client.get(reverse('user_delete'))
        self.assertRedirects(response, '/home/?next=/delete/')

    def test_get_view_populates_form_into_context(self):
        response = self.client.get(reverse('user_delete'))
        self.assertTrue(response.context['user_delete'])

    def test_post_view_deletes_user(self):
        response = self.client.post(reverse('user_delete'))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(self.client.login(username='john',
                                           password='johnpassword'))

    def test_post_view_redirects_for_anonymous_user(self):
        self.client.logout()
        response = self.client.post(reverse('user_delete'))
        self.assertRedirects(response, '/home/?next=/delete/')

    def test_delete_form_successful_messages(self):
        response = self.client.post(reverse('user_delete'))
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn('User successfully deleted!', messages)


class ExportUserCSVViewTest(TestCase):
    """Test user list export view."""

    def setUp(self):
        self.user = User.objects.create_user(username='john',
                                             email='lennon@thebeatles.com',
                                             birth_date=datetime.datetime.now(),
                                             password='johnpassword')
        self.client.login(username='john', password='johnpassword')

    def test_get_view_url_exists_at_desired_location(self):
        response = self.client.get('/download/')
        self.assertEqual(response.status_code, 200)

    def test_get_view_url_accessible_by_name(self):
        response = self.client.get(reverse('export_user_csv'))
        self.assertTrue(response.status_code)

    def test_get_view_for_anonymous_user_user(self):
        self.client.logout()
        response = self.client.get(reverse('export_user_csv'))
        self.assertEqual(response.status_code, 302)

    def test_get_view_redirects_for_anonymous_user(self):
        self.client.logout()
        response = self.client.get(reverse('export_user_csv'))
        self.assertRedirects(response, '/login/?next=/download/')

    def test_csv_export(self):
        response = self.client.get('/download/')
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        cvs_reader = csv.reader(io.StringIO(content))
        body = list(cvs_reader)
        self.assertIn('john', body[1])
        self.assertEqual(body.pop(0), ['Username', 'Birthday', 'Eligible',
                                       'Random Number', 'BizzFuzz'])
