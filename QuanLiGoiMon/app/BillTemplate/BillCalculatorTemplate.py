from decimal import Decimal

class BillCalculatorTemplate:

    def calculate(self, subtotal: Decimal):
        discount_rate = self.get_discount_rate(subtotal)
        vat_rate = self.get_vat_rate()
        discount_amount = subtotal * discount_rate
        vat_amount = (subtotal - discount_amount) * vat_rate
        total = subtotal + vat_amount - discount_amount

        return {
            "vat_rate": vat_rate,
            "discount_rate": discount_rate,
            "vat_amount": vat_amount,
            "discount_amount": discount_amount,
            "total": total
        }

    def get_vat_rate(self) -> Decimal:
        raise NotImplementedError

    def get_discount_rate(self, subtotal: Decimal) -> Decimal:
        return Decimal("0")
