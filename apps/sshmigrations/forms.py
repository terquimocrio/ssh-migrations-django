from django import forms
from .utils import get_all_branches_as_tuple
from .models import GHConnection, Project, SSHConnection

import os

REPO_OWNER = os.environ.get('REPO_OWNER')
REPO_NAME = os.environ.get('REPO_NAME')
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')

BRANCHES_CHOICES = get_all_branches_as_tuple(REPO_OWNER, REPO_NAME, ACCESS_TOKEN)

class BranchesForm(forms.Form):
    project = forms.ModelChoiceField(queryset=Project.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    # branches = forms.ChoiceField(choices=(('', 'Select branch'),), widget=forms.Select(attrs={'class': 'form-control'}))

class CommandForm(forms.Form):
    command = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

# Catalogs

class GHConnectionForm(forms.ModelForm):
    class Meta:
        model = GHConnection
        fields = ['access_token', 'repo_owner', 'repo_name']
        widgets = {
            'access_token': forms.TextInput(attrs={'class': 'form-control'}),
            'repo_owner': forms.TextInput(attrs={'class': 'form-control'}),
            'repo_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class SSHConnectionForm(forms.ModelForm):
    class Meta:
        model = SSHConnection
        fields = ['ssh_name', 'ssh_host', 'ssh_port', 'ssh_username', 'ssh_private_key']
        widgets = {
            'ssh_name': forms.TextInput(attrs={'class': 'form-control'}),
            'ssh_host': forms.TextInput(attrs={'class': 'form-control'}),
            'ssh_port': forms.NumberInput(attrs={'class': 'form-control'}),
            'ssh_username': forms.TextInput(attrs={'class': 'form-control'}),
            'ssh_private_key': forms.FileInput(attrs={'class': 'form-control'}),
        }

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['project_name', 'project_path', 'ssh_connection', 'gh_connection']
        widgets = {
            'project_name': forms.TextInput(attrs={'class': 'form-control'}),
            'project_path': forms.TextInput(attrs={'class': 'form-control'}),
            'ssh_connection': forms.Select(attrs={'class': 'form-control'}),
            'gh_connection': forms.Select(attrs={'class': 'form-control'}),
        }