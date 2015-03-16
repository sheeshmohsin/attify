from django import forms
from core.models import *

class UploadApkForm(forms.ModelForm):

    class Meta:
        # Set this form to use the UploadApk Model
        model = UploadApk
        
