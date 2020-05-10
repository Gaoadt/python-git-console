from django.test import TestCase, Client
from django.forms import ValidationError
from django.http import HttpResponse, HttpResponseRedirect
from console.forms import repo_name_validator
from console.views import new_repo
from console.repository_manager import RepositoryManager
from parameterized import parameterized

import os, shutil

class RepoNameTests(TestCase):
    def setUp(self):
        RepositoryManager.server_home_temp = RepositoryManager.server_home
        RepositoryManager.server_home = os.path.join(os.getcwd(),'temp','unit_testing','repos')
    
    @parameterized.expand([
        ["dashboard"],
        ["admin"],
        ["a"],
        ["ab"],
    ])
    def test_cannot_make(self, name):
        #Calling internal checker
        self.assertRaises(ValidationError, repo_name_validator, name)
        
        #Simulating request
        c = Client()
        result = c.post('/dashboard/new', {'repo_name': name, 'repo_description': "Cool project"})
        self.assertNotIsInstance(result, HttpResponseRedirect)
    
    @parameterized.expand([
        ["lion"],
        ["zebra"],
        ["Jiraf99"],
    ])
    def test_can_make(self, name):
         #Calling internal checker
        repo_name_validator(name)
        
        #Simulating request
        c = Client()
        result = c.post('/dashboard/new', {'repo_name': name, 'repo_description': "Cool project"})
        self.assertIsInstance(result, HttpResponseRedirect)

    def tearDown(self):
        shutil.rmtree(RepositoryManager.server_home)
        RepositoryManager.server_home = RepositoryManager.server_home_temp

