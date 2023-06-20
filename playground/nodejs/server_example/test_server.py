import requests

base_url = "http://localhost:3000"

def test_get_request_positive():
    # Send a GET request to the API
    response = requests.get(base_url + "/api/user/john")

    # Assert the response status code
    assert response.status_code == 200
    assert response.json()['id'] == 'john'
    assert response.json()['name'] == 'John Doe'

def test_get_request_negative():
    # Send a GET request to the API
    response = requests.get(base_url + "/api/user/error")
    
    # Assert the response status code
    assert response.status_code == 404
    assert response.json()['error'] == 'User not found'