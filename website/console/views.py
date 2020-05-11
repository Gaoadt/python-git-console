from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import NewRepositoryForm
from .models import Repository
from .repository_manager import RepositoryManager, RepositoryData
def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """

    return redirect('repos')

def repos(request):
    """
    Function renders list of repositories
    """
    repo_list = Repository.objects.all()
    if repo_list.count() == 0:
        return redirect("no_repos")

    return render(request, 'repos.html',{'repo_list':repo_list} )

def no_repos(request):
    """
    Function renders no repos title
    """
    repo_list = Repository.objects.all()
    if repo_list.count() != 0:
        return redirect("repos")
    return render(request, 'no_repos.html')


def new_repo(request):
    if request.method == 'POST':
        form = NewRepositoryForm(request.POST)
        if form.is_valid():
            RepositoryManager().createRepo(form.cleaned_data['repo_name'],
                form.cleaned_data['repo_description'])
            return redirect("repos")
        
    else:
        form = NewRepositoryForm()

    return render(request, 'new_repo.html', {'form': form})

def view_repo(request, name, branch = "master", inside_path=""):
    repo = get_object_or_404(Repository, name=name)
    hostname = request.get_host().split(":")[0]
    data = RepositoryManager().getRepoData(repo, branch, inside_path, hostname)
    if data is None:
        return redirect("view_repo", name, branch)

    if not isinstance(data, RepositoryData):
        return HttpResponse(data, content_type='application/octet-stream')
    print(data.backpath)
    return render(request, 'view.html', {'data': data})
