'''
Created on Oct 9, 2015

@author: jacobmelvin
'''
from django import forms
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile


class UserCreationFormExtended(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeHolder':'Enter Password'}), label='')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeHolder':'Confirm Password'}), label='')
    city = forms.CharField(widget=forms.TextInput(attrs={'placeHolder':'City'}), label='')
    state = forms.CharField(widget=forms.TextInput(attrs={'placeHolder':'State'}), label='')

    def __init__(self, *args, **kwargs):
        super(UserCreationFormExtended, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True


        self.fields['username'].widget = forms.TextInput(attrs={'placeholder': 'username'})
        self.fields['email'].widget = forms.TextInput(attrs={'placeholder': 'Email'})
        self.fields['first_name'].widget = forms.TextInput(attrs={'placeholder': 'First Name'})
        self.fields['last_name'].widget = forms.TextInput(attrs={'placeholder': 'Last Name'})

        self.fields['username'].label = ""
        self.fields['email'].label = ""
        self.fields['first_name'].label = ""
        self.fields['last_name'].label = ""

        self.helper = FormHelper(self)
        self.helper.form_method = 'POST'
        self.helper.layout = Layout('username',
                                    'email',
                                    'first_name',
                                    'last_name',
                                    'city',
                                    'state',
                                    'password1',
                                    'password2',
                                    Submit('submit','Sign Up',css_class='btn-primary')
                                    )


    class Meta:
       model = User
       fields = ('username', 'email', 'first_name', 'last_name')


    def clean_email(self):
        email = self.cleaned_data['email']
        email_base, provider = email.split("@")
        domain, extension = provider.split('.')

        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            print
            print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
            print "ATTEMPTING TO RAISE VALIDATION ERROR"
            print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
            print
            raise forms.ValidationError(u'Username "%s" is already in use.' % username,code='invalid')
        return username

    def clean(self):
        """
        Verifies that the values entered into the password fields match

        NOTE: Errors here will appear in ``non_field_errors()`` because it applies to more than one field.
        """
        #cleaned_data = super(RegistrationForm, self).clean()
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError("Passwords don't match. Please enter both fields again.")
        return self.cleaned_data


    def save(self, commit=True):
            newUser = super(UserCreationFormExtended, self).save(commit=False)
            newUser.email = self.cleaned_data["email"]
            newUser.set_password(self.cleaned_data['password1'])
            newUser.first_name = self.cleaned_data['first_name']
            newUser.last_name = self.cleaned_data['last_name']
            newUser.username = self.cleaned_data['username']

            profile = None
            if commit:
                newUser.save()
                profile = UserProfile.objects.create(user=newUser,
                                                 city=self.cleaned_data['city'],
                                                 state=self.cleaned_data['state'])

            return newUser , profile



class AuthenticationForm(forms.Form):
    """
    Login form
    """
    username = forms.CharField(widget=forms.widgets.TextInput(attrs={'placeHolder':'username'}),label='')
    password = forms.CharField(widget=forms.widgets.PasswordInput(attrs={'placeHolder':'Enter Password'}),label='')



    def __init__(self, *args, **kwargs):
        super(AuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].required = True
        self.fields['password'].required = True

        self.helper = FormHelper(self)
        self.helper.form_method = 'POST'
        self.helper.layout = Layout('username',
                                    'password',
                                    Submit('submit','Login',css_class='btn-primary')
                                    )


    class Meta:
        fields = ['username', 'password']