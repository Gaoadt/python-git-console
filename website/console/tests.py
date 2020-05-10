from django.test import TestCase, Client
from django.forms import ValidationError
from django.http import HttpResponse, HttpResponseRedirect
from console.forms import repo_name_validator
from console.views import new_repo
from console.repository_manager import RepositoryManager
from parameterized import parameterized
from console.models import Repository

import os, shutil

class DashboardTests(TestCase):
    def setUp(self):
        RepositoryManager.server_home_temp = RepositoryManager.server_home
        RepositoryManager.server_home = os.path.join(os.getcwd(),'temp','unit_testing','repos')
        self.tempFolder = os.path.join(os.getcwd(),'temp')
    
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
        self.assertEqual(Repository.objects.filter(name=name).count(), 1)
    
    @parameterized.expand([
        ["lion"],
        ["zebra"],
        ["Jiraf99"],
    ])
    def test_view_repo_access(self, name):
        c = Client()
        c.post('/dashboard/new', {'repo_name': name, 'repo_description': "Cool project"})
        result = c.get("/"+name+"/")
        self.assertEqual(result.status_code, 200)

    @parameterized.expand([
        ["lion"],
        ["zebra"],
        ["Jiraf99"],
    ])
    def test_cannot_view_repo(self, name):
        c = Client()
        result = c.get("/"+name+"/")
        self.assertEqual(result.status_code, 404)

    @parameterized.expand([
        ["lion", "Lion is a king of animals"],
        ["zebra", "Marti: Alex what are you doing? (c) Madagaskar"],
        ["monkey", "There will be a lecture about.. Right lets... (c) Madagaskar"],
    ])
    def test_correct_readme(self, name, text):
        c = Client()
        c.post('/dashboard/new', {'repo_name': name, 'repo_description': text})
        res = c.get(f"/{name}/master/README.md", follow = True)
        self.assertEqual(res.content.decode("utf-8"), text)

    def tearDown(self):
        try:
            shutil.rmtree(self.tempFolder)
        except Exception:
            pass
        RepositoryManager.server_home = RepositoryManager.server_home_temp

