from flask import session
from app import utils

def add_to_cart_service(data):
    table_id = str(data.get("table_id"))
    food_id = str(data.get("id"))

    carts = session.get("cart", {})

    if table_id not in carts:
        carts[table_id] = {}

    table_cart = carts[table_id]

    if food_id in table_cart:
        table_cart[food_id]["quantity"] += 1
    else:
        table_cart[food_id] = {
            "id": food_id,
            "name": data.get("name"),
            "price": data.get("price"),
            "quantity": 1,
            "note": data.get("note", "")
        }

    session["cart"] = carts
    return utils.stats_cart(table_cart)

def update_cart_quantity_service(table_id, food_id, quantity):
    carts = session.get("cart", {})

    if table_id in carts and food_id in carts[table_id]:
        carts[table_id][food_id]["quantity"] = int(quantity)

    session["cart"] = carts
    return utils.stats_cart(carts.get(table_id, {}))

def delete_cart_item_service(table_id, food_id):
    carts = session.get("cart", {})

    if table_id in carts and food_id in carts[table_id]:
        del carts[table_id][food_id]

    session["cart"] = carts
    return utils.stats_cart(carts.get(table_id, {}))

def update_cart_note_service(table_id, food_id, note):
    carts = session.get("cart", {})

    if table_id in carts and food_id in carts[table_id]:
        carts[table_id][food_id]["note"] = note or ""

    session["cart"] = carts
