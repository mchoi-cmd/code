import json
import requests

base_url = "http://localhost:3000"
headers = {'Content-Type': 'application/json'}
sample_cart_no_item = {"items" : []}
sample_cart_single_item = {
    "items" : [
        {"id": "item1", "unitPrice": 10, "quantity": 2}
    ]
}
sample_cart_multiple_items = {
    "items" : [
        {"id": "item1", "unitPrice": 10, "quantity": 2},
        {"id": "item2", "unitPrice": 5, "quantity": 3},
        {"id": "item3", "unitPrice": 5, "quantity": 3},
    ]
}
sample_cart_invalid_type = {
    "items" : [
        {"id": "item1", "unitPrice": "10", "quantity": 2},
    ]
}
sample_cart_invalid_data = {
    "items" : [
        {"id": "item1", "unitPrice": 10},
        {"id": "item2", "unitPrice": 5, "quantity": 3},
        {"id": "item3", "unitPrice": 5, "quantity": 3},
    ]
}
sample_cart_negative_unitPrice = {
    "items" : [
        {"id": "item1", "unitPrice": -2, "quantity": 2},
    ]
}
sample_cart_negative_quantity = {
    "items" : [
        {"id": "item1", "unitPrice": 2, "quantity": -2},
    ]
}


def test_post_positive_multiple_items():
    # Send Request
    payload = json.dumps(sample_cart_multiple_items)
    response = requests.post(base_url + "/cart", headers=headers, data=payload)

    # Assert
    assert response.status_code == 200
    assert response.json()["items"] == sample_cart_multiple_items["items"]
    assert response.json()["totalPrice"] == 50


def test_post_positive_single_item():
    # Send Request
    payload = json.dumps(sample_cart_single_item)
    response = requests.post(base_url + "/cart", headers=headers, data=payload)

    # Assert
    assert response.status_code == 200
    assert response.json()["items"] == sample_cart_single_item["items"]
    assert response.json()["totalPrice"] == 20


def test_post_positive_no_item():
    # Send Request
    payload = json.dumps(sample_cart_no_item)
    response = requests.post(base_url + "/cart", headers=headers, data=payload)

    # Assert
    assert response.status_code == 400


def test_post_negative_invalid_item():
    # Send Request
    payload = json.dumps(sample_cart_invalid_type)
    response = requests.post(base_url + "/cart", headers=headers, data=payload)

    # Assert
    assert response.status_code == 400


def test_post_negative_unitPrice():
    # Send Request
    payload = json.dumps(sample_cart_negative_unitPrice)
    response = requests.post(base_url + "/cart", headers=headers, data=payload)

    # Assert
    assert response.status_code == 400


def test_post_negative_quantity():
    # Send Request
    payload = json.dumps(sample_cart_negative_quantity)
    response = requests.post(base_url + "/cart", headers=headers, data=payload)

    # Assert
    assert response.status_code == 400


def test_post_negative_invalid_data():
    # Send Request
    payload = json.dumps(sample_cart_invalid_data)
    response = requests.post(base_url + "/cart", headers=headers, data=payload)

    # Assert
    assert response.status_code == 400


def test_post_no_data():
    # Send Request
    response = requests.post(base_url + "/cart")

    # Assert
    assert response.status_code == 400
    assert response.json()["error"] == "Invalid request body"


def test_invalid_get_path():
    # Send Request
    response = requests.get(base_url + "/cart")

    # Assert
    assert response.status_code == 404


def test_invalid_put_path():
    # Send Request
    response = requests.put(base_url + "/cart")

    # Assert
    assert response.status_code == 404

# To do  / for future consideration:
#
# More input validations (e.g. float for numbers, special characters, etc  )
# Review OWASP - Security test cases - mixed in special characters
# Scale & performance consideration
## create a cart that exceeds the expected number of items,
## unit price and quantity that exeed expected value
## create a reasonable large cart and check how fast the request is processed
# Split out test data from the tests