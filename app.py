# TechMart - Electronics Store
# Python Flask + SQL Server (SSMS 2022, localhost\SQLEXPRESS)
# How to run:  python app.py
# Then open in your browser:  http://127.0.0.1:5000

from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from config import get_connection

app = Flask(__name__)
# Secret key for sessions. Change this in your project.
app.secret_key = "techmart-secret-key-change-this"


@app.context_processor
def inject_categories():
    """Make the category list available in every template (e.g. the footer)."""
    try:
        return {"nav_categories": get_categories()}
    except Exception:
        return {"nav_categories": []}


# ---------- Helper functions ----------

def resolve_image(image, product_id):
    """Return the full image URL for a product.

    - A full http(s) URL is used as it is.
    - A file name like 'iphone-13.jpg' is a local file in static/images/.
    - Anything else (e.g. an old seed like 'galaxy-a55') falls back to picsum.
    """
    if image and image.startswith("http"):
        return image
    if image and image.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
        return url_for("static", filename="images/" + image)
    return "https://picsum.photos/seed/" + str(image or product_id) + "/600/400"


def get_products(category_id=None, search=None):
    """Fetch the product list. Category or search filter can be applied."""
    conn = get_connection()
    cursor = conn.cursor()
    sql = "SELECT Id, CategoryId, Name, Description, Price, OldPrice, Image, Stock FROM Products"
    params = []
    conditions = []
    if category_id:
        conditions.append("CategoryId = ?")
        params.append(int(category_id))
    if search:
        conditions.append("(Name LIKE ? OR Description LIKE ?)")
        params.append("%" + search + "%")
        params.append("%" + search + "%")
    if conditions:
        sql += " WHERE " + " AND ".join(conditions)
    sql += " ORDER BY Id"
    cursor.execute(sql, params)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    # Convert each row to a dict so templates can use it easily.
    products = []
    for r in rows:
        products.append({
            "Id": r[0], "CategoryId": r[1], "Name": r[2],
            "Description": r[3], "Price": r[4], "OldPrice": r[5],
            "Image": resolve_image(r[6], r[0]), "Stock": r[7],
        })
    return products


def get_categories():
    """Fetch all categories."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT Id, Name, Description FROM Categories ORDER BY Id")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return [{"Id": r[0], "Name": r[1], "Description": r[2]} for r in rows]


def get_product(product_id):
    """Fetch one product by id, or return None."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT Id, CategoryId, Name, Description, Price, OldPrice, Image, Stock "
        "FROM Products WHERE Id = ?", (product_id,)
    )
    r = cursor.fetchone()
    cursor.close()
    conn.close()
    if not r:
        return None
    return {"Id": r[0], "CategoryId": r[1], "Name": r[2], "Description": r[3],
            "Price": r[4], "OldPrice": r[5], "Image": resolve_image(r[6], r[0]), "Stock": r[7]}


def login_required(func):
    """Check that the user is logged in."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            flash("Please login first.")
            return redirect(url_for("login"))
        return func(*args, **kwargs)
    return wrapper


def admin_required(func):
    """Check that the user is an admin."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get("role") != "admin":
            flash("This page is for admin only.")
            return redirect(url_for("login"))
        return func(*args, **kwargs)
    return wrapper


def get_cart_items():
    """Get product details and the total for the session cart."""
    cart = session.get("cart", {})  # {product_id: quantity}
    items = []
    total = 0
    for pid, qty in cart.items():
        product = get_product(int(pid))
        if product:
            subtotal = product["Price"] * qty
            total += subtotal
            items.append({"product": product, "quantity": qty, "subtotal": subtotal})
    return items, total


# ---------- Customer pages ----------

@app.route("/")
def home():
    products = get_products()
    categories = get_categories()
    return render_template("index.html", products=products, categories=categories)


@app.route("/products")
def products():
    category_id = request.args.get("category")
    search = request.args.get("search")
    all_products = get_products(category_id, search)
    categories = get_categories()
    selected_category_name = None
    if category_id:
        for cat in categories:
            if str(cat["Id"]) == str(category_id):
                selected_category_name = cat["Name"]
                break
    return render_template("products.html", products=all_products,
                           categories=categories,
                           selected_category=category_id, search=search,
                           selected_category_name=selected_category_name)


@app.route("/product/<int:product_id>")
def product_detail(product_id):
    product = get_product(product_id)
    if not product:
        flash("Product not found.")
        return redirect(url_for("products"))
    return render_template("product.html", product=product)


