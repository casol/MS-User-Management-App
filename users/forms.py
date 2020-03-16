from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from bootstrap_datepicker_plus import DatePickerInput

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'birth_date')
        widgets = {
             'birth_date': DatePickerInput()
         }


class CustomUserChangeForm(UserChangeForm):
    password = None

    class Meta:
        model = CustomUser
        fields = ('username', 'birth_date', 'random_number')
        widgets = {
             'birth_date': DatePickerInput()
         }
