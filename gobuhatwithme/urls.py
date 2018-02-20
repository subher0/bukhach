from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path(r'', include('bukhach.urls')),
    path('api/v1/admin/', admin.site.urls),
]
