"""
URL configuration for config project.
"""
from django.contrib import admin
from django.urls import path, include

from landing.views import home, sdr_agent, slides_index, slides_deck

urlpatterns = [
    path('', home, name='home'),
    path('sdr-agent/', sdr_agent, name='sdr_agent'),
    path('slides/', slides_index, name='slides_index'),
    path('slides/<str:deck_name>/', slides_deck, name='slides_deck'),
    path('app/', include('backoffice.urls')),
    path('admin/', admin.site.urls),
]
