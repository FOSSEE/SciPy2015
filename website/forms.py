from django import forms
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import validate_email

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
