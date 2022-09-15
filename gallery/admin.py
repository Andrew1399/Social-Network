from django import forms
from django.contrib import admin
from gallery.models import Image


class AdminForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('path_to_image', 'name', 'datetime', 'author')


@admin.register(Image)
class AdminModel(admin.ModelAdmin):
    form = AdminForm
    list_display = ('name', 'datetime', 'size', 'author')

    def save_model(self, request, obj, form, change):
        form.instance.size = request.FILES['path_to_image'].size
        return super().save_model(request, obj, form, change)

