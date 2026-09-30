from getpass import getpass

from database import users_collection
from security import hash_password


def main():
    email = input("Admin email: ").strip().lower()
    name = input("Admin name: ").strip()
    password = getpass("Admin password: ")
    confirmation = getpass("Confirm password: ")

    if not email or not name:
        raise SystemExit("Email and name are required.")
    if len(password) < 12:
        raise SystemExit("Use an admin password with at least 12 characters.")
    if password != confirmation:
        raise SystemExit("Passwords do not match.")
    if users_collection.find_one({"email": email}):
        raise SystemExit("That email is already registered.")

    users_collection.insert_one({
        "name": name,
        "email": email,
        "password_hash": hash_password(password),
        "role": "admin",
        "is_active": True,
    })
    print("Administrator created. There is no public admin registration route.")


if __name__ == "__main__":
    main()
