from django import forms
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.core.validators import validate_email
from django.contrib.auth.forms import UserCreationForm
from website.models import Proposal



class ProposalForm(forms.ModelForm):
    class Meta:
        model = Proposal
        exclude = ('user', )

    def clean_attachment(self):
        cleaned_data = self.cleaned_data
        attachment = cleaned_data.get('attachment', None)
        if attachment:
            if not attachment.name.endswith('.pdf'):
                raise forms.ValidationError('Only [.pdf] files are allowed')
            elif attachment.size > (5*1024*1024):
                raise forms.ValidationError('File size exceeds 5MB')
        return attachment


class UserRegisterForm(UserCreationForm):
	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'email', 'username', 'password1',
		          'password2')


class UserLoginForm(forms.Form):
    username = forms.CharField(
			widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}), 
			label=''
		)
    password = forms.CharField(
			widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}), 
			label=''
		)
