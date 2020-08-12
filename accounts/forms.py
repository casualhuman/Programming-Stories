from django.contrib.auth.models import User 
from django import forms
from .models import Profile, EmailList
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    error_messages = {
        'invalid_login':_('Sorry Check Again '),
        'inactive':_('banned')
    }

    username = forms.CharField(label='',
                                widget=forms.TextInput(
                                    attrs = {
                                       'placeholder': 'username or email',
                                       }
                               ))

    password = forms.CharField(label='', 
                                widget=forms.PasswordInput(
                                    attrs = {
                                        'placeholder': 'Password'
                                    }
                                )
                                )

    
User._meta.get_field('email').blank = False
User._meta.get_field('email')._unique = True 


class UserRegistrationForm(forms.ModelForm):

    password1 = forms.CharField(label='', 
                                widget=forms.PasswordInput(attrs={
                                    'placeholder': 'Password'})
                                )

    password2 = forms.CharField(label='',
                                widget=forms.PasswordInput(attrs={
                                    'placeholder': 'Confirm Password'})
                                )

    error_messages = {
        'duplicate_username': ("username taken :("),
        'duplicate_email': ("email signed up ")
        }


    class Meta:
        model = User
        fields = ('username', 'email')
        widgets = {
            'username': forms.TextInput(attrs = {'cols': 1, 'rows': 8, 'placeholder':'username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}, ),

        }
        labels = {
            'username': _(''),
            'email': _(''),
            
        }

        help_texts ={
            'username': None 
        }

       
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError("passwords don't match")

        return cd['password1']

    def clean_username(self):
        username = self.cleaned_data["username"]
        if self.instance.username == username:
            return username
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(
            self.error_messages['duplicate_username'],
            code='duplicate_username',
        )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError(self.error_messages['duplicate_email'])
            
        return email
        

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('photo',)


class EmailListForm(forms.ModelForm):
    class Meta:
        model = EmailList
        fields = ('name', 'email',)
