from fastapi.testclient import TestClient

from app.main import app  # replace with the actual name of your FastAPI app

client = TestClient(app)


def test_create_user():
    """
    Test case for creating a user.

    Sends a POST request to the "/users/" endpoint with a JSON payload containing the email address.
    Checks if the response status code is 200 and if the response
    JSON matches the expected structure.

    Raises:
        AssertionError: If the response status code is not 200 or if the response JSON is invalid.
    """
    response = client.post("/users/", json={"email": "test@example.com"})
    if response.status_code != 200:
        raise AssertionError("Invalid response status code")
    if response.json() != {
        "email": "test@example.com",
        "profiles": [],
        "favorite_profiles": [],
    }:
        raise AssertionError("Invalid response")


def test_read_user():
    """
    Test case for reading a user's information.

    Sends a GET request to the "/users/test@example.com" endpoint and checks if the response
    status code is 200 and the JSON response matches the expected user information.

    Raises:
        Any exceptions that occur during the test execution.
    """
    response = client.get("/users/test@example.com")
    if response.status_code != 200 or response.json() != {
        "email": "test@example.com",
        "profiles": [],
        "favorite_profiles": [],
    }:
        raise AssertionError("Invalid response")


def test_update_user():
    """
    Test case for updating a user's email address.

    Sends a PUT request to the "/users/test@example.com" endpoint with a new email address.
    Checks if the response status code is 200 and if the response JSON matches the expected values.

    Raises:
        AssertionError: If the response status code is not 200 or if the response JSON is invalid.
    """
    response = client.put(
        "/users/test@example.com",
        json={"email": "new@example.com"},
    )
    if response.status_code != 200:
        raise AssertionError("Invalid response status code")
    if response.json() != {
        "email": "new@example.com",
        "profiles": [],
        "favorite_profiles": [],
    }:
        raise AssertionError("Invalid response")


def test_delete_profile():
    """
    Test case for deleting a profile.

    Sends a DELETE request to the "/profiles/1" endpoint and checks if the response
    status code is 200 and the response JSON is {"detail": "Profile deleted"}.
    Raises an AssertionError if the response status code or JSON is invalid.
    """
    response = client.delete("/profiles/1")
    if response.status_code != 200:
        raise AssertionError("Invalid response status code")
    if response.json() != {"detail": "Profile deleted"}:
        raise AssertionError("Invalid response")


def test_delete_user_removes_profiles():
    """
    Test case to verify that deleting a user also removes their profiles.
    """
    client.post(
        "/users/test@example.com/profiles",
        json={"name": "Test Profile"},
    )
    client.delete("/users/test@example.com")
    response = client.get("/profiles")
    if any(profile["name"] == "Test Profile" for profile in response.json()):
        raise AssertionError("Profile was not deleted")


def test_cannot_create_duplicate_user():
    """
    Test case to verify that a duplicate user cannot be created.

    It sends a POST request to create a user with a specific email address.
    Then it sends another POST request with the same email address.
    The expected behavior is that the second request should return a 400 status code
    and a JSON response with the detail "User already exists".
    """
    client.post("/users/", json={"email": "test@example.com"})
    response = client.post("/users/", json={"email": "test@example.com"})
    if response.status_code != 400:
        raise AssertionError("Invalid response status code")
    if response.json() != {"detail": "User already exists"}:
        raise AssertionError("Invalid response")
