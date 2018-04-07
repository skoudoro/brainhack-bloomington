
import datetime

from colorfield.fields import ColorField
# from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.contrib.auth.models import User
from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

import markdown
import bleach


# markdown allowed tags that are not filtered by bleach

allowed_html_tags = bleach.ALLOWED_TAGS + ['p', 'pre', 'table', 'img',
                                           'h1', 'h2', 'h3', 'h4', 'h5',
                                           'h6', 'b', 'i', 'strong', 'em',
                                           'tt', 'br', 'blockquote',
                                           'code', 'ul', 'ol', 'li',
                                           'dd', 'dt', 'a', 'tr', 'td',
                                           'div', 'span', 'hr']

allowed_attrs = ['href', 'class', 'rel', 'alt', 'class', 'src', 'id']

TRUE_FALSE_CHOICES = (
    (True, 'Yes'),
    (False, 'No')
)


class ServiceBox(models.Model):
    title = models.CharField('title', max_length=100)
    box_color = ColorField('separator color', default='', blank=True)
    short_description = models.TextField()
    description = models.TextField()
    order = models.IntegerField(blank=True, default=99)
    is_visible = models.BooleanField('is visible?', default=True, help_text='')

    created = models.DateTimeField(editable=False, auto_now_add=True)
    modified = models.DateTimeField(editable=False, auto_now_add=True)

    def save(self, *args, **kwargs):
        self.modified = datetime.datetime.now()

        # clear the cache
        cache.clear()

        # Call the "real" save() method.
        super(ServiceBox, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Workshop(models.Model):
    title = models.CharField('title', max_length=100)
    sep_color = ColorField('separator color', default='', blank=True)
    background_image = models.ImageField('background image', upload_to='workshop_images/', default='', blank=True)
    is_thumbnail = models.BooleanField('is thumbnail?', default=False, help_text='')
    is_visible = models.BooleanField('is visible?', default=True, help_text='')
    body_markdown = models.TextField(null=True, blank=True)
    body_html = models.TextField(editable=False)

    created = models.DateTimeField(editable=False, auto_now_add=True)
    modified = models.DateTimeField(editable=False, auto_now_add=True)

    def save(self, *args, **kwargs):
        html_content = markdown.markdown(self.body_markdown, extensions=['codehilite'])

        # bleach is used to filter html tags like <script> for security
        self.body_html = bleach.clean(html_content, allowed_html_tags,
                                      allowed_attrs)
        self.modified = datetime.datetime.now()

        # clear the cache
        cache.clear()

        # Call the "real" save() method.
        super(Workshop, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Conference(models.Model):
    title = models.CharField('title', max_length=100)
    background_image = models.ImageField('background image', upload_to='images/', default='', blank=True)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=timezone.now()+timezone.timedelta(hours=1))
    registration_deadline = models.DateTimeField(default=timezone.now)
    city = models.CharField('City', max_length=100, default="Bloomington")
    states = models.CharField('State', max_length=100, default="IN")
    country = models.CharField('country', max_length=100, default="USA")
    standard_price = models.IntegerField(blank=True, default=100)
    student_price = models.IntegerField(blank=True, default=60)
    what_is_title = models.CharField('slide name', max_length=100, default="What is BrainHack?")
    what_is_description = models.TextField(null=True, blank=True)
    what_is_html = models.TextField(editable=False)
    what_is_image = models.ImageField('What is image', upload_to='images/', default='', blank=True)

    created = models.DateTimeField(editable=False, auto_now_add=True)
    modified = models.DateTimeField(editable=False, auto_now_add=True)

    def save(self, *args, **kwargs):
        html_content = markdown.markdown(self.what_is_description, extensions=['codehilite'])

        # bleach is used to filter html tags like <script> for security
        self.what_is_html = bleach.clean(html_content, allowed_html_tags,
                                         allowed_attrs)
        self.modified = datetime.datetime.now()

        # clear the cache
        cache.clear()

        # Call the "real" save() method.
        super(Conference, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Profile(models.Model):
    BOOL_CHOICES = ((True, 'Yes'), (False, 'No'))
    INTEREST_CHOICES = ((1, 'Brain Computer Interfaces'), (2,'MRI'), (3,'EEG & MEG'), (4,'PET'), (5, 'Network Science'),
                        (6, 'Machine Learning'), (7, 'Statistical Analysis'), (8, 'Other'))
    ACADEMIC_CHOICES = ((1, 'Professor'), (2, 'Postdoc'), (1, 'PhD student'), (2, 'Master student'),
                        (1, 'BSc Student'), (2, 'Other'))
    CODE_CHOICES = ((1, 'Novice'), (2, 'Intermediate'), (3, 'Advanced'))
    CODE_FAVORITE_CHOICES = ((1, 'C / C++'), (2, 'Python'), (3, 'Matlab'), (4, 'Javascript'), (5, 'Other'))

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    affiliation = models.CharField('Affiliation', max_length=100, default="Indiana University")
    need_parking = models.BooleanField(choices=BOOL_CHOICES, default=BOOL_CHOICES[1][0])
    area_of_interest = models.CharField(max_length=200, choices=INTEREST_CHOICES, blank=True, null=True)
    project_idea = models.TextField(null=True, blank=True)
    code_level = models.CharField(max_length=200, choices=CODE_CHOICES, default=1)
    code_favorite = models.CharField(max_length=200, choices=CODE_FAVORITE_CHOICES, default=1)
    academic_level  = models.CharField(max_length=200, choices=ACADEMIC_CHOICES, default=1)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance,
                               )
    instance.profile.save()


class Speaker(models.Model):
    profile = models.ForeignKey(Profile, verbose_name='profile')
    title = models.CharField('title', max_length=100)
    abstract_markdown = models.TextField(null=True, blank=True)
    abstract_html = models.TextField(editable=False)

    created = models.DateTimeField(editable=False, auto_now_add=True)
    modified = models.DateTimeField(editable=False, auto_now_add=True)

    def save(self, *args, **kwargs):
        html_content = markdown.markdown(self.abstract_markdown, extensions=['codehilite'])

        # bleach is used to filter html tags like <script> for security
        self.abstract_html = bleach.clean(html_content, allowed_html_tags,
                                          allowed_attrs)
        self.modified = datetime.datetime.now()

        # clear the cache
        cache.clear()

        # Call the "real" save() method.
        super(Speaker, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Prospect(models.Model):
    mail = models.EmailField(null=True, blank=True, default=" Enter you email to stay tuned")

    def __str__(self):
        return self.mail