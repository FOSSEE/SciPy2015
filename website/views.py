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
    return render_to_response('down.html')
    if request.method == "POST":
        return HttpResponse("Working")
    return render_to_response('base.html')
    

def contact(request):
    context = {}
    return HttpResponse("Reached Here")
    if request.method == "POST":
        sender_name = request.POST['name']
        sender_email = request.POST['email']
        query = request.POST['message']
        to = ('scipy@fossee.in',)
        subject = "Query from - "+sender_name
        message = form['message']
        send_mail(subject, message, sender_email, to, fail_silently=True)
        context['mailsent'] = True
        return render(request, 'base.html', context)
    else:
        return HttpResponseRedirect('/')
