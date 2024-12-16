from ckeditor.fields import RichTextField
from django.db import models
from django.utils.translation import gettext_lazy as _


class ContentPage(models.Model):
    class Meta:
        verbose_name = _("страница с содержимым")
        verbose_name_plural = _("страницы с содержимым")

    title = models.CharField(_("заголовок"), max_length=255)
    content = RichTextField(_("содержимое"), blank=True)


    def __str__(self):
        return self.title

