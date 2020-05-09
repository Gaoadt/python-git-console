"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from console import views

urlpatterns = [
    path('', views.index),
    path('dashboard/repositories', views.repos, name="repos"),
    path('dashboard/start', views.no_repos, name="no_repos"),
    path('dashboard/new', views.new_repo, name="new_repo"),
    path('view/<str:name>/', views.view_repo, name="view_repo"),
    path('view/<str:name>/<str:branch>/', views.view_repo, name="view_repo"),
    path('view/<str:name>/<str:branch>/<path:inside_path>', views.view_repo, name="view_repo"),
] 
