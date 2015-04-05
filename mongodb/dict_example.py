__author__ = 'marco'


cache = dict()


def list_users():
    """ Accesses the DB and returns all users in a list

    :return: list of users
    """
    return list()

def all_users():
    """ Accesses the DB and retrieves all users and cache them locally
    :return:
    """
    # the most idiotic caching policy ever shown in this building
    if len(cache) == 0:
        users = list_users()
        for user in users:
            cache[user['username']] = user
    return cache

def get_user_from_db(username):
    """ Implementation using a list()

    :param username:
    :return:
    """
    for user in list_users():
        if user.get('username') == username:
            return user
    return None


def get_user(username):
    """ Implementation using a dict()

    :param username:
    :return:
    """
    return all_users().get(username)

