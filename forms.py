from django import forms
from .models import Composition

class CompositionForm(forms.ModelForm):
    class Meta:
        model = Composition
        fields = ['title', 'album', 'genre', 'duration', 'audio_file']  # не обязательно все, можно меньше
