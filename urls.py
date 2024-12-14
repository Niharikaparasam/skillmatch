# skillmatch/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [ path('admin/', admin.site.urls),
    path('', include('recommendations.urls')),  # Link to app-level URLs
]
