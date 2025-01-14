from django.urls import path, re_path
from specialties import views

urlpatterns = (
    path("", views.index),
    re_path(r"^contentpage/(?P<pk>\d+)$", views.contentpage, name="contentpage"),
)