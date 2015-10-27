from django.db import models
from django.contrib.auth.models import User

from social.apps.django_app.default.models import UserSocialAuth
from scipy2015 import settings

def get_document_dir(instance, filename):
    return '%s/attachment/%s' % (instance.user, filename)

class Proposal(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=1024, help_text='Title of your Talk')
    abstract = models.TextField(max_length=1024, help_text='Abstract of your Talk')
    content_link = models.CharField(max_length=1024, help_text='Link to the content of your Talk')
    speaker_link = models.CharField(max_length=1024, help_text='Link to information about the Speaker')
    bio = models.TextField(max_length=512, help_text='A short description about you')
    attachment = models.FileField(upload_to=get_document_dir)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    contact_number = models.IntegerField(max_length=10)
    def __unicode__(self):
        name = self.user.username
        return '%s'%(name)


class Comments(models.Model):
    proposal = models.ForeignKey(Proposal)
    user = models.ForeignKey(User)
    comment = models.CharField(max_length=700)
