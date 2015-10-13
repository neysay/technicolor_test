'''
Created on Oct 9, 2015

@author: jacobmelvin
'''
from django import forms
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile
from django.contrib.auth import authenticate


class UserCreationFormExtended(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeHolder':'Enter Password'}), label='')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeHolder':'Confirm Password'}), label='')
    city = forms.CharField(widget=forms.TextInput(attrs={'placeHolder':'City'}), label='')
    state = forms.CharField(widget=forms.TextInput(attrs={'placeHolder':'State'}), label='')
    profession = forms.CharField(widget=forms.TextInput(attrs={'placeHolder':'Job'}), label='')

    def __init__(self, *args, **kwargs):
        """
        Setup user creation form.
        Add crispyforms layout helper for html management
        """
        super(UserCreationFormExtended, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['username'].widget = forms.TextInput(attrs={'placeholder': 'username'})
        self.fields['email'].widget = forms.EmailInput(attrs={'placeholder': 'Email'})
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
                                    Div(
                                        Div('first_name',css_class='col-md-6'),
                                        Div('last_name',css_class='col-md-6'),
                                        css_class='row'
                                    ),
                                    Div(
                                        Div('city',css_class='col-xs-9'),
                                        Div('state',css_class='col-xs-3'),
                                        css_class='row'
                                    ),
                                    'profession',
                                    'password1',
                                    'password2',
                                    Submit('submit','Sign Up',css_class='btn-primary')
                                    )

    class Meta:
        #Overide class definition
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def clean_username(self):
        """
        Validate username is not already in use
        :return: String , users name
        """
        username = self.cleaned_data['username']
        if User.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            raise forms.ValidationError(u'Username "%s" is already in use.' % username,code='invalid')

        return username

    def clean(self):
        """
        Verifies that the values entered into the password fields match

        NOTE: Errors here will appear in ``non_field_errors()`` because it applies to more than one field.
        :return: {}, dictionary with forms validated data
        """
        #cleaned_data = super(RegistrationForm, self).clean()
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError("Passwords don't match. Please enter both fields again.")
        return self.cleaned_data


    def save(self, commit=True):
        """
        Customize save method on form.
        Pass in User object based data then save User model.
        After user model is saved add that user model foriegn key to newly
        generated UserProfile model.

        :return: django.contrib.auth.models.User , .models.UserProfile
        """
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
                                                 state=self.cleaned_data['state'],
                                                 profession=self.cleaned_data['profession'])

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

    """
    def clean_username(self):
        username = self.cleaned_data['username']
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError(u'Username "%s" Does not exist, please register username' %
                                        username,code='invalid')

        return username
    """

    def clean(self):
        """
        Verifies that the values entered into the password fields match

        NOTE: Errors here will appear in ``non_field_errors()`` because it applies to more than one field.
        """

        if 'username' in self.cleaned_data and 'password' in self.cleaned_data:
            user = authenticate(username=self.cleaned_data['username'], password=self.cleaned_data['password'])
            if user is None or not user.is_active:
                raise forms.ValidationError(u'username or password is invalid', code='invalid')


        return self.cleaned_data




class SearchForm(forms.Form):

    CATEGORIES = (
        ('city', "City"),
        ('state',"State"),
        ('profession',"Profession")
    )
    searchBy = forms.ChoiceField(label="Search By:",choices=CATEGORIES)
    searchSelect = forms.CharField(widget=forms.widgets.TextInput(attrs={'placeHolder':'search by name'}),label="")
    groupBy = forms.ChoiceField(label="Group By:",choices=CATEGORIES)
    #groupSelect = forms.CharField(widget=forms.widgets.TextInput(attrs={'placeHolder':'order by name'}),label="")

    def __init__(self, *args, **kwargs):

        super(SearchForm, self).__init__(*args, **kwargs)
        self.fields['searchSelect'].required = False
        #self.fields['groupSelect'].required = False


        self.helper = FormHelper(self)
        self.helper.form_method = 'POST'
        """
        self.helper.layout = Layout(
                                    Div(
                                        Div('searchBy',css_class='col-md-3'),
                                        Div('searchSelect',css_class='col-md-9'),
                                        css_class='row'
                                    ),
                                    Div(
                                        Div('groupBy',css_class='col-md-3'),
                                        Div('groupSelect',css_class='col-md-9'),
                                        css_class='row'
                                    ),
                                    Submit('search','Search',css_class='btn-primary')
                                    )
        """
        self.helper.layout = Layout('searchBy',
                                    'searchSelect',
                                    'groupBy',
                                    #'groupSelect',
                                    Submit('search','Search',css_class='btn-primary'),

                                    )

    class Meta:
        fields = ('searchBy', 'searchSelect', 'groupBy')


    def clean(self):
        """
        Verifies that the values entered into the password fields match

        NOTE: Errors here will appear in ``non_field_errors()`` because it applies to more than one field.
        """
        #validSearch = ['city','state']
        #if 'searchBy' in self.cleaned_data and 'groupBy' in self.cleaned_data:
        #    if not self.cleaned_data['searchBy'] in validSearch:
        #        raise forms.ValidationError(u'%s is not a valid search category' %
        #                                    (self.cleaned_data['searchBy']), code='invalid')


        return self.cleaned_data