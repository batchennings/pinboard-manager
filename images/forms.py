from django import forms
from .models import Image

class TagsForm(forms.Form):
    tags = forms.CharField(label="Tags", max_length=256)
