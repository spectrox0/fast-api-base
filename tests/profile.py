from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_profile():
    """
    Test case for creating a profile.

    Sends a POST request to the '/profiles/' endpoint with a
    JSON payload containing the profile name and description.
    Checks if the response status code is 200 and if the returned JSON matches the expected values.

    Raises:
        AssertionError: If the response status code is not 200
        or if the returned JSON does not match the expected values.
    """
    response = client.post(
        "/profiles/",
        json={"name": "Test Profile", "description": "This is a test profile"},
    )
    if response.status_code != 200:
        raise AssertionError(
            "Expected status code 200, but received: "
            + str(response.status_code),
        )
    if response.json() != {
        "name": "Test Profile",
        "description": "This is a test profile",
    }:
        raise AssertionError(
            """Expected JSON response:
             {'name': 'Test Profile', 'description': 'This is a test profile'}, but received: """
            + str(response.json()),
        )


def test_read_profile():
    """
    Test case for reading a profile.

    This function sends a GET request to the '/profiles/1' endpoint and asserts that the response
    status code is 200 and the JSON response matches the expected profile data.

    """
    response = client.get("/profiles/1")
    if response.status_code != 200:
        raise AssertionError(
            "Expected status code 200, but received: "
            + str(response.status_code),
        )
    if response.json() != {
        "name": "Test Profile",
        "description": "This is a test profile",
    }:
        raise AssertionError(
            """Expected JSON response:
            {'name': 'Test Profile', 'description': 'This is a test profile'}, but received: """
            + str(response.json()),
        )


def test_update_profile():
    """
    Test case for updating a profile.

    Sends a PUT request to the '/profiles/1' endpoint with a JSON payload
    containing the updated profile information. Asserts that the response
    status code is 200 and the JSON response matches the expected values.
    """
    response = client.put(
        "/profiles/1",
        json={"name": "New Profile", "description": "This is a new profile"},
    )
    if response.status_code != 200:
        raise AssertionError(
            "Expected status code 200, but received: "
            + str(response.status_code),
        )
    if response.json() != {
        "name": "New Profile",
        "description": "This is a new profile",
    }:
        raise AssertionError(
            """Expected JSON response:
            {'name': 'New Profile', 'description': 'This is a new profile'},
            but received: """
            + str(response.json()),
        )


def test_delete_profile():
    """
    Test case for deleting a profile.

    Sends a DELETE request to the "/profiles/1" endpoint and asserts that the response
    status code is 200 and the response JSON is {"detail": "Profile deleted"}.
    """
    response = client.delete("/profiles/1")
    if response.status_code != 200:
        raise AssertionError(
            "Expected status code 200, but received: "
            + str(response.status_code),
        )
    if response.json() != {"detail": "Profile deleted"}:
        raise AssertionError(
            "Expected JSON response: {'detail': 'Profile deleted'}, but received: "
            + str(response.json()),
        )


def test_add_favorite_profile_not_in_profiles():
    """
    Test case to verify that adding a
    favorite profile that is not in the user's profile list returns a 400 status code
    and the expected error message in the JSON response.
    """
    response = client.post(
        "/users/test@example.com/favorite_profiles",
        json={"name": "Profile Not in List"},
    )
    if response.status_code != 400:
        raise AssertionError(
            "Expected status code 400, but received: "
            + str(response.status_code),
        )
    if response.json() != {"detail": "Profile not in user's profile list"}:
        raise AssertionError(
            """Expected JSON response:
            {'detail': 'Profile not in user's profile list'}, but received: """
            + str(response.json()),
        )


def test_remove_profile_also_removes_from_favorites():
    """
    Test case to verify that removing a profile also removes it from the favorite_profiles list.
    """
    client.post(
        "/users/test@example.com/profiles",
        json={"name": "Test Profile"},
    )
    client.post(
        "/users/test@example.com/favorite_profiles",
        json={"name": "Test Profile"},
    )
    client.delete("/users/test@example.com/profiles/Test Profile")
    response = client.get("/users/test@example.com")
    if "Test Profile" in response.json()["favorite_profiles"]:
        raise AssertionError("Test Profile still exists in favorite_profiles")
