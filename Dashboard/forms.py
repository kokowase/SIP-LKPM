from django import forms

class SearchDataForm(forms.Form):
    nib = forms.CharField(max_length=100,required=False)
    kecamatan = forms.CharField(max_length=100,required=False)

class PickDateForm(forms.Form):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    