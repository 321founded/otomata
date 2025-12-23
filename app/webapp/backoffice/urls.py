from django.urls import path
from . import views

app_name = 'backoffice'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('', views.dashboard, name='dashboard'),
    path('workflows/', views.workflows_list, name='workflows'),
    path('workflows/<int:pk>/', views.workflow_detail, name='workflow_detail'),
    path('runs/', views.runs_list, name='runs'),
    path('runs/<int:pk>/', views.run_detail, name='run_detail'),
    path('data/', views.data, name='data'),
]
