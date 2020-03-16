import csv
import datetime

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

from users.forms import CustomUserCreationForm, CustomUserChangeForm
from .templatetags import eligible, bizz_fuzz

User = get_user_model()


def home(request):
    """Display home page."""
    return render(request,
                  'management_tool/home.html',
                  {'section': 'home'})


@login_required
def user_list(request):
    """Display user list."""
    user_list = User.objects.filter(is_staff=False,
                                    is_active=True)
    return render(request,
                  'management_tool/user_list.html',
                  {'user_list': user_list,
                   'section': 'users'})


@login_required
def user_edit(request):
    """Display the edit form and handle the edit action."""
    if request.method == 'POST':
        user_form = CustomUserChangeForm(instance=request.user,
                                         data=request.POST)
        if user_form.is_valid():
            user_form.save()
            messages.success(request,
                             'Your profile has been updated successfully!')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        user_form = CustomUserChangeForm(instance=request.user)
    return render(request,
                  'management_tool/user_edit.html',
                  {'user_form': user_form})


@login_required
def user_details(request, username):
    """Display user profile details."""
    user_details = get_object_or_404(User, username=username,
                                     is_active=True)
    return render(request,
                  'management_tool/user_details.html',
                  {'user_details': user_details,
                   'section': 'account'})


@login_required(login_url='home')
def user_delete(request):
    """Display the delete form and handle the delete action."""
    user_delete = get_object_or_404(User,
                                    username=request.user.username)

    if (request.method == 'POST'
            and request.user.username == user_delete.username
            and request.user.is_authenticated):
        # user_delete.is_active = False
        # user_delete.save()
        user_delete.delete()
        messages.success(request, "User successfully deleted!")
        return redirect('home')

    return render(request,
                  'management_tool/user_delete.html',
                  {'user_delete': user_delete})


def signup(request):
    """Display the signup form and handle the signup action."""
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            raw_password = user_form.cleaned_data.get('password1')
            new_user.set_password(raw_password)
            # save a new user
            new_user.save()
            username = user_form.cleaned_data.get('username')
            # authenticate and login a new user
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        user_form = CustomUserCreationForm()
    return render(request,
                  'management_tool/signup.html',
                  {'user_form': user_form})


@login_required
def export_user_csv(request):
    """Downloads all users as cvs file with a single csv file."""
    response = HttpResponse(content_type='text/csv')
    attachmen_name = 'attachment; filename="{date}_user_list.csv"'.format(
        date=datetime.datetime.now().strftime('%b-%d-%Y'))
    response['Content-Disposition'] = attachmen_name

    user_list = User.objects.filter(is_staff=False,
                                    is_active=True)
    writer = csv.writer(response)
    writer.writerow(['Username', 'Birthday', 'Eligible',
                     'Random Number', 'BizzFuzz'])
    for user in user_list:
        writer.writerow([
            user.username,
            user.birth_date,
            eligible.calculate_age(user.birth_date),
            user.random_number,
            bizz_fuzz.get_bizz_fuzz(user.random_number)
        ])
    return response
