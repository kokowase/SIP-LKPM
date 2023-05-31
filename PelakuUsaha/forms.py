from django import forms
from .models import PelakuUsaha

class PelakuUsahaForm(forms.ModelForm):
    class Meta:
        model = PelakuUsaha
        fields = '__all__'
