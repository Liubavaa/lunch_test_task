import pytest
from rest_framework.test import APIClient
from . import models


@pytest.mark.django_db
def test_employee_registration():
    client = APIClient()
    response = client.post('/api/register/', {
        "username": "employee_test",
        "password": "password123",
        "role": "employee"
    })
    assert response.status_code == 201
    assert models.CustomUser.objects.filter(username="employee_test").exists()


@pytest.mark.django_db
def test_restaurant_registration():
    client = APIClient()
    response = client.post('/api/register/', {
        "username": "restaurant_test",
        "password": "password123",
        "role": "admin"
    })
    assert response.status_code == 201
    assert models.CustomUser.objects.filter(username="restaurant_test").exists()


@pytest.mark.django_db
def test_create_restaurant():
    client = APIClient()

    user = models.CustomUser.objects.create_user(username="restaurant_test", password="password123", role="admin")
    client.force_authenticate(user=user)

    response = client.post('/api/restaurant/create/', {
        "name": "Test Restaurant"
    })

    assert response.status_code == 201
    assert models.Restaurant.objects.filter(name="Test Restaurant").exists()


@pytest.mark.django_db
def test_employee_access_restaurant_denied():
    client = APIClient()

    user = models.CustomUser.objects.create_user(username="employee_test", password="password123")
    client.force_authenticate(user=user)

    response = client.post('/api/restaurant/create/', {
        "name": "Test Restaurant"
    })

    assert response.status_code == 403
    assert not models.Restaurant.objects.filter(name="Test Restaurant").exists()


@pytest.mark.django_db
def test_menu_creation():
    client = APIClient()

    # Create restaurant admin user
    user = models.CustomUser.objects.create_user(username="restaurant_test", password="password123", role="admin")
    restaurant = models.Restaurant.objects.create(admin=user, name="Test Restaurant")
    client.force_authenticate(user=user)

    response = client.post('/api/menu/upload/', {
        "description": "Test Menu",
        "date": "2024-09-28"
    })
    assert response.status_code == 201
    assert models.Menu.objects.filter(restaurant=restaurant).exists()


def prepare_for_voting():
    client = APIClient()

    restaurant_user = models.CustomUser.objects.create_user(username="restaurant_test", password="password123",
                                                            role="admin")
    restaurant = models.Restaurant.objects.create(admin=restaurant_user, name="Test Restaurant")
    menu = models.Menu.objects.create(restaurant=restaurant, description="Test Menu", date="2024-09-28")

    employee_user = models.CustomUser.objects.create_user(username="employee_test", password="password123")
    client.force_authenticate(user=employee_user)
    return client, menu, employee_user


@pytest.mark.django_db
def test_menu_voting():
    client, menu, employee_user = prepare_for_voting()

    response = client.post(f'/api/menu/vote/{menu.id}')
    assert response.status_code == 201
    assert menu.vote_set.filter(employee=employee_user).exists()


@pytest.mark.django_db
def test_double_voting():
    client, menu, employee_user = prepare_for_voting()

    response = client.post(f'/api/menu/vote/{menu.id}')
    assert response.status_code == 201
    response = client.post(f'/api/menu/vote/{menu.id}')
    assert response.status_code == 200

    assert menu.vote_set.count() == 1  # Still only one vote
