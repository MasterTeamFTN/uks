def get_user_and_repo(url):
    """
    Example github url: https://github.com/MasterTeamFTN/uks
    """
    url_split = url.split('/')
    user = url_split[3]
    repo = url_split[4]

    return user, repo

