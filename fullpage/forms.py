from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from fullpage.models import Profile


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    affiliation = forms.CharField(max_length=30, required=True, help_text='Required.')
    email = forms.EmailField(max_length=254, help_text='Required.')
    need_parking = forms.ChoiceField(choices = Profile.BOOL_CHOICES, label="Do you need a parking pass?",
                                     initial='False', widget=forms.Select(), required=False,
                                     help_text='Optional.')
    area_of_interest = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                                 label="What is your area of interest?",
                                                 required=True,
                                                 help_text='Required.',
                                                 choices=Profile.INTEREST_CHOICES)
    project_idea =  forms.CharField(label="Do you have a specific project in mind that you would like to work on during the Brainhack? Please describe.",
                                    widget=forms.Textarea,
                                    required=False,
                                    help_text='Optional.')
    code_level = forms.MultipleChoiceField(widget=forms.RadioSelect,
                                           label="What is your programming experience?",
                                           required=True,
                                           choices=Profile.CODE_CHOICES)
    code_favorite = forms.MultipleChoiceField(widget=forms.RadioSelect,
                                              label="What is your favorite programming language?",
                                              required=True,
                                              choices=Profile.CODE_FAVORITE_CHOICES, )
    academic_level  = forms.MultipleChoiceField(widget=forms.RadioSelect,
                                                label="What is your academic level?",
                                                required=True,
                                                choices=Profile.ACADEMIC_CHOICES, )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'affiliation', 'email', 'password1', 'password2', )
