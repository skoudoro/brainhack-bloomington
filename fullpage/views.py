from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from fullpage.forms import RegistrationForm, ProspectForm
from django.contrib import messages


# Create your views here.
def index(request):
    context = {}
    if request.method == 'POST':
        submitted_form = ProspectForm(request.POST)
        if submitted_form.is_valid():
            submitted_form.save()
            return redirect('index')
        else:
            messages.error(request, submitted_form.errors)
            context['form'] = submitted_form
            return render(request, 'fullpage/index.html', context)

    else:
        form = ProspectForm()

    form = ProspectForm()
    context['form'] = form
    return render(request, 'fullpage/index.html', context)


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            # user.profile.birth_date = form.cleaned_data.get('birth_date')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = RegistrationForm()
    return render(request, 'fullpage/registration.html', {'form': form})