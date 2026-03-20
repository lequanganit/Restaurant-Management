from app import db, dao
from app.models import OrderStatus, TableStatus, Bill, FoodOrderStatus
def close_order(table_id, cashier_id):
    try:
        order = dao.get_open_order_by_table_id(table_id)
        if not order:
            return False
        not_done = any(fo.status != FoodOrderStatus.DONE for fo in order.order_foods)
        if not_done:
            return False
        bill_data = dao.get_bill_by_table(table_id)
        if not bill_data:
            return False
        table = order.table
        order.status = OrderStatus.CLOSE
        if table:
            table.status = TableStatus.EMPTY
        bill = Bill(
            total_amount=bill_data["summary"]["total"],
            order_id=order.id,
            user_id=cashier_id,
            vat_id=1,
            discount_id=1
        )
        db.session.add(bill)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print("Lỗi thanh toán:", e)
        return False