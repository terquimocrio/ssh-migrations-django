from django.urls import path
from . import views

urlpatterns = [
    path('', views.MigrationsView.as_view(), name='main'),
]