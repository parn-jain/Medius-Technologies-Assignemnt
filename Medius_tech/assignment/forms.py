from django import forms

class FileUploadForm(forms.Form):
    file = forms.FileField(label='Choose a file')