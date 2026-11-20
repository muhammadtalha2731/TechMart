# TechMart - Database connection settings
# This file is only for connecting to the database.
#
# On the laptop (local run), it uses the defaults below:
#   Server: localhost\SQLEXPRESS (SQL Server 2022, same name as in SSMS)
#   Database: TechMartDB
#   Login: Windows Authentication (Trusted_Connection=yes)
#   This means: it connects with the Windows user logged in on the laptop.
#   No separate username/password is needed in SSMS.
#
# On the live server (deploy), the same settings come from environment
# variables instead, so no password is ever written in the code:
#   DB_SERVER   - e.g. techmart-server.database.windows.net (Azure SQL)
#   DB_NAME     - e.g. TechMartDB
#   DB_USER     - e.g. techmart_admin (SQL login, Azure SQL)
#   DB_PASSWORD - the SQL login password (set on the hosting site only)
#   DB_DRIVER   - optional, e.g. "ODBC Driver 18 for SQL Server"
# If DB_USER is empty, Windows Authentication is used (local run).

import os

import pyodbc

SERVER = os.environ.get("DB_SERVER", r"localhost\SQLEXPRESS")
DATABASE = os.environ.get("DB_NAME", "TechMartDB")
DB_USER = os.environ.get("DB_USER", "")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "")
DB_DRIVER = os.environ.get("DB_DRIVER", "")

# Try ODBC Driver 18 first, and Driver 17 if it is not available.
# Both drivers work with SQL Server.
DRIVERS_TO_TRY = [DB_DRIVER] if DB_DRIVER else [
    "ODBC Driver 18 for SQL Server",
    "ODBC Driver 17 for SQL Server",
]


def build_connection_string(driver):
    """Build the ODBC connection string for one driver."""
    parts = [
        f"DRIVER={{{driver}}};",
        f"SERVER={SERVER};",
        f"DATABASE={DATABASE};",
    ]
    if DB_USER:
        # SQL login (used on the live server / Azure SQL).
        parts.append(f"UID={DB_USER};")
        parts.append(f"PWD={DB_PASSWORD};")
        parts.append("Encrypt=yes;")
        parts.append("TrustServerCertificate=no;")
    else:
        # Windows Authentication (used on the laptop).
        parts.append("Trusted_Connection=yes;")
    return "".join(parts)


def get_connection():
    """Create a SQL Server connection and return it."""
    last_error = None
    for driver in DRIVERS_TO_TRY:
        try:
            return pyodbc.connect(build_connection_string(driver))
        except pyodbc.Error as e:
            last_error = e
    # If both drivers fail, raise the error.
    raise last_error
