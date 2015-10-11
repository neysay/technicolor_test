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

    return render(request, "home.html", context)


def register(request):
    if request.method == 'POST':
        userForm = UserCreationFormExtended(request.POST)
        if userForm.is_valid():
            newUser , userProfile = userForm.save()
            if not request.user.is_anonymous():
                logout(request)
            _loginUser(request,userForm.cleaned_data['username'],userForm.cleaned_data['password1'])

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
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user,success = _loginUser(request,form.cleaned_data['username'],form.cleaned_data['password'])
            if success:
                user_full_name = user.get_full_name()
            """
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            if user is not None:
                if user.is_active:
                    django_login(request, user)
                    print "LOGIN SUCESSFUL"
                    return redirect('/')
            else:
                print "LOGIN FAILURE, TRY AGAIN"
            """
    else:
        form = AuthenticationForm()
    return render_to_response('home.html', {
        'form': form,"user_full_name":user_full_name
    }, context_instance=RequestContext(request))


def _loginUser(request,username,password):
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            django_login(request, user)
            print "LOGIN SUCCESSFUL"
            return user,True


    print "LOGIN FAILURE"
    return user,False

def logout(request):
    """
    Logout View

    :param request:
    :return:

    """

    django_logout(request)
    return redirect('/')