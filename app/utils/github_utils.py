from django.contrib.auth.models import User
from ..projects.models import Branch, Commit
import requests

def get_branches_and_commits(project):
    github_user, github_repo = _get_user_and_repo(project.github_url)

    branches_url = f'https://api.github.com/repos/{github_user}/{github_repo}/branches'
    response = requests.get(branches_url)
    branches = response.json()

    if response.status_code != 200:
        return None

    created_branches = []

    for branch in branches:
        created_branch = Branch.objects.create(name=branch['name'], last_commit_sha=branch['commit']['sha'], project=project)
        created_branches.append(created_branch)

        commit_sha = branch['commit']['sha']
        commits_url = f'https://api.github.com/repos/{github_user}/{github_repo}/commits?per_page=10&sha={commit_sha}'
        _get_and_save_commits(commits_url, created_branch)

    return created_branches

def _get_user_and_repo(url):
    """
    Example github url: https://github.com/MasterTeamFTN/uks
    """
    url_split = url.split('/')
    user = url_split[3]
    repo = url_split[4]

    return user, repo

def _get_and_save_commits(url, branch):
    response = requests.get(url)
    commits = response.json()

    # TODO: ovo treba raditi i sa paginacijom :(
    for commit in commits:
        try:
            user = User.objects.get(email=commit['commit']['email'])
        except:
            user = None

        print(commit)
        Commit.objects.create(
            sha=commit['sha'],
            message=commit['commit']['message'],
            github_diff_url=commit['html_url'],
            branch=branch,
            datetime=commit['commit']['author']['date'],
            author=user
        )

