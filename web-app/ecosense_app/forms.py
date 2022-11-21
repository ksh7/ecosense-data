from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from . import models

class ResearchAddForm(forms.ModelForm):
    class Meta:
        model = models.ResearchInsight
        fields = ('dataset', 'is_public', 'title', 'finding', 'description', 'attribution', 'graph_data_available', 'graph_data', 'data_sources')

class DataSourceForm(forms.ModelForm):
    class Meta:
        model = models.Dataset
        fields = (
            'topics',
        )
