from django import forms
from gallery.models import Image


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('path_to_image', 'name')
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Title', 'class': 'form-control custom'})
        }
