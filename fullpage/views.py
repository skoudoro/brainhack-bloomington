from django.shortcuts import render
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