@app.route("/add_to_cart/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):
    quantity = int(request.form.get("quantity", 1))
    if quantity < 1:
        quantity = 1
    cart = session.get("cart", {})
    key = str(product_id)
    cart[key] = cart.get(key, 0) + quantity
    session["cart"] = cart
    flash("Product added to cart.")
    return redirect(url_for("cart_page"))


@app.route("/cart")
def cart_page():
    items, total = get_cart_items()
    return render_template("cart.html", items=items, total=total)


@app.route("/update_cart", methods=["POST"])
def update_cart():
    cart = session.get("cart", {})
    for key in list(cart.keys()):
        qty = request.form.get("qty_" + key)
        if qty is not None:
            qty = int(qty)
            if qty <= 0:
                del cart[key]
            else:
                cart[key] = qty
    session["cart"] = cart
    flash("Cart updated.")
    return redirect(url_for("cart_page"))


@app.route("/remove_from_cart/<int:product_id>")
def remove_from_cart(product_id):
    cart = session.get("cart", {})
    cart.pop(str(product_id), None)
    session["cart"] = cart
    flash("Product removed from cart.")
    return redirect(url_for("cart_page"))


@app.route("/checkout", methods=["GET", "POST"])
@login_required
def checkout():
    items, total = get_cart_items()
    if not items:
        flash("Your cart is empty. Please add a product first.")
        return redirect(url_for("products"))

    if request.method == "POST":
        # Save the order: first into Orders, then into OrderItems.
        # OUTPUT INSERTED.Id returns the new order id with the INSERT
        # itself, so we never depend on SCOPE_IDENTITY().
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Orders (UserId, TotalAmount, Status, PaymentMethod) "
            "OUTPUT INSERTED.Id "
            "VALUES (?, ?, 'Pending', 'Cash on Delivery')",
            (session["user_id"], total),
        )
        # Get the new order id.
        order_id = int(cursor.fetchone()[0])
        for item in items:
            cursor.execute(
                "INSERT INTO OrderItems (OrderId, ProductId, Quantity, Price) "
                "VALUES (?, ?, ?, ?)",
                (order_id, item["product"]["Id"], item["quantity"],
                 item["product"]["Price"]),
            )
            # Decrease the stock.
            cursor.execute(
                "UPDATE Products SET Stock = Stock - ? WHERE Id = ?",
                (item["quantity"], item["product"]["Id"]),
            )
        conn.commit()
        cursor.close()
        conn.close()
        session["cart"] = {}
        return render_template("checkout.html", items=[], total=0,
                               order_id=order_id, success=True)

    return render_template("checkout.html", items=items, total=total,
                           order_id=None, success=False)


@app.route("/orders")
@login_required
def my_orders():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT Id, TotalAmount, Status, PaymentMethod, CreatedAt "
        "FROM Orders WHERE UserId = ? ORDER BY Id DESC",
        (session["user_id"],),
    )
    rows = cursor.fetchall()
    orders = []
    for r in rows:
        # Also fetch the items of each order.
        cursor.execute(
            "SELECT p.Name, oi.Quantity, oi.Price "
            "FROM OrderItems oi JOIN Products p ON oi.ProductId = p.Id "
            "WHERE oi.OrderId = ?", (r[0],)
        )
        items = [{"Name": x[0], "Quantity": x[1], "Price": x[2]}
                 for x in cursor.fetchall()]
        orders.append({"Id": r[0], "TotalAmount": r[1], "Status": r[2],
                       "PaymentMethod": r[3], "CreatedAt": r[4], "items": items})
    cursor.close()
    conn.close()
    return render_template("orders.html", orders=orders)


# ---------- Login / Register / Logout ----------

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        phone = request.form.get("phone", "").strip()
        address = request.form.get("address", "").strip()
        if not name or not email or not password:
            flash("Name, Email and Password are required.")
            return render_template("register.html")
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT Id FROM Users WHERE Email = ?", (email,))
        if cursor.fetchone():
            flash("This email is already registered.")
            cursor.close()
            conn.close()
            return render_template("register.html")
        hashed = generate_password_hash(password)
        cursor.execute(
            "INSERT INTO Users (Name, Email, Password, Phone, Address, Role) "
            "VALUES (?, ?, ?, ?, ?, 'customer')",
            (name, email, hashed, phone, address),
        )
        conn.commit()
        cursor.close()
        conn.close()
        flash("Account created. Please login now.")
        return redirect(url_for("login"))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT Id, Name, Email, Password, Role FROM Users WHERE Email = ?",
            (email,),
        )
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if user and check_password_hash(user[3], password):
            session["user_id"] = user[0]
            session["user_name"] = user[1]
            session["role"] = user[4]
            flash("Login successful. Welcome, " + user[1] + "!")
            if user[4] == "admin":
                return redirect(url_for("admin_dashboard"))
            return redirect(url_for("home"))
        flash("Incorrect email or password.")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for("home"))


