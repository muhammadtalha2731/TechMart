# TechMart - Script to create the admin account
# Run this script only once, after creating the database.
# How to run (in the VS Code terminal):
#     python create_admin.py
#
# This creates the admin@techmart.com account.
# The password is NOT written anywhere in the code. It comes from the
# ADMIN_PASSWORD environment variable, or you type it when asked.
# (The password is NOT saved in plain text, it is saved as a hash.)
# If the admin already exists, running this script again updates
# its password and role.

import getpass
import os

from config import get_connection
from werkzeug.security import generate_password_hash

ADMIN_NAME = "Admin"
ADMIN_EMAIL = "admin@techmart.com"


def get_admin_password():
    """Get the admin password from the environment, or ask for it."""
    password = os.environ.get("ADMIN_PASSWORD", "")
    if not password:
        password = getpass.getpass("Enter a password for the admin account: ")
    if not password:
        raise SystemExit("No password given. Run the script again.")
    return password


def main():
    admin_password = get_admin_password()
    conn = get_connection()
    cursor = conn.cursor()

    # Check: does the admin already exist?
    cursor.execute("SELECT Id FROM Users WHERE Email = ?", (ADMIN_EMAIL,))
    existing = cursor.fetchone()

    hashed = generate_password_hash(admin_password)

    if existing:
        # If the admin already exists, update its password and role.
        cursor.execute(
            "UPDATE Users SET Password = ?, Role = 'admin' WHERE Email = ?",
            (hashed, ADMIN_EMAIL),
        )
        print("Admin already existed. Password and role updated.")
    else:
        cursor.execute(
            "INSERT INTO Users (Name, Email, Password, Role) VALUES (?, ?, ?, 'admin')",
            (ADMIN_NAME, ADMIN_EMAIL, hashed),
        )
        print("Admin account created.")

    conn.commit()
    cursor.close()
    conn.close()
    print("Email: admin@techmart.com")
    print("Now run python app.py and login.")


if __name__ == "__main__":
    main()
