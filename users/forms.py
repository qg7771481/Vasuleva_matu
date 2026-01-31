from django import forms
from django.contrib.auth.models import User
from django.forms import ValidationError


class RegisterForm(forms.ModelForm):
    password_confirm = forms.CharField()
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirm')
        widgets = {
            'password_confirm': forms.PasswordInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        }

    def clean_password_confirm(self):
        password = self.cleaned_data.get("password")
        password_confirm = self.cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise ValidationError("Passwords don't match.")

        return password_confirm

    def save(self, commit: bool = True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()

        return user






