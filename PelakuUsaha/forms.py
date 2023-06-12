from django import forms
from .models import PelakuUsaha

class PelakuUsahaForm(forms.ModelForm):
    class Meta:
        model = PelakuUsaha
        fields = '__all__'
        widgets = {
            'permasalahan': forms.Textarea(attrs={'rows': 5, 'cols': 40}),
        }
