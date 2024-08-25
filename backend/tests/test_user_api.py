from werkzeug.test import Client
from flaskr.services.user_service import UserService

user_service = UserService()

def test_do_not_create_the_same_user_twice(client: Client):
    user_data = {"email": "user1@test.com", "password": "11111111"}
    user_service.create_new_user(user_data)  # Create the user first

    # Log in to get a JWT token
    login_response = client.post("/api/auth/signin", json=user_data)
    assert login_response.status_code == 200  # Ensure login is successful

    token = login_response.json["access_token"]  # Extract the token

    # Attempt to create the same user
    response = client.post("/api/users", json=user_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 409  # Expecting Conflict status for duplicate

def test_create_new_user(client: Client):
    user_data = {"email": "user2@test.com", "password": "11111111"}

    response = client.post("/api/users", json=user_data)

    assert response.status_code == 201  # Expecting Created status for successful user creation

def test_create_category(client: Client):
    user_data = {"email": "user1@test.com", "password": "11111111"}
    user_service.create_new_user(user_data)

    # Log in to get the JWT token
    login_response = client.post("/api/auth/signin", json=user_data)
    assert login_response.status_code == 200
    token = login_response.json["access_token"]

    # Create a category after successful login
    category_data = {"name": "New Category"}
    response = client.post("/api/categories", json=category_data, headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 201  # Expecting Created status for successful category creation
