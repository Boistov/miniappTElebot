from django.contrib import admin
from django.urls import path, include  # Use `include` for app URLs

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('menu.urls')),  # Include URLs from the 'menu' app
]
