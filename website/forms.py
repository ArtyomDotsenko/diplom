from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import Month, God, MunicipalOrganizations


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(
        attrs={'class': 'form-control', 'autocomplete': 'off'}))
    password1 = forms.CharField(
        label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))
    email = forms.EmailField(
        label='E-mail', help_text='Введите адрес почты', widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    password = forms.CharField(
        label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class AddDataForm(forms.Form):
    fact = forms.FloatField(label='Факт по потреблению', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    limit = forms.FloatField(label='Лимит по потреблению', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    explanatory_note = forms.FileField(label='Пояснительная записка', required=False, allow_empty_file=True,
                                       widget=forms.FileInput(attrs={'class': 'form-control'}))
    note = forms.CharField(label='Краткое описание пояснительной записки', required=False,
                           widget=forms.TextInput(attrs={'class': 'form-control'}))


class MonthYear(forms.Form):
    month = forms.ModelChoiceField(queryset=Month.objects.all(), label='Месяц',
                                   widget=forms.Select(attrs={'class': 'form-control'}))
    god = forms.ModelChoiceField(queryset=God.objects.all(), label='Год',
                                 widget=forms.Select(attrs={'class': 'form-control'}))


class OrganizationsForm(forms.Form):
    organizations = forms.ModelChoiceField(queryset=MunicipalOrganizations.objects.all(), label='Организация',
                                           widget=forms.Select(attrs={'class': 'form-control'}))
