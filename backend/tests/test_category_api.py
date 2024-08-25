from werkzeug.test import Client  # type: ignore
from flaskr.services.category_service import CategoryService
from flaskr.services.user_service import UserService

category_service = CategoryService()
user_service = UserService()

def test_list_categories_in_user(client: Client):
    user_data = {"email": "user1@test.com", "password": "11111111"}
    user = user_service.create_new_user(user_data)

    assert user is not None  # Ensure user was created successfully

    for index in range(1, 6):
        category_data = {
            "category_name": f"TestCategoryName{index}",
            "user_id": user.id,
        }
        category_service.create_new_category(category_data)

    access_token = user_service.authenticate_user(user_data)["access_token"]
    print(f"Access Token: {access_token}")  # Debugging: Print access token

    response = client.get(f"/api/users/{user.id}/categories", headers={"Authorization": f"Bearer {access_token}"})
    
    assert response.status_code == 200
    assert len(response.json) == 5


def test_create_new_category(client: Client):
    user_data = {"email": "user1@test.com", "password": "11111111"}
    user = user_service.create_new_user(user_data)

    assert user is not None  # Ensure user was created successfully

    # Authenticate the user to get an access token
    auth_response = user_service.authenticate_user(user_data)
    access_token = auth_response.get("access_token")
    assert access_token is not None  # Ensure the token was obtained

    print(f"Access Token for Creating Category: {access_token}")  # Debugging

    category_data = {"category_name": "TestCategoryName", "user_id": user.id}

    response = client.post(
        "/api/categories",
        json=category_data,
        headers={"Authorization": f"Bearer {access_token}"},  # Include the token
    )

    assert response.status_code == 201  # Expecting Created status


def test_remove_category_by_id(client: Client):
    user_data = {"email": "user1@test.com", "password": "11111111"}
    user = user_service.create_new_user(user_data)

    assert user is not None  # Ensure user was created successfully

    # Create categories for the user
    for index in range(1, 6):
        category_data = {
            "category_name": f"TestCategoryName{index}",
            "user_id": user.id,
        }
        category_service.create_new_category(category_data)

    # Authenticate the user to get an access token for deletion
    auth_response = user_service.authenticate_user(user_data)
    access_token = auth_response.get("access_token")
    assert access_token is not None  # Ensure the token was obtained

    print(f"Access Token for Deleting Category: {access_token}")  # Debugging

    categories_in_user = client.get(f"/api/users/{user.id}/categories", headers={"Authorization": f"Bearer {access_token}"})
    assert len(categories_in_user.json) == 5

    # Delete the category with ID 5
    delete_response = client.delete(f"/api/categories/5", headers={"Authorization": f"Bearer {access_token}"})
    assert delete_response.status_code == 204  # Expecting No Content for successful deletion

    # Check if the category was removed
    categories_in_user = client.get(f"/api/users/{user.id}/categories", headers={"Authorization": f"Bearer {access_token}"})
    assert len(categories_in_user.json) == 4
