from django.shortcuts import render
from django.utils.safestring import mark_safe
from accounts.views import EmailListForm


def subscribe_form(request):
    if request.method == 'POST':
        subscribe_form = EmailListForm(request.POST)
        if subscribe_form.is_valid():
            subscribe_form = subscribe_form.save()

            return render(request, 'accounts/subscribe_done.html', {'name': subscribe_form.name})

    else:
        subscribe_form = EmailListForm()

    return {'subscribe_form': subscribe_form}
            
def base_view(request):
    # get user profile picture and make advailable to html
    profile_photo = False
    if request.user.is_authenticated and request.user.profile:
        photo_url = request.user.profile.photo.url 
        profile_photo = f"""<img  src="{ photo_url }" alt="John Doe" class="rounded-circle  mr-1" style="width:30px; height:30px;">"""
        profile_photo = mark_safe(profile_photo)

    return {'profile_photo': profile_photo}
