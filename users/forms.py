from django import forms
from users.models import Profile


class ProfileModelForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'status', 'country', 'bio', 'image')
