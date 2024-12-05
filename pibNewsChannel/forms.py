from django import forms  # Ensure this line is present
from .models import PibVideo  # Correct model name with capitalization

class VideoDescriptionForm(forms.ModelForm):
    class Meta:
        model = PibVideo
        fields = ['description']
        widgets = {
            'description': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter video description here...',
                'rows': 4, 
                'cols': 50
            }),
        }
