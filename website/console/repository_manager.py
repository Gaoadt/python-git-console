from console.models import Repository
from django.http import Http404
import git
import os, shutil, getpass


class RepositoryManager:
    server_folder = "git_server"
    server_home = os.path.join(os.path.expanduser("~"), server_folder)
    
    def makeRepoPath(self, name):
        return os.path.join(self.server_home, name)
    
    def repoNameVacant(self, checkedName):
        return len(Repository.objects.filter(name=checkedName)) == 0

    def createRepo(self, name, readme_text):
        if not self.repoNameVacant(name):
            return
        
        path = self.makeRepoPath(name)
        gitrepo = git.Repo.init(path, bare=False)
        

        index = gitrepo.index
        new_file_path = os.path.join(gitrepo.working_tree_dir, 'README.md')
        readme = open(new_file_path, 'w')
        readme.write(readme_text)
        readme.close()
        index.add([new_file_path])        
        index.commit("Initial commit")

        repo = Repository(name=str(name), path=path)
        repo.save()
                 

    def getRepoData(self, repository, branch, path, hostname):
        repo = git.Repo(repository.path)
        data = RepositoryData(repository.name, path,
            f"git clone {getpass.getuser()}@{hostname}:{repository.path}",
            "", branch)
        
        if branch not in repo.heads:
            raise Http404

        tree = repo.heads[branch].commit.tree
        try:
            if path != "":
                tree = tree[path]
        except KeyError:
            return None

        if isinstance(tree, git.Blob):
            return tree.data_stream.read()
        
        data.branches = [item.name for item in repo.branches]
        data.backpath = os.path.join("",*tree.path.split('/')[:-1])
        for entry in tree:
            name = entry.path.split('/')[-1]
            data.items.append(RepositoryItem(
                isinstance(entry, git.Blob), entry.path, name))
        return data


class RepositoryItem:
    def __init__(self, isFile, path, name):
        self.isFile = isFile
        self.path = path
        self.name = name
        


class RepositoryData:
    branches = []
    def __init__(self, name, path, clone_link, backpath, branch):
        self.name = name
        self.clone_link = clone_link
        self.items = []
        self.backpath = backpath
        self.branch = branch
        self.path = path
    
