from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404
from specialties import models


def index(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        "specialties/index.html",
        context={
            "contentpages": models.ContentPage.objects.all(),
            "title": "заголовок",
        },
    )

def contentpage(request: HttpRequest, pk: int) -> HttpResponse:
    contentpage = get_object_or_404(models.ContentPage, pk=pk)
    return render(
        request,
        "specialties/contentpage.html",
        context={
            "contentpages": models.ContentPage.objects.all(),
            "contentpage": contentpage
        },
    )
