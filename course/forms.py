from django import forms
from django.contrib.auth.forms import UserCreationForm
from multiupload.fields import MultiFileField

from .models import UserProfile, Course


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'user_type',)


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'total_hours']

    files = MultiFileField(min_num=1, max_num=5, max_file_size=1024*1024*5)
