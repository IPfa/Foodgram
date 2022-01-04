from .models import Tag
from .widgets import ColorPicker
from django import forms


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        widgets = {
            'color': ColorPicker,
        }
        fields = '__all__'
