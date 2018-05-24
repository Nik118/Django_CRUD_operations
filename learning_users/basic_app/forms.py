from django import forms
from django.contrib.auth.models import User
from basic_app.models import Userprofile

class userform(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username','email','password')


class userprofileform(forms.ModelForm):
    class Meta():
        model = Userprofile
        fields = ('portfolio_site', 'profile_pic')
