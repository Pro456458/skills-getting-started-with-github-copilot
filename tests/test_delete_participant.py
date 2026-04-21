"""Tests for DELETE /activities/{activity_name}/participants/{email} endpoint (AAA pattern)"""


def test_delete_participant_success(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants/{email}")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Removed" in data["message"]
    assert email in data["message"]


def test_delete_participant_removes_from_activity(client):
    # Arrange
    activity_name = "Chess Club"
    email = "daniel@mergington.edu"
    initial_count = 2

    # Act
    client.delete(f"/activities/{activity_name}/participants/{email}")

    # Assert
    response = client.get("/activities")
    activities = response.json()
    assert email not in activities[activity_name]["participants"]
    assert len(activities[activity_name]["participants"]) == initial_count - 1


def test_delete_nonexistent_participant_fails(client):
    # Arrange
    activity_name = "Basketball Team"
    email = "noone@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants/{email}")

    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "Participant not found" in data["detail"]


def test_delete_from_nonexistent_activity_fails(client):
    # Arrange
    activity_name = "Fake Club"
    email = "test@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants/{email}")

    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]


def test_delete_allows_re_signup(client):
    # Arrange
    activity_name = "Programming Class"
    email = "emma@mergington.edu"

    # Act
    client.delete(f"/activities/{activity_name}/participants/{email}")
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    response = client.get("/activities")
    activities = response.json()
    assert email in activities[activity_name]["participants"]


def test_delete_restores_availability(client):
    # Arrange
    response = client.get("/activities")
    initial_spots = 20 - len(response.json()["Programming Class"]["participants"]) 

    # Act
    client.delete("/activities/Programming%20Class/participants/emma@mergington.edu")

    # Assert
    response = client.get("/activities")
    new_spots = 20 - len(response.json()["Programming Class"]["participants"])
    assert new_spots == initial_spots + 1
