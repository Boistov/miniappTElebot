from django.contrib import admin
from django.urls import path
from menu.views import menu_view  # Import the view function

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', menu_view, name='home'),  # Homepage URL
]
