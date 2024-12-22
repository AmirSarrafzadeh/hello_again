"""
URL configuration for the hello_again project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# Import the necessary functions and modules from Django
import os
from django.contrib import admin
from pathlib import Path
from django.urls import path
from django.urls import re_path
from django.shortcuts import render
from django.http import FileResponse
from loyalty_app.api import api
from loyalty_app.views import list_entries
BASE_DIR = Path(__file__).resolve().parent.parent


# Handle the favicon request
def favicon_view(request):
    return FileResponse(open(os.path.join(BASE_DIR, 'static/favicon.ico'), 'rb'))


def home(request):
    return render(request, 'home.html')


urlpatterns = [
    path('admin/', admin.site.urls),  # Admin panel
    path('entries', list_entries, name='list_entries'),  # API endpoint for listing entries
    path('api/entries', list_entries, name='list_entries'),  # API endpoint for listing entries
    path('api/', api.urls),  # Ninja API endpoints
    path('', home, name='home'),  # Root path with a welcome message
    re_path(r'^favicon\.ico$', favicon_view),
]
