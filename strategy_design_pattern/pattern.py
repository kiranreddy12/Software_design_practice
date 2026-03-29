from abc import ABC, abstractmethod
from typing import Dict


# ====================== STRATEGY INTERFACE ======================
class PaymentStrategy(ABC):
    """Abstract Strategy - Common interface for all payment methods"""

    @abstractmethod
    def pay(self, amount: float, details: Dict = None) -> str:
        pass


# ====================== CONCRETE STRATEGIES ======================
class CreditCardStrategy(PaymentStrategy):
    def pay(self, amount: float, details: Dict = None) -> str:
        card_number = details.get("card_number", "XXXX-XXXX-XXXX-XXXX")
        return f"✅ Paid ₹{amount:.2f} using Credit Card ({card_number[-4:]})"


class PayPalStrategy(PaymentStrategy):
    def pay(self, amount: float, details: Dict = None) -> str:
        email = details.get("email", "user@example.com")
        return f"✅ Paid ₹{amount:.2f} using PayPal ({email})"


class UPI_Strategy(PaymentStrategy):
    def pay(self, amount: float, details: Dict = None) -> str:
        upi_id = details.get("upi_id", "user@upi")
        return f"✅ Paid ₹{amount:.2f} using UPI ({upi_id})"


class CashOnDeliveryStrategy(PaymentStrategy):
    def pay(self, amount: float, details: Dict = None) -> str:
        return f"✅ Order placed for ₹{amount:.2f}. Pay in Cash on Delivery."


# ====================== CONTEXT ======================
class ShoppingCart:
    """Context - Uses the strategy"""

    def __init__(self, payment_strategy: PaymentStrategy = CashOnDeliveryStrategy()):
        self._strategy = payment_strategy
        self.items = []
        self.total = 0.0

    def add_item(self, name: str, price: float):
        self.items.append((name, price))
        self.total += price

    def set_payment_strategy(self, strategy: PaymentStrategy):
        """Change strategy at runtime"""
        self._strategy = strategy

    def checkout(self, payment_details: Dict = None) -> str:
        if not self.items:
            return "Cart is empty!"

        print(f"Processing payment of ₹{self.total:.2f}...")
        result = self._strategy.pay(self.total, payment_details)
        print(result)
        return "Checkout completed successfully!"


# ====================== CLIENT CODE ======================
if __name__ == "__main__":
    cart = ShoppingCart(CreditCardStrategy())  # Default strategy

    cart.add_item("Laptop", 45000)
    cart.add_item("Mouse", 800)

    print("=== Using Credit Card ===")
    cart.checkout({"card_number": "1234-5678-9012-3456"})

    print("\n=== Switching to PayPal at runtime ===")
    cart.set_payment_strategy(PayPalStrategy())
    cart.checkout({"email": "sai.kiran@example.com"})

    print("\n=== Switching to UPI ===")
    cart.set_payment_strategy(UPI_Strategy())
    cart.checkout({"upi_id": "sai@oksbi"})

    print("\n=== Cash on Delivery ===")
    cart.set_payment_strategy(CashOnDeliveryStrategy())
    cart.checkout()
