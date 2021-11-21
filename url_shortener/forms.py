from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import Url

User = get_user_model()


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UrlForm(forms.ModelForm):

    class Meta:
        model = Url
        fields = ['original']

    def clean_original(self):
        given_url = self.cleaned_data['original']
        is_url_correct = given_url.find('https://') == 0 or given_url.find('http://') == 0 or given_url.find('ftp://') == 0

        if not is_url_correct:
            raise forms.ValidationError("You need to use correct url!")

        return given_url
