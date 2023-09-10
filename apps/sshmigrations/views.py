import logging
import os
from typing import Any

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import FormView, TemplateView, CreateView, UpdateView, ListView
from .models import GHConnection, Project, SSHConnection

from .forms import BranchesForm, CommandForm, ProjectForm, GHConnectionForm, SSHConnectionForm 
from .utils import makemigrations, merge_branch, migrate, ssh_connection

# Create your views here.

logging.basicConfig(level=logging.ERROR)

SSH_HOST = os.environ.get('SSH_HOST')
SSH_PORT = os.environ.get('SSH_PORT')
SSH_USERNAME = os.environ.get('SSH_USERNAME')
SSH_PRIVATE_KEY_PATH = os.environ.get('SSH_PRIVATE_KEY_PATH')
PROJECT_PATH = os.environ.get('PROJECT_PATH')

class MigrationsView(FormView):
    form_class = BranchesForm
    template_name = 'sshmigrations/migrations.html'
    success_url = '/'

    def form_valid(self, form):
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):

        connection = ssh_connection(
            SSH_PRIVATE_KEY_PATH, SSH_HOST, SSH_PORT, SSH_USERNAME)

        merge = merge_branch(
            PROJECT_PATH, request.POST['branches'], connection)
        makemigrations_ = makemigrations(
            PROJECT_PATH, request.POST['branches'], connection)
        migrate_ = migrate(PROJECT_PATH, request.POST['branches'], connection)

        print('Successful messages')
        print(f"merge: {merge[0]}")
        print(f"migrations: {makemigrations_[0]}")
        print(f"migrate: {migrate_[0]}")

        print('Error messages')

        print(f"merge: {merge[1]}")
        print(f"migrations: {makemigrations_[1]}")
        print(f"migrate: {migrate_[1]}")

        return super().post(request, *args, **kwargs)

class ExecCommandView(FormView):
    form_class = CommandForm
    template_name = 'sshmigrations/exec_command.html'
    success_url = '/exec_command'

    def form_valid(self, form):
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):

        connection = ssh_connection(
            SSH_PRIVATE_KEY_PATH, SSH_HOST, SSH_PORT, SSH_USERNAME)

        command = request.POST['command']
        stdin, stdout, stderr = connection.exec_command(command)

        error_message = stderr.read().decode('utf-8')
        success_message = stdout.read().decode('utf-8')

        print(f"error_message: {error_message}")
        print(f"success_message: {success_message}")

        context = self.get_context_data(**kwargs)
        context['form'] = self.form_class
        context['error_message'] = error_message
        context['success_message'] = success_message

        return render(request, self.template_name, context=context)
    
class CatalogsIndexView(TemplateView):
    template_name = 'sshmigrations/catalogs/index.html'
    
    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context['catalogs'] = [
            {
                'name': 'SSH Connection',
                'description': 'CRUD SSH Connection',
                'url': '/catalogs/sshconnection/'
            },
            {
                'name': 'Github Connection',
                'description': 'CRUD Github Connection',
                'url': '/catalogs/ghconnection/'
            },
            {
                'name': 'Project',
                'description': 'CRUD Project',
                'url': '/catalogs/project/'
            },
        ]
        return context
    
# Catalogs

# Project
class IndexProjectView(ListView):
    model = Project
    template_name = 'sshmigrations/catalogs/project/index.html'
    context_object_name = 'projects'

class CreateProjectView(CreateView):
    model = Project
    template_name = 'sshmigrations/catalogs/project/create.html'
    success_url = '/catalogs/project/'
    form_class = ProjectForm

class UpdateProjectView(UpdateView):
    model = Project
    template_name = 'sshmigrations/catalogs/project/update.html'
    success_url = '/catalogs/project/'
    form_class = ProjectForm

# SSH Connection
class IndexSSHConnectionView(ListView):
    model = SSHConnection
    template_name = 'sshmigrations/catalogs/ssh_connection/index.html'
    context_object_name = 'ssh_connections'

class CreateSSHConnectionView(CreateView):
    model = SSHConnection
    template_name = 'sshmigrations/catalogs/ssh_connection/create.html'
    success_url = '/catalogs/sshconnection/'
    form_class = SSHConnectionForm

class UpdateSSHConnectionView(UpdateView):
    model = SSHConnection
    template_name = 'sshmigrations/catalogs/ssh_connection/update.html'
    success_url = '/catalogs/sshconnection/'
    form_class = SSHConnectionForm

# GHConnection
class IndexGHConnectionView(ListView):
    model = GHConnection
    template_name = 'sshmigrations/catalogs/gh_connection/index.html'
    context_object_name = 'gh_connections'

class CreateGHConnectionView(CreateView):
    model = GHConnection
    template_name = 'sshmigrations/catalogs/gh_connection/create.html'
    success_url = '/catalogs/ghconnection/'
    form_class = GHConnectionForm

class UpdateGHConnectionView(UpdateView):
    model = GHConnection
    template_name = 'sshmigrations/catalogs/gh_connection/update.html'
    success_url = '/catalogs/ghconnection/'
    form_class = GHConnectionForm



    