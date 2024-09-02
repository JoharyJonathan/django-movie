from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class AdminSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    secret_key = forms.CharField(required=True, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'secret_key')

    def save(self, commit=True):
        user = super(AdminSignUpForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.is_superuser = True
        user.is_staff = True
        if commit:
            user.save()
        return user