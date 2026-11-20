# TechMart - Database connection settings
# This file is only for connecting to the database.
# Server: localhost\SQLEXPRESS  (SQL Server 2022, same name as in SSMS)
# Database: TechMartDB
# Login: Windows Authentication (Trusted_Connection=yes)
# This means: it connects with the Windows user logged in on the laptop.
# No separate username/password is needed in SSMS.

import pyodbc

SERVER = r"localhost\SQLEXPRESS"
DATABASE = "TechMartDB"

# Try ODBC Driver 17 first, and Driver 18 if it is not available.
# Both drivers work with SQL Server.
DRIVERS_TO_TRY = [
    "ODBC Driver 17 for SQL Server",
    "ODBC Driver 18 for SQL Server",
]


def get_connection():
    """Create a SQL Server connection and return it."""
    last_error = None
    for driver in DRIVERS_TO_TRY:
        try:
            conn_str = (
                f"DRIVER={{{driver}}};"
                f"SERVER={SERVER};"
                f"DATABASE={DATABASE};"
                "Trusted_Connection=yes;"
            )
            return pyodbc.connect(conn_str)
        except pyodbc.Error as e:
            last_error = e
    # If both drivers fail, raise the error.
    raise last_error
