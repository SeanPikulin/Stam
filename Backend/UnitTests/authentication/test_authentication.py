import pytest
from Backend.UnitTests.authentication import authentication


def test_login_all_good():
    auth = authentication.Authentication.get_instance()
    response = auth.login(username='Tali',password='puppy')
    print(response.succeeded())
    assert response.succeeded(), response.get_msg == "login succeeded"

def test_login_username_doesnt_exist():
    auth = authentication.Authentication.get_instance()
    response = auth.login(username='shahaf',password='sadna')
    assert not response.succeeded(), response.get_msg == "username doesn't exist in the system"

def test_login_username_exists_password_incorrect():
    auth = authentication.Authentication.get_instance()
    response = auth.login(username='Inon',password='gguy')
    assert not response.succeeded(), response.get_msg == "password incorrect"

def test_register_username_already_exists():
    auth = authentication.Authentication.get_instance()
    response = auth.login(username='Omer',password='coooool')
    assert not response.succeeded(), response.get_msg == "username already exists"

def test_register_all_good():
    auth = authentication.Authentication.get_instance()
    response = auth.register(username='Shahaf',password='sadna')
    assert response.succeeded(), response.get_msg == "registration succeeded"

# if __name__=="__main__":
#     test_register_all_good()