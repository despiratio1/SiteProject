from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


def index(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        'specialties/index.html',
        context={
            "title": "заголовок",
        },
    )

def geography(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        'specialties/geography.html',
        context={
            "title": "заголовок",
        },
    )

def skills(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        'specialties/skills.html',
        context={
            "title": "заголовок",
        },
    )
