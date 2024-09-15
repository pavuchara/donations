from copy import deepcopy


CORRECT_USER_CREATE_DATA = {
    'first_name': 'Марсель',
    'last_name': 'Павук',
    'username': 'marsel',
    'paternal_name': 'Павукович',
    'email': 'marsel@marsel.com',
    'password': 'very_strong_pass',
}


class IncorrectUserData:
    correct_data = CORRECT_USER_CREATE_DATA

    @classmethod
    def get_wrog_first_name(cls):
        user_data = deepcopy(CORRECT_USER_CREATE_DATA)
        user_data['first_name'] = '1' * 200
        return user_data

    @classmethod
    def get_wrong_email(cls):
        user_data = deepcopy(CORRECT_USER_CREATE_DATA)
        user_data['email'] = '1' * 200
        return user_data

    @classmethod
    def get_wrong_username(cls):
        user_data = deepcopy(CORRECT_USER_CREATE_DATA)
        user_data['username'] = '1' * 200
        return user_data


CORRECT_USER_UPDARE_DATA = {
    'first_name': 'Марсель1',
    'last_name': 'Павук1',
    'username': 'marsel1',
    'paternal_name': 'Павукович',
    'email': 'marsel@marsel.com',
    'password': 'very_strong_pass',
}


CORRECT_USER_PARTIAL_UPDARE_DATA = {
    'first_name': 'Марсель2',
    'last_name': 'Павук2',
    'paternal_name': 'Павукович2',
    'email': 'marsel2@marsel.com',
}


class IncorrectPartialUpdateUser:

    @classmethod
    def get_wrog_first_name(cls):
        return {'first_name': '1' * 200}

    @classmethod
    def get_wrong_email(cls):
        return {'email': '1' * 200}

    @classmethod
    def get_wrong_username(cls):
        return {'username': '1' * 200}


CORRECT_SECOND_USER_CREATE_DATA = {
    'first_name': 'Марсель2',
    'last_name': 'Павук2',
    'username': 'marsel2',
    'paternal_name': 'Павукович2',
    'email': 'marsel2@marsel.com',
    'password': 'very_strong_pass',
}


CORRECT_USER_TOKEN_OBTAIN_DATA = {
    'username': 'marsel',
    'password': 'very_strong_pass',
}
