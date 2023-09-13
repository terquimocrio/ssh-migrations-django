from django.urls import path
from . import views

app_name = 'sshmigrations'

urlpatterns = [
    path('', views.MigrationsView.as_view(), name='main'),
    path('exec_command/', views.ExecCommandView.as_view(), name='exec_command'),
    path('catalogs/', views.CatalogsIndexView.as_view(), name='catalogs'),

    # Catalogs
    # Project
    path('catalogs/project/', views.IndexProjectView.as_view(), name='index_project'),
    path('catalogs/project/create/', views.CreateProjectView.as_view(), name='create_project'),
    path('catalogs/project/update/<int:pk>/', views.UpdateProjectView.as_view(), name='update_project'),

    # SSH Connection
    path('catalogs/sshconnection/', views.IndexSSHConnectionView.as_view(), name='index_ssh_connection'),
    path('catalogs/sshconnection/create/', views.CreateSSHConnectionView.as_view(), name='create_ssh_connection'),
    path('catalogs/sshconnection/update/<int:pk>/', views.UpdateSSHConnectionView.as_view(), name='update_ssh_connection'),

    # GHConnection
    path('catalogs/ghconnection/', views.IndexGHConnectionView.as_view(), name='index_gh_connection'),
    path('catalogs/ghconnection/create/', views.CreateGHConnectionView.as_view(), name='create_gh_connection'),
    path('catalogs/ghconnection/update/<int:pk>/', views.UpdateGHConnectionView.as_view(), name='update_gh_connection'),
    
    # API
    path('api/get_branches/<int:pk>', views.BranchesView.as_view(), name='get_branches'),
]