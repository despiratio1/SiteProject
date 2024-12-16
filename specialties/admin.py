from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib import admin
from django import forms

from specialties import models

class ContentPageAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = models.ContentPage
        fields = '__all__'


@admin.register(models.ContentPage)
class ContentPageAdmin(admin.ModelAdmin):
    form = ContentPageAdminForm
    list_display = ("title", )



