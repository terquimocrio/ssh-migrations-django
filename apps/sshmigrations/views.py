import logging
import os
from typing import Any
from django import http

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import FormView, TemplateView, CreateView, UpdateView, ListView, View
from .models import GHConnection, Project, SSHConnection

from .forms import BranchesForm, CommandForm, ProjectForm, GHConnectionForm, SSHConnectionForm
from .utils import makemigrations, merge_branch, migrate, ssh_connection, get_all_branches_as_json

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

        # ssh_connection_ = SSHConnection.objects.get(
        #     pk=request.POST['ssh_connection'])
        # gh_connection = GHConnection.objects.get(
        #     pk=request.POST['gh_connection'])
        project = Project.objects.get(pk=request.POST['project'])

        connection = ssh_connection(
            project.ssh_connection.ssh_private_key.path, project.ssh_connection.ssh_host, project.ssh_connection.ssh_port, project.ssh_connection.ssh_username)

        merge = merge_branch(
            project.project_path, request.POST['branches'], connection)

        makemigrations_ = makemigrations(
            project.project_path, request.POST['branches'], connection)
        migrate_ = migrate(project.project_path,
                           request.POST['branches'], connection)

        context = self.get_context_data(**kwargs)
        context['form'] = self.form_class

        error_message_merge = merge[1]
        success_message_merge = merge[0]

        error_message_migration = makemigrations_[1]
        success_message_migration = makemigrations_[0]

        error_message_migrate = migrate_[1]
        success_message_migrate = migrate_[0]
        

        context['error_message_merge'] = error_message_merge
        context['success_message_merge'] = success_message_merge
        context['error_message_migration'] = error_message_migration
        context['success_message_migration'] = success_message_migration
        context['error_message_migrate'] = error_message_migrate
        context['success_message_migrate'] = success_message_migrate

        print('Successful messages')
        print(f"merge: {merge[0]}")
        print(f"migrations: {makemigrations_[0]}")
        print(f"migrate: {migrate_[0]}")

        print('Error messages')

        print(f"merge: {merge[1]}")
        print(f"migrations: {makemigrations_[1]}")
        print(f"migrate: {migrate_[1]}")

        return render(request, self.template_name, context=context)


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
    
class BranchesView(View):
    def dispatch(self, request, *args, **kwargs):
        project = Project.objects.get(pk=kwargs['pk'])
        repo_owner = project.gh_connection.repo_owner
        repo_name = project.gh_connection.repo_name
        access_token = project.gh_connection.access_token

        branches_json = get_all_branches_as_json(
            repo_owner, repo_name, access_token)
        return JsonResponse(branches_json, safe=False)


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
