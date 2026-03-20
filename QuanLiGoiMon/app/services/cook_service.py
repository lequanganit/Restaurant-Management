from flask import jsonify
from app import db, dao, app
from app.models import FoodOrderStatus
from app.services.notification_service import add_notification, create_message_to_waiter

def move_new_food_orders_to_pending():
    app.config["RERENDER"] = True
    return jsonify({"success": True})

def update_status_food_order(order_id, new_status, old_status=FoodOrderStatus.PENDING):
    food_order = dao.get_food_orders_by_order_id_status(order_id, old_status)
    
    for fo in food_order:
        fo.status = FoodOrderStatus(new_status)
    db.session.commit()

def get_orders_by_status(status):
    orders = []
    food_orders = dao.get_food_orders_by_status(status)
    orders_dict = {}
    for fo in food_orders:
        order_id = fo.order_id
        if order_id not in orders_dict:
            orders_dict[order_id] = {
                "order_id": order_id,
                "table_name": fo.order.table.name,
                "user_id": fo.user_id,
                "food_orders": []
            }
        orders_dict[order_id]["food_orders"].append({
            "id": fo.id,
            "food_name": fo.food.name,
            "quantity": fo.quantity,
            "note": fo.note
        })
    orders.extend(orders_dict.values())
    return orders

def notify_waiter(table_name, user_id):
    message = create_message_to_waiter(table_name)
    add_notification(user_id, message)