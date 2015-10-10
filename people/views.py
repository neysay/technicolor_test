from django.shortcuts import render
from django.http import HttpResponse , HttpResponseRedirect
from .forms import UserCreationFormExtended
from .models import UserProfile
# Create your views here.


def home(request):

    """
    form = SignUpForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
    """
    form = {}
    context = {"form": form , "description":"Welcome"}
    return render(request, "home.html", context)


def register(request):

    if request.method == 'POST':
        userForm = UserCreationFormExtended(request.POST)
        #profileForm = RegistrationForm(request.POST)
        if userForm.is_valid():
            new_user = userForm.save()
            profile = UserProfile.objects.create(user=new_user,
                                                 city=userForm.cleaned_data['city'],
                                                 state=userForm.cleaned_data['state'])
            #new_user_profile = profileForm.save(new_user)
            return HttpResponseRedirect("/")
    else:
        userForm = UserCreationFormExtended()

    context = {"form": userForm}
    #return render(request, "registration/register.html", context)
    return render(request, "home.html", context)