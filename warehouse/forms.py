from django import forms
from warehouse.models import Rating

class RateForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rate',]
