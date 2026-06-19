import re
from django import forms
from django.contrib.auth.forms import UserCreationForm
from datetime import date
from .models import CustomUser, Application, Review


class RegisterForm(UserCreationForm):
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
    DAY_CHOICES = [(i, str(i).zfill(2)) for i in range(1, 32)]
    MONTH_CHOICES = [(i, str(i).zfill(2)) for i in range(1, 13)]

    current_year = date.today().year
    YEAR_CHOICES = [(year, str(year)) for year in range(current_year, current_year + 6)]
    
    day = forms.ChoiceField(
        choices=DAY_CHOICES,
        label='День',
        widget=forms.Select(attrs={'class': 'date-select'})
    )
    month = forms.ChoiceField(
        choices=MONTH_CHOICES,
        label='Месяц',
        widget=forms.Select(attrs={'class': 'date-select'})
    )
    year = forms.ChoiceField(
        choices=YEAR_CHOICES,
        label='Год',
        widget=forms.Select(attrs={'class': 'date-select'})
    )

    class Meta:
        model = Application
        fields = ['transport', 'payment']
        widgets = {
            'transport': forms.Select(),
            'payment': forms.Select(),
        }

    def clean(self):
        cleaned_data = super().clean()
        day = cleaned_data.get('day')
        month = cleaned_data.get('month')
        year = cleaned_data.get('year')

        if day and month and year:
            try:
                start_date = date(int(year), int(month), int(day))
                cleaned_data['start_date'] = start_date

                if start_date < date.today():
                    raise forms.ValidationError(
                        'Дата начала обучения не может быть в прошлом'
                    )
            except ValueError:
                raise forms.ValidationError(
                    'Выбрана некорректная дата (например, 31 февраля)'
                )

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.start_date = self.cleaned_data['start_date']
        if commit:
            instance.save()
        return instance


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Поделитесь впечатлениями об обучении...'
            }),
        }