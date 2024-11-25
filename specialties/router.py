from django.urls import path
from specialties import views

urlpatterns = (
    path('', views.index),
)