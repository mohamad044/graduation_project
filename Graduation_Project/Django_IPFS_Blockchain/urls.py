# myproject/urls.py

from django.contrib import admin
from django.urls import path, include



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('filehandler.urls')),  # Route to app-level URLs

]
