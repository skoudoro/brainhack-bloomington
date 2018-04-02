from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from fullpage.forms import RegistrationForm

#from fullpage.models import Section, FullPage, slides as Slides

# Create your views here.
def index(request):
    # fullpage = FullPage.objects.all()[0]
    # sections = Section.objects.all()
    # slides = Slides.objects.all()
    return render(request, 'fullpage/index.html',
            # {
            #     'fullpage' : fullpage,
            #     'sections' : sections,
            #     'slides' : slides,
            # }
        )


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