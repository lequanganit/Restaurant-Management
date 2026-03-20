from decimal import Decimal
from app.models import VAT
from app.models import Discount
from app.BillTemplate.BillCalculatorTemplate import BillCalculatorTemplate

class DefaultBillCaculator(BillCalculatorTemplate):

    def get_vat_rate(self):
        vat = VAT.query.first()
        return Decimal(str(vat.vat)) if vat else Decimal("0")

    def get_discount_rate(self, subtotal):
        discount = Discount.query.first()
        if discount and subtotal > Decimal("500000"):
            return Decimal(str(discount.discount))
        return Decimal("0")
