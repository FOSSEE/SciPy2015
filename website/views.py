from django.shortcuts import render
from django.utils.encoding import force_text
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf
from django.contrib.auth import authenticate, login, logout
from django.contrib.admin.models import CHANGE
from django.contrib.auth.decorators import login_required


def home(request):
    return render_to_response('base.html')
