CORRECT_USER_CREATE_DATA = {
    'first_name': 'Марсель',
    'last_name': 'Павук',
    'username': 'marsel',
    'paternal_name': 'Павукович',
    'email': 'marsel@marsel.com',
    'password': 'very_strong_pass',
}


CORRECT_SECOND_USER_CREATE_DATA = {
    'first_name': 'Марсель2',
    'last_name': 'Павук2',
    'username': 'marsel2',
    'paternal_name': 'Павукович2',
    'email': 'marsel2@marsel.com',
    'password': 'very_strong_pass',
}


INCORRECT_USER_CREATE_DATA = {
    'first_name': 'qwe',
    'last_name': 'qwe',
    'paternal_name': 'qwe',
    'email': 'qwe',
    'password': 'qwe',
}


CORRECT_USER_PARTIAL_UPDARE_DATA = {
    'first_name': 'Марсель2',
    'last_name': 'Павук2',
    'paternal_name': 'Павукович2',
    'email': 'marsel2@marsel.com',
}


INCORRECT_USER_PARTIAL_UPDARE_DATA = {
    'first_name': '123' * 200,
    'last_name': '123' * 200,
    'paternal_name': '123' * 200,
    'email': '123',
}


CORRECT_USER_UPDARE_DATA = {
    'first_name': 'Марсель1',
    'last_name': 'Павук1',
    'username': 'marsel1',
    'paternal_name': 'Павукович',
    'email': 'marsel@marsel.com',
    'password': 'very_strong_pass',
}


INCORRECT_USER_UPDARE_DATA = {
    'first_name': 'Марсель1',
    'last_name': 'Павук',
    'paternal_name': 'Павукович',
    'email': 'marsel',
}


CORRECT_USER_TOKEN_OBTAIN_DATA = {
    'username': 'marsel',
    'password': 'very_strong_pass',
}
