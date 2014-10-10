"""
    Copyright (c) 2014, Jaime Pajuelo.
    All rights reserved.

    Code released under the BSD 2-Clause license.
"""

from django import forms
from django.contrib.auth.models import User


class RegistrationForm(forms.ModelForm):

    first_name = forms.CharField(
        label="First name", max_length=30)
    last_name = forms.CharField(
        label="Last name", max_length=30)
    email = forms.EmailField(
        label="E-mail", max_length=254,
        widget=forms.TextInput)
    username = forms.RegexField(
        label="Username", regex=r'^[\w.@+-]{5,}$', max_length=30,
        help_text="Enter at least 5 characters (only alphanumerics|.|-|_)")
    password = forms.CharField(
        label="Password", min_length=5,
        widget=forms.PasswordInput(render_value=True),
        error_messages={
            'min_length': "Enter at least 5 characters.",
        },
        help_text="Enter at least 5 characters")
    password_conf = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput,
        help_text="Enter the same password as above, for verification")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']

    def clean_email(self):
        email = self.cleaned_data['email']

        if not User.objects.filter(email__exact=email).exists():
            return email

        raise forms.ValidationError("The e-mail is already in use.")

    def clean_username(self):
        username = self.cleaned_data['username']

        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username

        raise forms.ValidationError("The username is already registered.")

    def clean_password_conf(self):
        password1 = self.cleaned_data.get('password', None)
        password2 = self.cleaned_data['password_conf']

        if password1 and password1 == password2:
            return password2

        raise forms.ValidationError("The two passwords do not match.")

    def get_credentials(self):
        username = self.cleaned_data.get('username', None)
        password = self.cleaned_data.get('password', None)

        return {'username': username, 'password': password}

    def save(self, commit=True):
        instance = super(RegistrationForm, self).save(commit=False)

        if commit:
            instance.set_password(self.cleaned_data['password'])
            instance.save()

        return instance
