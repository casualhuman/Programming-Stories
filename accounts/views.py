from django.shortcuts import render
from django.http import HttpResponse
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm, EmailListForm
from django.contrib import messages 
from django.contrib.auth import authenticate, login as dj_login
from .models import Profile
from pages.templates.pages import page 
from django.contrib.auth.views import LoginView
from accounts.models import EmailList

class CustomLoginView(LoginView):
    form_class = LoginForm
    

def user_registration(request):

    if request.method=='POST':
        register_form = UserRegistrationForm(request.POST)

        if register_form.is_valid():
            # Get all the info from form 
            # Save the form but not directly in the db
            # add the password to the db

            cd = register_form.cleaned_data 
            register_form = register_form.save(commit=False) 
            register_form.set_password(cd['password1']) 
            register_form.save()
            
            EmailList.objects.create(name=cd['username'], email=cd['email'])
            Profile.objects.create(user=register_form)

            return render(request, 
                            'registration/registration_done.html',
                            {'new_user': register_form})

    else:
        register_form = UserRegistrationForm() 

    return render(request,
                'registration/registration_form.html',
                {'register_form': register_form})



def profile(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)

        profile_form = ProfileEditForm(instance=request.user.profile,
                                        data=request.POST,
                                        files=request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            # # display a success message
            # message.success('Profile updated successfully')
            success = True

        else:
            success = False


    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(request, 'accounts/profile.html',{'user_form': user_form,
                                                    'profile_form': profile_form,
                                                    'success': success})


def subscribe(request):
    return render(request, 'accounts/subscribe.html',)


