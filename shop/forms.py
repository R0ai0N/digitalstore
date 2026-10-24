from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django_svg_image_form_field import SvgAndImageFormField

from .models import Category, Delivery


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = []
        field_classes = {
            'icon': SvgAndImageFormField,
        }


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Имя пользователя'
    }))

    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Пароль'
    }))


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Имя пользователя',
        'autofocus': True
    }))

    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ваше имя'
    }))

    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ваша фамилия'
    }))

    email = forms.EmailField(label='Почта', widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ваша почта'
    }))

    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Пароль'
    }))

    password2 = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Подтвердите пароль'
    }))

    phone_number = forms.CharField(label='Номер телефона', max_length=40, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Номер телефона'
    }))

    photo = forms.ImageField(label='Фото', required=False, widget=forms.FileInput(attrs={
        'class': 'form-control'
    }))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class DeliveryForm(forms.ModelForm):
    class Meta:
        model = Delivery
        fields = ('city', 'address', 'state', 'phone', 'comment', 'first_name', 'last_name', 'email')
        widgets = {
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Город'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Адрес'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Регион'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Номер телефона'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Комментарии к заказу'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваше имя...'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваша фамилия...'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ваша почта'}),
        }
