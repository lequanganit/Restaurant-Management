from app.models import VAT, Discount
from decimal import Decimal
from app.BillTemplate.DefaultBillCaculator import DefaultBillCaculator

def stats_cart(cart):
    total_quantity = 0
    total_amount = 0
    if cart:
        for item in cart.values():
            total_quantity += item["quantity"]
            total_amount += item["quantity"]*item["price"]
    return {
        'total_quantity': total_quantity,
        'total_amount': total_amount
    }

def calculate_bill(subtotal):
    calculator = DefaultBillCaculator()
    return calculator.calculate(subtotal)
