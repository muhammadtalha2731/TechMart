# TechMart - Script to create the admin account
# Run this script only once, after creating the database.
# How to run (in the VS Code terminal):
#     python create_admin.py
#
# This creates the admin@techmart.com / admin123 account.
# The password is NOT saved in plain text, it is saved as a hash.

from config import get_connection
from werkzeug.security import generate_password_hash

ADMIN_NAME = "Admin"
ADMIN_EMAIL = "admin@techmart.com"
ADMIN_PASSWORD = "admin123"


def main():
    conn = get_connection()
    cursor = conn.cursor()

    # Check: does the admin already exist?
    cursor.execute("SELECT Id FROM Users WHERE Email = ?", (ADMIN_EMAIL,))
    existing = cursor.fetchone()

    hashed = generate_password_hash(ADMIN_PASSWORD)

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
    print("Password: admin123")
    print("Now run python app.py and login.")


if __name__ == "__main__":
    main()
