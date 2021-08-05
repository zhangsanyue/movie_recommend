from django import forms
from movie.models import *
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from .models import OAuth_ex, OAuth_type


class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=Category.NAME_MAX_LENGTH, help_text="Category")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Category
        fields = ('name', )


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ('title', 'director', 'writers', 'stars', 'storyline', 'image',)
        exclude = ('category',)
    

class RecommendListForm(forms.ModelForm):
    class Meta:
        model = RecommendList
        fields = ('title', )
        exclude = ('movie',)


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture',)


class BindEmail(forms.Form):
    """bind the openid to email"""
    openid = forms.CharField(widget=forms.HiddenInput(attrs={'id': 'openid'}))
    nickname = forms.CharField(widget=forms.HiddenInput(attrs={'id': 'nickname'}))
    oauth_type_id = forms.CharField(widget=forms.HiddenInput(attrs={'id': 'oauth_type'}))

    email = forms.EmailField(label=u'Email',
                             widget=forms.EmailInput(
                                 attrs={'class': 'form-control', 'id': 'email', 'placeholder': u'Input your Email'}))
    pwd = forms.CharField(label=u'Password', max_length=36,
                          widget=forms.PasswordInput(
                              attrs={'class': 'form-control', 'id': 'pwd', 'placeholder': u'If not register，this would be your password'}))

    def clean_email(self):
        oauth_type_id = self.cleaned_data.get('oauth_type_id')
        email = self.cleaned_data.get('email')

        users = User.objects.filter(email=email)
        oauth_type = OAuth_type.objects.get(id=oauth_type_id)

        if users:

            if OAuth_ex.objects.filter(user=users[0], oauth_type=oauth_type):
                raise ValidationError(u'Email was bound')
        return email

    def clean_pwd(self):
        email = self.cleaned_data.get('email')
        pwd = self.cleaned_data.get('pwd')

        users = User.objects.filter(email=email)
        if users:
            user = authenticate(username=email, password=pwd)
            if user is not None:
                return pwd
            else:
                return ValidationError(u'Invalid password')

