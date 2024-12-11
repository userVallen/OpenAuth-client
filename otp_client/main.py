from flask import Flask, request, jsonify
import hashlib
import requests
import time

# Define the URL of your Flask server
url = "http://localhost:5000/otp/signup"

# Prompt the user for their username (real-life scenario)
username = input("Enter your username: ")

# Create the data to be sent in the request body
data = {"username": username}

# Send the POST request to the server
response = requests.post(url, json=data)

app = Flask(__name__)

# Route to receive the signup request and generate a key
@app.route('/otp/signup', methods=['POST'])
def signup():
    # Parse the JSON data from the request body
    data = request.get_json()

    # Extract the 'username' field from the request body
    username = data.get("username")

    # Fetch key from the server
    key = get_key_from_server("http://localhost:5000/otp/signup", username)

    # Return the key and message
    return jsonify({"key": key, "message": "Signup Successful", "username": username})

def get_key_from_server(server_url, username):
    # Fetch key from the server
    response = requests.post(server_url, json={"username": username})

    if response.status_code == 200:
        # Parse the JSON response
        response_data = response.json()
        key = response_data.get("key")
        return key
    else:
        raise Exception(f"Failed to fetch key: {response.status_code}, {response.text}")

def hash_key(key):
    # Get the current time block (rounded down to the nearest 60 seconds)
    current_time_block = int(time.time() // 60)

    # Concatenate the key and the current time block
    combined_key = f"{key}{current_time_block}"

    # Hash the key using SHA256
    hashed_key = hashlib.sha256(combined_key.encode()).hexdigest()

    return hashed_key

def generate_otp(hashed_key):
    #Extract the last 6 characters from the hashed key
    last_6_chars = hashed_key[-6:]

    # Convert the last 6 characters into a 6-digit number
    otp = int(last_6_chars, 16)  # Convert hex to an integer

    # Ensure the OTP is a 6-digit number
    otp = otp % 1000000

    return otp

def main():
    hashed_key = hash_key(key)
    otp = generate_otp(hashed_key)
    print(f"OTP: {otp:06d}")
    return otp

if __name__ == "__main__":
    key = get_key_from_server("http://localhost:5000/otp/signup", username)
    main()
