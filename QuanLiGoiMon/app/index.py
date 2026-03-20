from flask import render_template, request, redirect, jsonify, session, abort
import math
from app import app, dao, login, utils, notifications, admin
from app.services import order_service, cash_service, cart_service, cook_service
from flask_login import login_user, logout_user, current_user
from app.models import UserRole, ROLES, FoodOrderStatus
from functools import wraps
from datetime import datetime

# controler

@app.route('/')
def index(): # ham route toi trang chu
    return render_template('index.html') # phan hoi ve 1 trang web

@app.route('/login')
def login_view(): # ham toi trang dang nhap
    return render_template('login.html')

@app.route('/logout')
def logout_process(): # ham dang xuat
    logout_user()
    return redirect('/login')

# login
@app.route('/login', methods=['post'])
def login_process():
    username = request.form.get('username').strip()
    password = request.form.get('password').strip()

    if not username or not password:
        return render_template('login.html', err_msg="Vui lòng không để trống tên đăng nhập hoặc mật khẩu!")
    user = dao.auth_user(username=username, password=password)

    if user:
        login_user(user=user)
        role_name = ROLES.get(user.user_role)
        next = request.args.get('next')
        if role_name:
            return redirect(next if next else f'/{role_name["name"]}')
    else:
        return render_template('login.html', err_msg="Sai tên đăng nhập hoặc mật khẩu!")

# decorator kiem tra role
def role_required(*allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect('/login')

            if current_user.user_role not in allowed_roles:
                abort(403)

            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.route('/waiter')
@role_required(UserRole.PHUCVU)
def waiter(): # ham toi trang goi mon
    tables = dao.load_tables(kw=request.args.get("kw"))
    return render_template('waiter.html', table=tables)

@app.route('/cook')
@role_required(UserRole.NHABEP)
def cook():
    status = request.args.get("status", default="pending")
    if status == 'pending':
        orders = cook_service.get_orders_by_status(FoodOrderStatus.PENDING)
    elif status == 'cooking':
        orders = cook_service.get_orders_by_status(FoodOrderStatus.COOKING)
    else:
        orders = []

    return render_template('cook.html', orders=orders, status=status)

@app.route('/cashier')
@role_required(UserRole.THUNGAN)
def cashier():
    kw = request.args.get("kw")
    page = request.args.get("page", 1, type=int)
    tables = dao.load_serving_tables(kw=kw, page=page)
    total = dao.count_serving_table()
    pages = math.ceil(total / app.config["TABLE_SIZE"])
    return render_template("cashier.html",tables=tables,pages=pages)
@app.route('/manager')
@role_required(UserRole.QUANLI)
def manager():
    report_type = request.args.get("type", "day")
    from_date = request.args.get("from_date")
    to_date = request.args.get("to_date")
    if report_type == "month":
        year = int(request.args.get("year"))
        revenues = dao.revenue_by_month(year)
        top_foods = []
        food_ratios = dao.food_ratio(year=year)
    else:
        revenues = dao.revenue_by_day(from_date, to_date)
        top_foods = dao.top_foods_by_date(from_date, to_date)
        food_ratios = dao.food_ratio(from_date=from_date, to_date=to_date)
    return render_template(
        "manager.html",
        revenues=revenues,
        top_foods=top_foods,
        food_ratios=food_ratios,
    )

# truyen role cho html
@app.context_processor
def inject_roles():
    user_role = ROLES.get(current_user.user_role) if current_user.is_authenticated else None
    return dict(user_role=user_role)


# nhan nut order render order.html
@app.route("/order/<int:table_id>")
@role_required(UserRole.PHUCVU)
def order(table_id):
    table = dao.get_table_by_id(table_id=table_id)
    categories = dao.load_categories()
    category_id = request.args.get("category_id", type=int)
    kw = request.args.get("keyword")
    foods = dao.load_foods(category_id=category_id, kw=kw, page=int(request.args.get("page", 1)))
    pages = math.ceil(dao.count_foods(category_id=category_id, kw=kw) / app.config["FOOD_SIZE"])
    page = int(request.args.get("page", 1))
    carts = session.get("cart", {})
    table_cart = carts.get(str(table_id), {})
    return render_template("order.html", table=table, foods=foods, categories=categories, pages=pages, page=page, cart_stats=utils.stats_cart(table_cart))

# order api
@app.route('/api/orders/<int:table_id>', methods=['post'])
def call_order_api(table_id):
    return order_service.call_order(table_id)
# cancel
@app.route('/api/orders/<int:table_id>/cancel', methods=['delete'])
def cancel_order_api(table_id):
    return order_service.cancel_order(table_id)

# cart api
@app.route('/api/carts', methods=['post'])
def add_to_cart():
    return jsonify(
        cart_service.add_to_cart_service(request.json)
    )

@app.route('/api/carts/<table_id>/<food_id>', methods=['put'])
def update_to_cart_quantity(table_id, food_id):
    return jsonify(
        cart_service.update_cart_quantity_service(table_id, food_id, request.json.get("quantity"))
    )

@app.route('/api/carts/<table_id>/<food_id>', methods=['delete'])
def delete_to_cart(table_id, food_id):
    return jsonify(
        cart_service.delete_cart_item_service(table_id, food_id)
    )

@app.route('/api/carts/<table_id>/<food_id>/note', methods=['put'])
def update_to_cart_note(table_id, food_id):
    cart_service.update_cart_note_service(table_id, food_id, request.json.get("note"))
    return jsonify({"success": True})

# render cart.html
@app.route('/cart/<int:table_id>')
@role_required(UserRole.PHUCVU)
def cart_view(table_id):
    carts = session.get('cart', {})
    table_cart = carts.get(str(table_id), {})

    return render_template("cart.html", cart=table_cart, cart_stats=utils.stats_cart(table_cart), table_id=table_id)

@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)

@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403

@app.route('/debug/clear-session')
def clear_session():
    session.clear()
    return "Session cleared"
#render bill.html
@app.route("/bill/<int:table_id>")
@role_required(UserRole.THUNGAN)
def bill(table_id):
    data = dao.get_bill_by_table(table_id)
    return render_template("bill.html", data=data,now=datetime.now())

@app.route("/api/pay/<int:table_id>", methods=["post"])
def pay(table_id):
    success = cash_service.close_order(table_id, current_user.id)
    if not success:
        return jsonify({"message": "Thanh toán thất bại"}), 400
    return jsonify({"message": "Thanh toán thành công"}), 200

# ======== cook code duoi nay

@app.route('/api/cook/accept/<int:order_id>', methods=['post'])
def accept_food_order(order_id):
    cook_service.update_status_food_order(order_id, FoodOrderStatus.COOKING)
    return jsonify({"success": True})
@app.route('/api/cook/rerender', methods=['post'])
def rerender_done():
    app.config["RERENDER"] = False
    return jsonify({"success": True})

@app.route('/api/cook/rerender')
def check_rerender():
    return jsonify({"rerender": app.config["RERENDER"]})

@app.route('/api/cook/complete/<int:order_id>', methods=['post'])
def complete_food_order(order_id):
    data = request.get_json()
    table_name = data.get("table_name")
    user_id = data.get("user_id")
    cook_service.update_status_food_order(order_id, FoodOrderStatus.DONE, FoodOrderStatus.COOKING)
    cook_service.notify_waiter(table_name, user_id)
    return jsonify({"success": True})

@app.route('/api/notify')
def get_notify():
    if current_user.id in notifications and len(notifications[current_user.id]) > 0:
        return jsonify(notifications[current_user.id].pop(0))
    return jsonify({})

if __name__ == '__main__':
    app.run(debug=True)