"""Tests for GET /activities endpoint (AAA pattern)"""


def test_get_activities_returns_all_activities(client):
    # Arrange: default data

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 9
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_get_activities_structure(client):
    # Arrange

    # Act
    response = client.get("/activities")
    data = response.json()
    activity = data["Chess Club"]

    # Assert
    assert "description" in activity
    assert "schedule" in activity
    assert "max_participants" in activity
    assert "participants" in activity
    assert isinstance(activity["participants"], list)


def test_get_activities_participant_count(client):
    # Arrange

    # Act
    response = client.get("/activities")
    data = response.json()

    # Assert
    assert len(data["Chess Club"]["participants"]) == 2
    assert "michael@mergington.edu" in data["Chess Club"]["participants"]
    assert len(data["Basketball Team"]["participants"]) == 0


def test_root_redirects_to_index(client):
    # Arrange

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"
