import re
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Application


class RegisterForm(UserCreationForm):
    """Форма регистрации с валидацией"""
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'full_name', 'birth_date', 'phone',
                  'password1', 'password2']
        widgets = {
            'birth_date': forms.DateInput(
                attrs={'type': 'text', 'placeholder': 'ДД.ММ.ГГГГ'}
            ),
        }

    def clean_username(self):
        login = self.cleaned_data['username']
        if len(login) < 6:
            raise forms.ValidationError('Логин должен быть не менее 6 символов')
        if not re.match(r'^[a-zA-Z0-9]+$', login):
            raise forms.ValidationError(
                'Логин должен содержать только латинские буквы и цифры'
            )
        return login


class ApplicationForm(forms.ModelForm):
    """Форма заявки на обучение"""
    class Meta:
        model = Application
        fields = ['transport', 'start_date', 'payment']
        widgets = {
            'start_date': forms.DateInput(
                attrs={'type': 'text', 'placeholder': 'ДД.ММ.ГГГГ'}
            ),
            'transport': forms.Select(),
            'payment': forms.Select(),
        }