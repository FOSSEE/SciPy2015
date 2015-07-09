from django.shortcuts import render
from django.utils.encoding import force_text
from django.contrib.contenttypes.models import ContentType
from django.template.context import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.admin.models import CHANGE
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail


from website.forms import ProposalForm, UserRegisterForm, UserLoginForm
from website.models import Proposal, Comments
from social.apps.django_app.default.models import UserSocialAuth
import random
import string


def userregister(request):
    context = {}
    context.update(csrf(request))
    registered_emails = []
    users = User.objects.all()
    for user in users:
        registered_emails.append(user.email)
    if request.user.is_anonymous():
        if request.method == 'POST':
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                if data['email'] in registered_emails:
                    context['form'] = form
                    context['email_registered'] = True
                    return render_to_response('user-register.html', context)
                else:
                    form.save()
                    context['registration_complete'] = True
                    return render_to_response('cfp.html', context)
            else:
                context.update(csrf(request))
                context['form'] = form
                return render_to_response('user-register.html', context)
        else:
            form = UserRegisterForm()
        context.update(csrf(request))
        context['form'] = form
        return render_to_response('user-register.html', context)
    else:
        context['user'] = request.user
        return HttpResponseRedirect('/2015/cfp')


def forgotpassword(request):
    context = {}
    user_emails = []
    context.update(csrf(request))
    if request.method == 'POST':
        users = User.objects.all()
        for user in users:
            user_emails.append(user.email)
        email = request.POST['email']
        if email == "":
            context['invalid_email'] = True
            return render_to_response("forgot-password.html", context)
        if email in user_emails:
            user = User.objects.get(email=email)
            password = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
            user.set_password(password)
            user.save()
            sender_name = "SciPy India 2015"
            sender_email = "scipy@fossee.in"
            subject = "SciPy India - Password Reset"
            to = (user.email, )
            message = """Dear """+user.first_name+""",\nYour password for SciPy India 2015 been reset. Your credentials are:\nUsername: """+user.username+"""\nPassword: """+password+"""\n\nWe recommend you to login with the given credentials & update your password immediately.\nLink to set new password: http://scipy.in/2015/update-password\n\nThank You !\n\nRegards,\n SciPy India,\nFOSSEE - IIT Bombay."""
            send_mail(subject, message, sender_email, to)
            form = UserLoginForm()
            context['form'] = form
            context['password_reset'] = True
            return render_to_response("cfp.html", context)
        else:
            context['invalid_email'] = True
            return render_to_response("forgot-password.html", context)
    else:
        return render_to_response('forgot-password.html', context)


def updatepassword(request):
    context = {}
    user = request.user
    context.update(csrf(request))
    if user.is_authenticated():
        if request.method == 'POST':
            new_password = request.POST['new_password']
            confirm = request.POST['confirm_new_password']
            if new_password == "" or confirm == "":
                context['empty'] = True
                return render_to_response("update-password.html", context)
            if new_password == confirm:
                user.set_password(new_password)
                user.save()
                context['password_updated'] = True
                logout(request)
                form = UserLoginForm()
                context['form'] = form
                return render_to_response("cfp.html", context)
            else:
                context['no_match'] = True
                return render_to_response("update-password.html", context)
        else:
            return render_to_response("update-password.html", context)
    else:
        form = UserLoginForm()
        context['form'] = form
        context['for_update_password'] = True
        return render_to_response('cfp.html', context)



def home(request):
    context = {}
    context.update(csrf(request))
    if request.method == "POST":
        sender_name = request.POST['name']
        sender_email = request.POST['email']
        to = ('scipy@fossee.in',)
        subject = "Query from - "+sender_name
        message = request.POST['message']
        try:
            send_mail(subject, message, sender_email, to)
            context['mailsent'] = True
        except:
            context['mailfailed'] = True
    return render_to_response('base.html', context)


def cfp(request):
    if request.method == "POST":
        context = {}
        context.update(csrf(request))
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if 'next' in request.GET:
                next = request.GET['next']
                return HttpResponseRedirect(next)
            context['user'] = user
            return render_to_response('cfp.html', context)
        else:
            context['invalid'] = True
            context['form'] = UserLoginForm
            return render_to_response('cfp.html', context)
    else:
        form = UserLoginForm()
        context = RequestContext(request, {'request': request,
                                           'user': request.user,
                                           'form': form})
        context.update(csrf(request))
        return render_to_response('cfp.html',
                             context_instance=context)


def submitcfp(request):
    context = {}
    if request.user.is_authenticated():
        social_user = request.user
        context.update(csrf(request))
        django_user = User.objects.get(username=social_user)
        context['user'] = django_user
        if request.method == 'POST':
            form = ProposalForm(request.POST, request.FILES)
            if form.is_valid():
                data = form.save(commit=False)
                data.user = django_user
                data.save()
                context['proposal_submit'] = True
                sender_name = "SciPy India 2015"
                sender_email = "scipy@fossee.in"
                subject = "SciPy India - Proposal Acknowledgment"
                to = (social_user.email, )
                message = """Dear """+django_user.first_name+""",\n\nThank you for showing interest & submitting a talk at SciPy India 2015 conference. We have received your proposal for the talk titled '"""+request.POST['title']+"""'.\nReviewal of the proposals will start once the CFP closes.\nYou will be notified regarding selection/rejection of your talk via email.\n\nThank You ! \n\nRegards,\nSciPy India 2015,\nFOSSEE - IIT Bombay"""
                send_mail(subject, message, sender_email, to)
                return render_to_response('cfp.html', context)
            else:
                context['proposal_form'] =  form
                return render_to_response('submit-cfp.html', context)
        else:
            form = ProposalForm()
            context['proposal_form'] = form
        return render_to_response('submit-cfp.html', context)
    else:
        context['login_required'] = True
        return render_to_response('cfp.html', context)
