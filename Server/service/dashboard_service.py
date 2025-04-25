import repository.dashboard_repository as repo

def summary_user_list():
    return repo.get_user_list_resume()