from app.services.cook_service import move_new_food_orders_to_pending
from flask import session
from app import db, dao
from app.models import TableStatus
from flask_login import current_user
from app.responses.error import NotAuthenticatedError, TableNotFoundError, EmptyCartError, ErrorResponse
from app.responses.success import SuccessCreated, SuccessOK

def call_order(table_id):
    carts = session.get("cart", {})
    table_cart = carts.get(str(table_id))

    if not current_user.is_authenticated:
        return NotAuthenticatedError().to_response()

    table = dao.get_table_by_id(table_id)
    if not table:
        return TableNotFoundError().to_response()

    if not table_cart:
        return EmptyCartError().to_response()

    try:
        order = dao.get_open_order_by_table_id(table_id)

        if not order:
            order = dao.create_order(user_id=current_user.id, table_id=table_id)
            table.status = TableStatus.SERVING

        for item in table_cart.values():
            food_id = int(item["id"])
            quantity = int(item["quantity"])
            note = item.get("note", "").strip()
            user_id = current_user.id

            food_order = dao.add_food_to_order(order_id=order.id, food_id=food_id, quantity=quantity, note=note, user_id=user_id)

        #   luu db
        db.session.commit()

        move_new_food_orders_to_pending()

        # xoa session khi cap nhap xong
        del carts[str(table_id)]
        session["cart"] = carts
        return SuccessCreated().to_response()

    except Exception as ex:
        db.session.rollback()
        print(ex)
        return ErrorResponse().to_response()

def cancel_order(table_id):
    carts = session.get("cart", {})

    if str(table_id) not in carts:
        return EmptyCartError().to_response()

    del carts[str(table_id)]
    session["cart"] = carts

    return SuccessOK("Đã hủy gọi món").to_response()