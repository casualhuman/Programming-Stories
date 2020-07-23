from django.shortcuts import render
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
            