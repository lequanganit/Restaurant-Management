# file xu li truy van db
from app import app, db
from app.models import Category, Table, Food, User, Order, FoodOrder, FoodOrderStatus, TableStatus, OrderStatus,Bill , VAT, Discount
from app.utils import calculate_bill
import hashlib
from datetime import datetime, time
from sqlalchemy import func
from sqlalchemy.orm import joinedload

def load_categories():
    return Category.query.filter(Category.active == True).all()

def load_foods(category_id=None, kw=None, page=1):
    query = Food.query.filter(Food.active == True)

    if kw:
        query = query.filter(Food.name.contains(kw))

    if category_id:
        query = query.filter(Food.category_id == category_id)

    if page:
        start = (page-1) * app.config["FOOD_SIZE"]
        end = start + app.config["FOOD_SIZE"]
        query = query.slice(start, end)

    return query.all()


def count_foods(category_id=None, kw=None):
    query = Food.query.filter(Food.active)

    if kw:
        query = query.filter(Food.name.contains(kw))

    if category_id:
        query = query.filter(Food.category_id == category_id)

    return query.count()

def load_tables(kw=None):
    query = Table.query.filter(Table.active == True)

    if kw:
        query = query.filter(Table.name.contains(kw))

    return query.all()


def get_table_by_id(table_id):
    return Table.query.get(table_id)

def get_user_by_id(user_id):
    return User.query.get(user_id)

# chung thuc nguoi dung
def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    return User.query.filter(User.username==username.strip(), User.password==password).first()

def get_open_order_by_table_id(table_id):
    return Order.query.filter(
        Order.table_id == table_id,
        Order.status == OrderStatus.OPEN
    ).first()

# lay mon an pending co kem note
def get_pending_food(order_id, food_id, note, user_id):
    return FoodOrder.query.filter(
        FoodOrder.order_id == order_id,
        FoodOrder.food_id == food_id,
        func.lower(FoodOrder.note) == func.lower(note),
        FoodOrder.user_id == user_id,
        FoodOrder.status == FoodOrderStatus.PENDING
    ).first()

# lấy food order theo id và có status, để cập nhật status
def get_food_orders_by_order_id_status(order_id, status):
    return FoodOrder.query.filter(FoodOrder.order_id == order_id, FoodOrder.status == status).all()

# query tất cả food order theo status, để render giao diện (chỉ cần 1 câu query)
def get_food_orders_by_status(status):
    return FoodOrder.query.filter(FoodOrder.status == status).options(joinedload(FoodOrder.food), joinedload(FoodOrder.order).joinedload(Order.table)).all()

def get_food_price(food_id):
    food = Food.query.get(food_id)
    if food:
        return food.price
    return 0

def create_order(user_id, table_id):
    order = Order(
        user_id=user_id,
        table_id=table_id,
        status=OrderStatus.OPEN
    )
    db.session.add(order)
    db.session.flush()  # lấy order.id
    return order

def add_food_to_order(order_id, food_id, quantity, note, user_id):
    food = get_pending_food(order_id, food_id, note, user_id)
    food_price = get_food_price(food_id)
    if food:
        food.quantity += quantity
    else:
        food = FoodOrder(
            order_id=order_id,
            food_id=food_id,
            user_id=user_id,
            quantity=quantity,
            price=food_price,
            note=note
        )
        print(food)
        db.session.add(food)
    db.session.flush()
    return food

def load_serving_tables(kw=None,page=1):
    query=Table.query.join(Order).filter(Table.status == TableStatus.SERVING,Order.status == OrderStatus.OPEN)
    if kw:
        query = query.filter(Table.name.contains(kw))
    if page:
        start = (page-1) * app.config["TABLE_SIZE"]
        end = start + app.config["TABLE_SIZE"]
        query = query.slice(start, end)
    return query.all()
def count_serving_table():
    query = Table.query.join(Order).filter(Table.status == TableStatus.SERVING,Order.status == OrderStatus.OPEN)
    return query.count()
def get_bill_by_table(table_id):
    order = Order.query.filter(
        Order.table_id == table_id,
        Order.status == OrderStatus.OPEN
    ).first()
    if not order:
        return None
    order_items = (
        db.session.query(
            Food.id,
            Food.name,
            FoodOrder.price,
            func.sum(FoodOrder.quantity).label("quantity"),
            func.sum(FoodOrder.quantity * FoodOrder.price).label("total")
        ).join(Food, Food.id == FoodOrder.food_id).filter(FoodOrder.order_id == order.id)
        .group_by(Food.id, Food.name, FoodOrder.price)
        .all()
    )
    subtotal = sum(item.total for item in order_items)
    summary = calculate_bill(subtotal)
    return {
        "order": order,
        "order_items":  order_items,
        "subtotal": subtotal,
        "summary": summary
    }
#Thong ke bao cao
def apply_date_filter(query, column, from_date_str=None, to_date_str=None):
    if from_date_str:
        from_date = datetime.strptime(from_date_str, "%Y-%m-%d")
        query = query.filter(column >= from_date)
    if to_date_str:
        to_date = datetime.strptime(to_date_str, "%Y-%m-%d")
        to_date = datetime.combine(to_date.date(), time(23, 59, 59))
        query = query.filter(column <= to_date)
    return query
def revenue_by_day(from_date=None, to_date=None):
    query1 = db.session.query(
        func.date(Bill.created_date),
        func.sum(Bill.total_amount))
    query = apply_date_filter(query1,Bill.created_date,from_date,to_date).group_by(func.date(Bill.created_date)).order_by(func.date(Bill.created_date))
    return query.all()
def top_foods_by_date(from_date=None, to_date=None, limit=5):
    if not from_date and not to_date:
        return []
    query1 = (db.session.query(
        Food.name,
        func.sum(FoodOrder.quantity)
    ).join(FoodOrder, Food.id == FoodOrder.food_id).join(Order, Order.id == FoodOrder.order_id)
    .filter(Order.status == OrderStatus.CLOSE))
    query = apply_date_filter(query1,FoodOrder.created_date,from_date,to_date).group_by(Food.name).order_by(func.sum(FoodOrder.quantity).desc()).limit(limit)
    return query.all()
def revenue_by_month(year=None):
    if not year:
        year = datetime.now().year
    query=db.session.query(
        func.month(Bill.created_date),
        func.sum(Bill.total_amount)
    ).filter(func.year(Bill.created_date) == year).group_by(func.month(Bill.created_date)).order_by(func.month(Bill.created_date))
    return query.all()
def food_ratio(from_date=None, to_date=None, year=None):
    query1 = (db.session.query(
            Food.name,
            func.sum(FoodOrder.quantity)
        ).join(FoodOrder, Food.id == FoodOrder.food_id).join(Order, Order.id == FoodOrder.order_id).filter(Order.status == OrderStatus.CLOSE).group_by(Food.name)
    )
    if year:
        query = query1.filter(func.year(FoodOrder.created_date) == year)
    else:
        query = apply_date_filter(
            query1,
            FoodOrder.created_date,
            from_date,
            to_date
        )
    return query.all()