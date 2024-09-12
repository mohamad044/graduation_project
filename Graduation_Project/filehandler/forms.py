from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField()


"""

from django import forms

class FileUploadForm(forms.Form):
    file = forms.FileField(label='Select a file')


"""