from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages 
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login as dj_login
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm, EmailListForm
from accounts.models import EmailList
from pages.templates.pages import page 
from .models import Profile
import random


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

            # select a random image as a temp profile picture 
            image_route = 'users/profile_pics/1.png'
            image_route_list = image_route.split('1', 1)
            image_route_list[0] = image_route_list[0] + str(random.randint(1, 3)) 
            image_route = ''.join(image_route_list)

            # create profile then add user to "email-list"
            Profile.objects.create(user=register_form, photo=image_route)
            EmailList.objects.create(name=cd['username'], email=cd['email'])
            

            return render(request, 
                            'registration/registration_done.html',
                            {'new_user': register_form})

    else:
        register_form = UserRegistrationForm() 

    return render(request,
                'registration/registration_form.html',
                {'register_form': register_form})



def profile(request):
    success = 'empty'
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)

        profile_form = ProfileEditForm(instance=request.user.profile,
                                        data=request.POST,
                                        files=request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
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
    return render(request, 'accounts/subscribe.html')


