from django.shortcuts import render
from django.http import HttpResponse , HttpResponseRedirect
from .forms import UserCreationFormExtended , AuthenticationForm, SearchForm
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth import login as django_login, authenticate, logout as django_logout
from .models import UserProfile

# Create your views here.


def signupLogin(request):
    """
    Present a user creation form and a login form.
     -> Detect which form user is submitting from and then act accordingly

    if user is successfully logged in then redirect them to the home page , else
    return them to log in page

    :param request:
    :return:
    """
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
    return render(request, "login.html", context)


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
        #If request is a POST method , attempt login
        form, user, success = _login(request)
        if success:
            user_full_name = user.get_full_name()
    else:
        #Present form to user
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



def home(request):
    if not request.user.is_authenticated() or request.user.is_anonymous():
        #If we are either not an activated account or known user send to login screen
        return HttpResponseRedirect("/login")

    #Present Blank form , unless params have been passed in from url in which case search will attempt to execute
    searchForm = SearchForm(request.GET or None)

    userProfiles = []
    if searchForm.is_valid():
        #Run Search Query
        userProfiles = searchByCategory(searchForm,searchForm.cleaned_data['searchBy'],searchForm.cleaned_data['groupBy'])

    #Generate full name of logged in user for display purposes
    user_full_name = request.user.get_full_name() if not request.user.is_anonymous() else ""

    #Generate a list of possible fields for user profile objects
    fields = [x.name for x in UserProfile._meta.fields]

    context = {"searchForm": searchForm,"fields": fields,"query_results":userProfiles,"user_full_name":user_full_name}
    return render(request,'home.html',context)
    #return HttpResponse(message)

def searchByCategory(form,category="state",orderBy=""):
    """
    Using a given search form execute a query based on category and requested order/grouping if provided

    For the circumstances of the provided user profile data results are always the same as an order by.
    """

    #Validate that we are operating on a django form object
    assert isinstance(form,SearchForm)

    userProfiles = None
    if not orderBy:
        orderBy = category

    #Filter by category
    #MAINT:
    # This can be done better by generating the custom field name passed into filter
    # then we could remove the if/else cases.  Would need to spend sometime looking for
    # proper python syntax to accomplish this.  custom field name is not a string
    if category == "city" and form.cleaned_data['searchSelect']:
        userProfiles = UserProfile.objects.filter(city=form.cleaned_data['searchSelect']).annotate().order_by(orderBy)
    elif category == "state" and form.cleaned_data['searchSelect']:
        userProfiles = UserProfile.objects.filter(state=form.cleaned_data['searchSelect']).annotate().order_by(orderBy)
    elif category == "profession" and form.cleaned_data['searchSelect']:
        userProfiles = UserProfile.objects.filter(profession=form.cleaned_data['searchSelect']).annotate().order_by(orderBy)
    else:
        userProfiles = UserProfile.objects.all().annotate().order_by(orderBy)

    # I wasn't sure what expected results were with my criteria of city,state,job.  results would always be the same
    # as order by.  Something I could add is an aggregation on the whole set of returned userProfiles and them provide
    # a count field for distinct groupings.  i.e 5 people live in Los Angeles, 6 people live in NV, etc...

    return userProfiles



"""
def fileFinder(request):
    for file in os.listdir("/mydir"):
        if file.endswith(".txt"):
            print(file)
"""
#Helper methods

def _login(request):
    """
    Use POST data of the request to test authentication of the user
    """
    form = AuthenticationForm(data=request.POST)
    user = None
    success = False
    if form.is_valid():
        user,success = _loginUser(request,form.cleaned_data['username'],form.cleaned_data['password'])

    return form , user , success

def _loginUser(request,username,password):
    """
    Authenticate the user with name in password, return true if successful
    """
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            django_login(request, user)
            return user,True

def _register(request):
    """
    Use POST data of the request to create a new user account , then automatically log them in
    if there was no validation issues
    """
    form = UserCreationFormExtended(request.POST)
    user = None
    success = False
    if form.is_valid():
        newUser , userProfile = form.save()
        if not request.user.is_anonymous():
            logout(request)
        user, success = _loginUser(request,newUser.username,form.cleaned_data['password1'])

    return form , user , success
