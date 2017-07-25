from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Problem

from ckeditor.fields import RichTextField


class ProblemText(forms.ModelForm):
    class Meta:
        model = Problem
        fields = ['statement']
        labels = {
            'statement': _(''),
        }
