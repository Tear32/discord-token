import json
import requests

def login_and_save(email, password, ):
    z = {
        "login": email,
        "password": password,
        "Undelete": "False"
    }
    X = requests.post("https://discord.com/api/v9/auth/login", json=z)
    if X.status_code == 200:
        token = X.json().get("token")
        print("Token:", token)
        h = {'Authorization': token}
        Z = requests.get("https://discord.com/api/v9/users/@me", headers=h)
        if Z.status_code == 200:
            user_info = Z.json()
            print("UserID:", user_info.get("id"))
            print("Email:", user_info.get("email"))
            print("Username:", user_info.get("username"))
            print("Verified:", user_info.get("verified"))
            data = {
                "Token": token,
                "Data": {
                    "Username": user_info.get("username"),
                    "Email": user_info.get("email"),
                    "UserID": user_info.get("id"),
                    "Verified": user_info.get("verified")
                }
            }
            return data
        else:
            print("@ME GET ERROR\n\n" + Z.text)
    else:
        print("LOGIN ERROR\n\n" + X.text)
    return None

while True:
    email = input("Email: ")
    if not email:
        break  
    password = input("Password: ")
    if not password:
        break  

    try:
        with open('tokens.json', 'r') as f:
            token_data_list = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        token_data_list = []
        token_data = login_and_save(email, password)
        if token_data:
                token_data_list.append(token_data)
                # Save updated token data to JSON file
                with open('tokens.json', 'w') as f:
                    json.dump(token_data_list, f, indent=4)
                break  
    print("\n--- Enter another email ---")

input("Press Enter to exit...")
