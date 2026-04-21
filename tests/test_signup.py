"""Tests for POST /activities/{activity_name}/signup endpoint (AAA pattern)"""


def test_signup_success(client):
    # Arrange
    activity_name = "Basketball Team"
    email = "test@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert email in data["message"]
    assert activity_name in data["message"]


def test_signup_adds_participant(client):
    # Arrange
    activity_name = "Soccer Club"
    email = "newstudent@mergington.edu"

    # Act
    client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )

    # Assert
    response = client.get("/activities")
    activities = response.json()
    assert email in activities[activity_name]["participants"]


def test_signup_duplicate_email_fails(client):
    # Arrange
    activity_name = "Chess Club"
    existing_email = "michael@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": existing_email}
    )

    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "already signed up" in data["detail"]


def test_signup_nonexistent_activity_fails(client):
    # Arrange
    activity_name = "Fake Club"
    email = "test@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]


def test_signup_multiple_activities(client):
    # Arrange
    email = "versatile@mergington.edu"
    activity1 = "Chess Club"
    activity2 = "Science Club"

    # Act
    response1 = client.post(
        f"/activities/{activity1}/signup",
        params={"email": email}
    )
    response2 = client.post(
        f"/activities/{activity2}/signup",
        params={"email": email}
    )

    # Assert
    assert response1.status_code == 200
    assert response2.status_code == 200
    response = client.get("/activities")
    activities = response.json()
    assert email in activities[activity1]["participants"]
    assert email in activities[activity2]["participants"]


def test_signup_updates_availability_count(client):
    # Arrange
    response = client.get("/activities")
    initial_spots = 15 - len(response.json()["Basketball Team"]["participants"]) 

    # Act
    client.post(
        "/activities/Basketball%20Team/signup",
        params={"email": "newuser@mergington.edu"}
    )

    # Assert
    response = client.get("/activities")
    new_spots = 15 - len(response.json()["Basketball Team"]["participants"])
    assert new_spots == initial_spots - 1
