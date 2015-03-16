from django import forms
from core.models import *

class UploadApkForm(forms.ModelForm):

    class Meta:
        # Set this form to use the UploadApk Model
        model = UploadApk


class EditorForm(forms.Form):
	code = forms.CharField(widget=forms.Textarea(attrs={'rows':30, 'cols':80}))
