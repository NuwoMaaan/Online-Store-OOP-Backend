from models.user import Customer, Staff
from models.catalogue import Catalogue
from models.cart import Cart
from services import terminal_payment_service as payment_service


import json

def banner():
    print(r"""
      __          ________    ____        _ _               _____ _                 
     /\ \        / /  ____|  / __ \      | (_)             / ____| |                
    /  \ \  /\  / /| |__    | |  | |_ __ | |_ _ __   ___  | (___ | |_ ___  _ __ ___ 
   / /\ \ \/  \/ / |  __|   | |  | | '_ \| | | '_ \ / _ \  \___ \| __/ _ \| '__/ _ \
  / ____ \  /\  /  | |____  | |__| | | | | | | | | |  __/  ____) | || (_) | | |  __/
 /_/    \_\/  \/   |______|  \____/|_| |_|_|_|_| |_|\___| |_____/ \__\___/|_|  \___
""")
   

def main():
    banner()
    print("This is the terminal interface for the backend system.")
    print("You can run various commands to interact with the system.")
    
    while True:
        print("\nAvailable commands:")
        print("1 - Login")
        print("2 - Create account")
        print("3 - Exit")
        command = input("Enter command number: ").strip()
        if command == "3":
            print("Exiting terminal. Goodbye!")
            break
        elif command == "1":   
            user = login()
            if user is None:
                print("Login failed. Please try again.")
            if user is not None:
                menu(user)
        elif command == "2":
            new_user = create_new_user()
            if new_user is None:
                print("Failed account creation")     
        else:
            print(f"Unknown command: {command}")

def menu(user):
    print(f"\n======main menu======")
    print("1 - View Catalogue")
    print("2 - View Cart")
    print("3 - Checkout")
    print("4 - Exit")
    choice = input("Enter your choice: ").strip()
    
    if choice == "1":
        Catalogue.catalogue_menu(user)
        menu(user)
    elif choice == "2":
        Cart.cart_menu(user)
        menu(user)
    elif choice == "3":
        payment_service.transaction_procedure(user)
    elif choice == "4":
        print("Exiting Menu")
    else:
        print(f"Unknown option: {choice}") 


def login():
    username = input("Enter username: ")
    password = input("Enter password: ")
    with open("Backend/db/user_data.json", "r") as f:
        data = json.load(f)
        users = data.get("users", [])
    for user in users:
        if user["username"] == username and user["password"] == password:
            print(f"Login successful. Welcome, {username}!")
            if user["role"] == "customer":
                return Customer(**user)
            elif user["role"] == "staff":
                return Staff(**user)
            else:
                print(f"Unknown role: '{user['role']}' for user {username}")
                return None
    print("Login failed. Invalid username or password.")
    return None

def create_new_user():
    print("======NEW CUSTOMER ACCOUNT CREATION======")
    email = input("Enter email: ")
    username = input("Enter username: ")
    password = input("Enter password: ")
    if '@' in email:
        with open("Backend/db/user_data.json", "r+") as f:
            data = json.load(f)
            users = data.get("users", [])

            existing_ids = {user["user_id"] for user in users}
            new_id = 1
            while new_id in existing_ids:
                new_id += 1

            for user in users:
                if user["username"] == username:
                    print("Username already exists.")
                    return None
                if user["email"] == email:
                    print("Email already registered.")
                    return None
    
            new_user = {"user_id": new_id,"username": username,"email": email,"role": "customer","password": password}
            users.append(new_user)
            data["users"] = users
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()
        print(f"Account created for: {username}")
        return new_user
    if '@' not in email:
        print("Invalid email. Must contain '@'")
        return None
        
    

if __name__ == "__main__":
    
    main()