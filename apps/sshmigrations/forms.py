from django import forms
from .utils import get_all_branches_as_tuple

import os

REPO_OWNER = os.environ.get('REPO_OWNER')
REPO_NAME = os.environ.get('REPO_NAME')
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')

BRANCHES_CHOICES = get_all_branches_as_tuple(REPO_OWNER, REPO_NAME, ACCESS_TOKEN)

print(BRANCHES_CHOICES)

class BranchesForm(forms.Form):
    branches = forms.ChoiceField(choices=BRANCHES_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    