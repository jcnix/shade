from django.contrib import auth
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template import RequestContext
import forms as myforms

def login(request):
    if not request.user.is_authenticated():
        form = myforms.LoginForm()
        if request.method == 'POST':
            form = myforms.LoginForm(request.POST)
            if form.is_valid():
                e = form.cleaned_data['email']
                p = form.cleaned_data['password']
                user = auth.authenticate(username=e, password=p)
                if user is not None:
                    auth.login(request, user)
                    return HttpResponseRedirect('/dashboard/')
                else:
                    form._errors['email'] = [u'Unable to authenticate']
                    return render(request, 'registration/login.html', {'form': form})

        return render(request, 'registration/login.html', {'form': form})
    else:
        return HttpResponseRedirect('/')

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/login/')

def register(request):
    if not request.user.is_authenticated():
        if request.method == 'POST':
            form = myforms.RegisterForm(request.POST)
            if form.is_valid():
                e = form.cleaned_data['email']
                p = form.cleaned_data['password']
                fn = form.cleaned_data['first_name']
                ln = form.cleaned_data['last_name']
                user = User.objects.create_user(
                        username=e,
                        email=e,
                        password=p
                        )
                user.first_name = fn
                user.last_name= ln
                user.save()
                return HttpResponseRedirect('/')
            else:
                return render_to_response('register.html', {'form': form},
                    context_instance=RequestContext(request))
        else:
            form = myforms.RegisterForm()
            return render_to_response('register.html', {'form': form},
                context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/')

