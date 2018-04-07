from django.contrib import admin
from fullpage.models import ServiceBox, Workshop,\
    Conference, Profile, Speaker, Prospect

admin.site.register(ServiceBox)
admin.site.register(Workshop)
admin.site.register(Conference)
admin.site.register(Profile)
admin.site.register(Speaker)
admin.site.register(Prospect)

"""from fullpage.models import FullPage, Section, slides

class FullpageInline(admin.StackedInline):
    model = Section
    extra = 1


class FullpageAdmin(admin.ModelAdmin):
    inlines = [
        FullpageInline
        ]


class SectionInline(admin.StackedInline):
    model = slides
    extra = 1

class SectionAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    inlines = [
        SectionInline
        ]


class SlideAdmin(admin.ModelAdmin):
    list_filter = ('section',)
    search_fields = ('name', 'content',)

admin.site.register(FullPage, FullpageAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(slides)"""