# ---------- Admin pages ----------

@app.route("/admin")
@admin_required
def admin_dashboard():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM Products")
    total_products = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM Orders")
    total_orders = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM Users")
    total_users = cursor.fetchone()[0]
    cursor.execute("SELECT ISNULL(SUM(TotalAmount), 0) FROM Orders")
    total_sales = cursor.fetchone()[0]
    cursor.execute("SELECT TOP 5 Id, TotalAmount, Status, CreatedAt FROM Orders ORDER BY Id DESC")
    recent = [{"Id": r[0], "TotalAmount": r[1], "Status": r[2], "CreatedAt": r[3]}
              for r in cursor.fetchall()]
    cursor.close()
    conn.close()
    return render_template("admin/dashboard.html",
                           total_products=total_products,
                           total_orders=total_orders,
                           total_users=total_users,
                           total_sales=total_sales,
                           recent_orders=recent)


@app.route("/admin/products", methods=["GET", "POST"])
@admin_required
def admin_products():
    conn = get_connection()
    cursor = conn.cursor()
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        category_id = int(request.form.get("category_id", 1))
        description = request.form.get("description", "").strip()
        price = float(request.form.get("price", 0))
        old_price = request.form.get("old_price")
        old_price = float(old_price) if old_price else None
        stock = int(request.form.get("stock", 0))
        image = request.form.get("image", "").strip() or "new-product"
        cursor.execute(
            "INSERT INTO Products (CategoryId, Name, Description, Price, OldPrice, Image, Stock) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (category_id, name, description, price, old_price, image, stock),
        )
        conn.commit()
        flash("Product added successfully.")
        return redirect(url_for("admin_products"))
    cursor.execute("SELECT Id, CategoryId, Name, Price, Stock FROM Products ORDER BY Id")
    products = [{"Id": r[0], "CategoryId": r[1], "Name": r[2],
                 "Price": r[3], "Stock": r[4]} for r in cursor.fetchall()]
    cursor.execute("SELECT Id, Name FROM Categories ORDER BY Id")
    categories = [{"Id": r[0], "Name": r[1]} for r in cursor.fetchall()]
    cursor.close()
    conn.close()
    return render_template("admin/products.html", products=products, categories=categories)


@app.route("/admin/products/delete/<int:product_id>")
@admin_required
def admin_delete_product(product_id):
    conn = get_connection()
    cursor = conn.cursor()
    # First check: if this product has order items, it cannot be deleted.
    cursor.execute("SELECT COUNT(*) FROM OrderItems WHERE ProductId = ?", (product_id,))
    used = cursor.fetchone()[0]
    if used > 0:
        flash("This product is part of an order, so it cannot be deleted.")
    else:
        cursor.execute("DELETE FROM Products WHERE Id = ?", (product_id,))
        conn.commit()
        flash("Product deleted successfully.")
    cursor.close()
    conn.close()
    return redirect(url_for("admin_products"))


@app.route("/admin/orders")
@admin_required
def admin_orders():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT o.Id, u.Name, o.TotalAmount, o.Status, o.PaymentMethod, o.CreatedAt "
        "FROM Orders o LEFT JOIN Users u ON o.UserId = u.Id ORDER BY o.Id DESC"
    )
    orders = [{"Id": r[0], "UserName": r[1], "TotalAmount": r[2], "Status": r[3],
               "PaymentMethod": r[4], "CreatedAt": r[5]} for r in cursor.fetchall()]
    cursor.close()
    conn.close()
    return render_template("admin/orders.html", orders=orders)


@app.route("/admin/orders/update/<int:order_id>", methods=["POST"])
@admin_required
def admin_update_order(order_id):
    new_status = request.form.get("status", "Pending")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE Orders SET Status = ? WHERE Id = ?", (new_status, order_id))
    conn.commit()
    cursor.close()
    conn.close()
    flash("Order status updated.")
    return redirect(url_for("admin_orders"))


if __name__ == "__main__":
    # debug=True means: the server restarts automatically when code changes.
    app.run(debug=True)
