import requests

base_url = "http://localhost:3000"
sample_name = "john"
sample_address = "123 ABC street"


def test_get_request_user_positive():
    # Send a GET request to the API
    response = requests.get(base_url + "/api/user/" + sample_name)

    # Assert the response status code
    assert response.status_code == 200
    assert response.json()["id"] == sample_name
    assert response.json()["name"] == "John Doe"


def test_get_request_user_negative():
    # Send a GET request to the API
    response = requests.get(base_url + "/api/user/error")

    # Assert the response status code
    assert response.status_code == 404
    assert response.json()["error"] == "User not found"


def test_get_request_address_positive():
    # Send a GET request to the API
    response = requests.get(base_url + "/api/address/" + sample_address)

    # Assert the response status code
    assert response.status_code == 200
    assert response.json()["id"] == sample_address
    assert response.json()["name"] == "123 Spring Ave"


def test_get_request_address_negative():
    # Send a GET request to the API
    response = requests.get(base_url + "/api/address/error")

    # Assert the response status code
    assert response.status_code == 500
    assert response.json()["error"] == "Address not found"


def test_post_request_address():
    # Send a POST request to the API
    response = requests.post(base_url + "/api/address/" + sample_address)

    # Assert the response status code
    assert response.status_code == 200
    assert response.json()["id"] == sample_address
