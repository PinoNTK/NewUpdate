from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from Api_Extraction import views



urlpatterns = [
    path('api/extract-cv/<str:pathfile>',views.extract_cv),
    path(r'api/upload/',views.Upload_CV),
    path('api/json/',views.get_json),
    path('demo/',views.demo)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)