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


from website.forms import ProposalForm
from website.models import Proposal, Comments
from social.apps.django_app.default.models import UserSocialAuth


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
    context = RequestContext(request, {'request': request,
                                       'user': request.user})
    return render_to_response('cfp.html',
                             context_instance=context)
                             

def userlogout(request):
    user = request.user
    if user.is_authenticated:
        logout(request)
        return HttpResponseRedirect("/cfp")
    else:
        return HttpResponseRedirect("/cfp")


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
