from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from FrontEnd import views

urlpatterns = [
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('candidate/', views.candidate)
]