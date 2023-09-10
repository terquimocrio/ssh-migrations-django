from django.urls import path
from . import views

app_name = 'sshmigrations'

urlpatterns = [
    path('', views.MigrationsView.as_view(), name='main'),
    path('exec_command/', views.ExecCommandView.as_view(), name='exec_command'),
]