from django import forms
from .models import Composition

class CompositionForm(forms.ModelForm):
    class Meta:
        model = Composition
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'album': forms.Select(attrs={'class': 'form-select'}),
            'genre': forms.Select(attrs={'class': 'form-select'}),
            'duration': forms.TimeInput(format='%H:%M:%S', attrs={'class': 'form-control', 'type': 'time'}),
            'audio_file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }