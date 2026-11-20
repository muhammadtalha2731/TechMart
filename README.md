# TechMart - Electronics Store (Flask + SQL Server)

This project is built in Visual Studio Code. All the code is in Python Flask and the database is in SQL Server Management Studio 2022 (SSMS). No XAMPP, PHP or MySQL is used.

## Tech Stack
- Frontend: HTML + CSS + Jinja Templates
- Backend: Python Flask
- Database: SQL Server 2022, server `localhost\SQLEXPRESS`, database `TechMartDB`
- Connection: pyodbc, Windows Authentication

## Setup - Step by Step

### Step 1: Check Python
Open the terminal in VS Code (Terminal menu > New Terminal) and run:
```
python --version
```
If no version is shown, download Python from python.org and, during installation, make sure to tick **"Add Python to PATH"**.

### Step 2: Check the ODBC Driver
**ODBC Driver 17 for SQL Server** is needed to connect to SQL Server. It is usually installed with SQL Server. If you get a driver error when running `python app.py`, download and install "ODBC Driver 17 for SQL Server" from Microsoft's website.

### Step 3: Install the packages
Open this folder in VS Code, then run in the terminal:
```
pip install -r requirements.txt
```

### Step 4: Create the database (in SSMS)
1. Open SSMS and connect to `localhost\SQLEXPRESS` (Windows Authentication).
2. Open a New Query.
3. Open the file `techmart_sqlserver.sql` from this folder, copy the whole code, paste it into the query and press **Run (F5)**.
4. Verify: `SELECT * FROM Products;` should show 60 products (15 in each category).

### Step 4b: Add the extra 48 products (only if the database already exists)
If you already created the database with the older 12-product file, do NOT run `techmart_sqlserver.sql` again. Instead, open the file `add_products.sql`, copy the whole code, paste it into a New Query in SSMS and press **Run (F5)**. It only adds products 13 to 60. Verify: `SELECT COUNT(*) FROM Products;` should show 60.

### Step 5: Create the admin account
Run in the terminal:
```
python create_admin.py
```
This creates the admin@techmart.com / admin123 account (the password is saved as a hash).
If the admin already exists, you can also change its role in SSMS:
```sql
UPDATE Users SET Role = 'admin' WHERE Email = 'admin@techmart.com';
```

### Step 6: Run the website
Run in the terminal:
```
python app.py
```
Then open in your browser: **http://127.0.0.1:5000**

Admin login: admin@techmart.com / admin123

## Folder Structure
```
techmart_flask/
  app.py                  - All routes: home, products, cart, checkout, login, admin
  config.py               - SQL Server connection (localhost\SQLEXPRESS, TechMartDB)
  create_admin.py         - Script to create the admin account
  requirements.txt        - Flask, pyodbc, Werkzeug
  techmart_sqlserver.sql  - Database file to run in SSMS (creates TechMartDB with 60 products)
  add_products.sql        - Adds products 13 to 60 to a database that already exists
  update_images.sql       - Updates the 12 product photos in a database that already exists
  templates/              - HTML pages (base, index, products, product, cart, checkout, login, register, orders)
  templates/admin/        - Admin pages (dashboard, products, orders)
  static/css/style.css    - One CSS file, professional blue theme, with hover + animation
  static/images/          - Real product photos (60 files, one per product)
```

## Features
- Customer: Home, Products, Search, Category Filter, Product Detail, Cart, Checkout (Cash on Delivery), Login/Register, My Orders
- Admin: Dashboard (total products, orders, users, sales), Product Add/Delete, Orders Status Change (Pending to Delivered)
