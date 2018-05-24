from django.shortcuts import render
from basic_app.forms import userprofileform, userform

from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request):
    return render(request,'basic_app/index.html')

def register(request):
    registered = False

    if request.method == "POST":
        user_form = userform(data=request.POST)
        userprofile_form = userprofileform(data=request.POST)

        if user_form.is_valid() and userprofile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = userprofile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()
            registered = True

        else:
            print (user_form.errors, userprofile_form.errors)
    else:
        user_form = userform()
        userprofile_form = userprofileform()

    return render(request,'basic_app/register.html',
                          {'user_form':user_form,
                           'profile_form':userprofile_form,
                           'registered':registered})

def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Accout not active")
        else:
            print("Someone tried to login and failed")
            print("username {} and password {}".format(username,password))
            return HttpResponse("Invalid Login")
    else:
        return render(request,'basic_app/login.html',{})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required
def special(request):
    return HttpResponse("You are logged in")
