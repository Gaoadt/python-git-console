from django import forms
from django.core.exceptions import ValidationError
from .repository_manager import RepositoryManager

forbidden_names = ["dashboard", "admin"]

def repo_name_validator(name):
    if len(name) > 200 or len(name) < 3:
        raise ValidationError("Repo name should be from 3 to 200 characters")
    if ' ' in name:
        raise ValidationError("Repo name should not have spaces in it")
    if not RepositoryManager().repoNameVacant(name):
        raise ValidationError("Repo with such name aleady exists")
    if name in forbidden_names:
        raise ValidationError("Name is reserved for developers purposes. How about developing cheryy_eating_game?")

class NewRepositoryForm(forms.Form):
    repo_name = forms.CharField(label='Repository name:', validators=[repo_name_validator])
    repo_description = forms.CharField(label="Project description:")