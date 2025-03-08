import pytest
from rest_framework.test import APIClient
from rest_framework import status
from usersapp.models import User

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_user(db):
    user = User.objects.create(username="testuser", password="testpass")
    return user

@pytest.mark.django_db
def test_create_user(api_client):
    data = {"username": "newuser", "password": "securepass"}
    response = api_client.post("/user/register/", data)  # ✅ URL yangilandi
    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.count() == 1
    assert User.objects.first().username == "newuser"

@pytest.mark.django_db
def test_get_users(api_client, create_user):
    response = api_client.get("/user/allusers/")  # ✅ URL to‘g‘rilandi
    assert response.status_code == status.HTTP_200_OK
    assert response.data[0]["username"] == create_user.username
