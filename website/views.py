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
from django.core.mail import send_mail


def home(request):
    context = {}
    if 'query' in request.GET:
        context['query'] = True
    context.update(csrf(request))
    if request.method == "POST":
        return HttpResponse("Working")
    return render_to_response('base.html', context)
    

def contact(request):
    context = {}
    context.update(csrf(request))
    if request.method == "POST":
        sender_name = request.POST['name']
        sender_email = request.POST['email']
        query = request.POST['message']
        to = ('hardythe1@gmail.com',)
        subject = "Query from - "+sender_name
        message = request.POST['message']
        send_mail(subject, message, sender_email, to, fail_silently=True)
        context['mailsent'] = True
        return HttpResponseRedirect('/?query=sent')
    else:
        return HttpResponseRedirect('/')
