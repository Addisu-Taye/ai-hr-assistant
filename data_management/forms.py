from django import forms
from .models import HRData

class UploadDataForm(forms.ModelForm):
    class Meta:
        model = HRData
        fields = ['data_file']