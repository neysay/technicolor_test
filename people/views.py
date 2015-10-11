from django.shortcuts import render
from django.http import HttpResponse , HttpResponseRedirect
from .forms import UserCreationFormExtended , AuthenticationForm
#from .models import UserProfile
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth import login as django_login, authenticate, logout as django_logout
# Create your views here.


def home(request):

    form = {}
    user_full_name = request.user.get_full_name() if not request.user.is_anonymous() else ""
    context = {"form": form , "user_full_name":user_full_name}
    if not request.user.is_authenticated() or request.user.is_anonymous():
        return HttpResponseRedirect("/login")

    return render(request, "home.html", context)

def signupLogin(request):

    success = False
    #user = request.user
    if request.method == 'POST':
        if request.POST['submit'] == "Login":
            loginForm, user, success = _login(request)
            signupForm = UserCreationFormExtended()
        else:
            signupForm, user, success = _register(request)
            loginForm = AuthenticationForm()
    else:
        signupForm = UserCreationFormExtended()
        loginForm = AuthenticationForm()

    if success:
        return HttpResponseRedirect("/")

    user_full_name = request.user.get_full_name() if not request.user.is_anonymous() else ""

    context = {"signup": signupForm, "login":loginForm, "user_full_name":user_full_name}
    #return render(request, "registration/register.html", context)
    return render(request, "registration/login.html", context)


def register(request):
    if request.method == 'POST':
        userForm, user, success = _register(request)
        if success:
            return HttpResponseRedirect("/")
    else:
        userForm = UserCreationFormExtended()

    user_full_name = request.user.get_full_name() if not request.user.is_anonymous() else ""

    context = {"form": userForm, "user_full_name":user_full_name}
    #return render(request, "registration/register.html", context)
    return render(request, "home.html", context)


def login(request):
    """
    Log in view
    """
    user_full_name = ""
    if request.method == 'POST':
        form, user, success = _login(request)
        if success:
            user_full_name = user.get_full_name()
    else:
        form = AuthenticationForm()
    return render_to_response('home.html', {
        'form': form,"user_full_name":user_full_name
    }, context_instance=RequestContext(request))



def logout(request):
    """
    Logout View

    :param request:
    :return:

    """
    django_logout(request)
    return redirect('/login')





#Helper methods

def _login(request):
    form = AuthenticationForm(data=request.POST)
    user = None
    success = False
    if form.is_valid():
        user,success = _loginUser(request,form.cleaned_data['username'],form.cleaned_data['password'])

    return form , user , success

def _loginUser(request,username,password):
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            django_login(request, user)
            print "LOGIN SUCCESSFUL"
            return user,True

def _register(request):
    form = UserCreationFormExtended(request.POST)
    user = None
    success = False
    if form.is_valid():
        newUser , userProfile = form.save()
        if not request.user.is_anonymous():
            logout(request)
        user, success = _loginUser(request,newUser.username,form.cleaned_data['password1'])

    return form , user , success
