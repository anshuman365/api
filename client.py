import requests

BASE_URL = "http://127.0.0.1:8000"

# Create a new user
def create_user(name, email, password):
    url = f"{BASE_URL}/users/"
    data = {"name": name, "email": email, "password": password}
    response = requests.post(url, json=data)
    return response.json()

# Get user by ID
def get_user(user_id):
    url = f"{BASE_URL}/users/{user_id}"
    response = requests.get(url)
    return response.json()

# Update user
def update_user(user_id, name=None, email=None, password=None):
    url = f"{BASE_URL}/users/{user_id}"
    data = {"name": name, "email": email, "password": password}
    response = requests.put(url, json={k: v for k, v in data.items() if v is not None})
    return response.json()

# Delete user
def delete_user(user_id):
    url = f"{BASE_URL}/users/{user_id}"
    response = requests.delete(url)
    return response.json()

# User authentication (JWT login)
def login(email, password):
    url = f"{BASE_URL}/token"
    data = {"email": email, "password": password}
    response = requests.post(url, json=data)
    return response.json()

if __name__ == "__main__":
    # Create a new user
    new_user = create_user("John Doe", "john@example.com", "secret")
    print("Created User:", new_user)

    user_id = new_user.get("id")
    
    if user_id:
        # Get user data
        user_data = get_user(user_id)
        print("Fetched User:", user_data)

        # Update user data
        updated_user = update_user(user_id, name="John Updated", email="john.updated@example.com")
        print("Updated User:", updated_user)

        # Delete user
        delete_response = delete_user(user_id)
        print("Deleted User Response:", delete_response)

    # User authentication example
    auth_response = login("john@example.com", "secret")
    print("Authentication Response:", auth_response)