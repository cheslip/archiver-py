from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import HttpResponseRedirect, render_to_response
from django.template import RequestContext
from employee.forms import LoginForm

def LoginRequest(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/single/')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            employee = authenticate(username=username, password=password)
            if employee is not None:
                login(request, employee)
                return HttpResponseRedirect('/single/')
            else:
                return render_to_response('auth.html', {'form':form}, context_instance=RequestContext(request))
        else:
            return render_to_response('auth.html', {'form':form}, context_instance=RequestContext(request))

    else:
        form = LoginForm()
        context = { 'form' : form }
        return render_to_response('auth.html', context, context_instance=RequestContext(request))

def LogoutRequest(request):
    logout(request)
    return HttpResponseRedirect('/login/')
