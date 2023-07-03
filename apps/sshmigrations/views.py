import logging
import os
from typing import Any

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import FormView

from .forms import BranchesForm
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
    template_name = 'sshmigrations/main.html'
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

        logging.info('Successful messages')
        logging.info(f"merge: {merge[0]}")
        logging.info(f"migrations: {makemigrations_[0]}")
        logging.info(f"migrate: {migrate_[0]}")

        logging.info('Error messages')

        logging.error(f"merge: {merge[1]}")
        logging.error(f"migrations: {makemigrations_[1]}")
        logging.error(f"migrate: {migrate_[1]}")

        return super().post(request, *args, **kwargs)