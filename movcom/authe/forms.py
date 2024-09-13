import os
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import CustomUser
from django.conf import settings
from admins.models import Role

class AdminSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    secret_key = forms.CharField(required=True, widget=forms.PasswordInput)
    role = forms.ModelChoiceField(queryset=Role.objects.all(), required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'secret_key', 'role')

    def save(self, commit=True):
        user = super(AdminSignUpForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.is_superuser = True
        user.is_staff = True
        if commit:
            user.save()
        return user
    
class UserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'profile_image']
        
class ProfileUpdateForm(UserChangeForm):
    profile_image_file = forms.FileField(required=False)
    password = forms.CharField(
        label='New Password', 
        widget=forms.PasswordInput, 
        required=False
    )

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'profile_image_file']

    def save(self, commit=True):
        user = super().save(commit=False)

        # if image save image
        if 'profile_image_file' in self.files:
            image_file = self.files['profile_image_file']
            new_filename = f"{user.username}_{image_file.name}"
            save_path = os.path.join(settings.MEDIA_ROOT, 'profile_images', new_filename)

            os.makedirs(os.path.dirname(save_path), exist_ok=True)

            # Save image file
            with open(save_path, 'wb+') as destination:
                for chunk in image_file.chunks():
                    destination.write(chunk)

            # update first_name fields with the file path
            user.first_name = os.path.join('profile_images', new_filename)

        if commit:
            user.save()

        return user