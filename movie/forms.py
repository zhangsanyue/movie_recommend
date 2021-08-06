from django import forms
from movie.models import *


class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=Category.NAME_MAX_LENGTH)
    image = forms.ImageField()
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Category
        fields = ('name', )


class MovieForm(forms.ModelForm):
    image = forms.ImageField()

    class Meta:
        model = Movie
        fields = ('title', 'director', 'writers', 'stars', 'storyline',)
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


