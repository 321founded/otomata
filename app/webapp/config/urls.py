"""
URL configuration for config project.
"""
from django.contrib import admin
from django.urls import path

from landing.views import home, slides_index, slides_deck

urlpatterns = [
    path('', home, name='home'),
    path('slides/', slides_index, name='slides_index'),
    path('slides/<str:deck_name>/', slides_deck, name='slides_deck'),
    path('admin/', admin.site.urls),
]
