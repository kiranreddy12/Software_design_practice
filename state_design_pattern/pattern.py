from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Optional, Dict, List


# ====================== CONTEXT ======================
class Order:
    """Context - The main Order object"""

    def __init__(self, order_id: str, customer_email: str):
        self.order_id = order_id
        self.customer_email = customer_email
        self.items: List[Dict] = []
        self.total_amount: float = 0.0
        self.created_at = datetime.now()
        self._state: OrderState = NewState(self)  # Initial state
        self.refund_processed = False
        self.tracking_number: Optional[str] = None
        self.delivery_date: Optional[datetime] = None

    def set_state(self, state: "OrderState"):
        print(
            f"🔄 Order {self.order_id}: Transitioning from {self._state.__class__.__name__} → {state.__class__.__name__}"
        )
        self._state = state

    # Delegate all actions to current state
    def add_item(self, item_name: str, price: float, qty: int = 1):
        self._state.add_item(item_name, price, qty)

    def pay(self, payment_method: str):
        self._state.pay(payment_method)

    def ship(self, tracking_number: str):
        self._state.ship(tracking_number)

    def deliver(self):
        self._state.deliver()

    def cancel(self):
        self._state.cancel()

    def return_order(self, reason: str):
        self._state.return_order(reason)

    def show_status(self):
        print(f"\n📋 Order {self.order_id} Status")
        print(f"   Current State : {self._state.__class__.__name__}")
        print(f"   Total Amount  : ₹{self.total_amount:.2f}")
        print(f"   Items         : {len(self.items)}")
        if self.tracking_number:
            print(f"   Tracking      : {self.tracking_number}")
        print("-" * 60)


# ====================== STATE INTERFACE ======================
class OrderState(ABC):
    def __init__(self, order: Order):
        self.order = order

    @abstractmethod
    def add_item(self, item_name: str, price: float, qty: int):
        pass

    @abstractmethod
    def pay(self, payment_method: str):
        pass

    @abstractmethod
    def ship(self, tracking_number: str):
        pass

    @abstractmethod
    def deliver(self):
        pass

    @abstractmethod
    def cancel(self):
        pass

    @abstractmethod
    def return_order(self, reason: str):
        pass


# ====================== CONCRETE STATES ======================


class NewState(OrderState):
    """Order is newly created - can add items and pay"""

    def add_item(self, item_name: str, price: float, qty: int):
        self.order.items.append({"name": item_name, "price": price, "qty": qty})
        self.order.total_amount += price * qty
        print(f"✅ Added {qty}x {item_name} (₹{price})")

    def pay(self, payment_method: str):
        print(
            f"💰 Payment successful via {payment_method} (₹{self.order.total_amount})"
        )
        self.order.set_state(PaidState(self.order))

    def ship(self, tracking_number: str):
        print("❌ Cannot ship - Order not yet paid!")

    def deliver(self):
        print("❌ Cannot deliver - Order not shipped!")

    def cancel(self):
        print("✅ Order cancelled successfully.")
        self.order.set_state(CancelledState(self.order))

    def return_order(self, reason: str):
        print("❌ Cannot return - Order not delivered yet!")


class PaidState(OrderState):
    """Order is paid - can be shipped or cancelled"""

    def add_item(self, item_name: str, price: float, qty: int):
        print("❌ Cannot add items after payment!")

    def pay(self, payment_method: str):
        print("❌ Payment already done!")

    def ship(self, tracking_number: str):
        self.order.tracking_number = tracking_number
        print(f"🚚 Order shipped! Tracking: {tracking_number}")
        self.order.set_state(ShippedState(self.order))

    def deliver(self):
        print("❌ Cannot deliver - Order not shipped yet!")

    def cancel(self):
        print("🔄 Cancelling paid order... Processing refund...")
        self.order.refund_processed = True
        print("✅ Refund initiated to original payment method.")
        self.order.set_state(CancelledState(self.order))

    def return_order(self, reason: str):
        print("❌ Cannot return - Order not delivered yet!")


class ShippedState(OrderState):
    """Order is shipped - can be delivered or returned"""

    def add_item(self, item_name: str, price: float, qty: int):
        print("❌ Cannot modify shipped order!")

    def pay(self, payment_method: str):
        print("❌ Already paid!")

    def ship(self, tracking_number: str):
        print("❌ Already shipped!")

    def deliver(self):
        print("📦 Order delivered successfully!")
        self.order.delivery_date = datetime.now()
        self.order.set_state(DeliveredState(self.order))

    def cancel(self):
        print("❌ Cannot cancel - Order already shipped!")

    def return_order(self, reason: str):
        print("❌ Cannot return - Order not yet delivered!")


class DeliveredState(OrderState):
    """Order is delivered - can be returned within return window"""

    def add_item(self, item_name: str, price: float, qty: int):
        print("❌ Cannot modify delivered order!")

    def pay(self, payment_method: str):
        print("❌ Already paid!")

    def ship(self, tracking_number: str):
        print("❌ Already shipped!")

    def deliver(self):
        print("❌ Already delivered!")

    def cancel(self):
        print("❌ Cannot cancel delivered order!")

    def return_order(self, reason: str):
        # Check return window (7 days)
        if datetime.now() - self.order.delivery_date < timedelta(days=7):
            print(f"🔄 Return request accepted. Reason: {reason}")
            print("✅ Refund will be processed in 3-5 business days.")
            self.order.set_state(ReturnedState(self.order))
        else:
            print("❌ Return window expired! Cannot return.")


class CancelledState(OrderState):
    """Final state - no further actions allowed"""

    def add_item(self, item_name: str, price: float, qty: int):
        print("❌ Order is cancelled!")

    def pay(self, payment_method: str):
        print("❌ Order is cancelled!")

    def ship(self, tracking_number: str):
        print("❌ Order is cancelled!")

    def deliver(self):
        print("❌ Order is cancelled!")

    def cancel(self):
        print("❌ Order is already cancelled!")

    def return_order(self, reason: str):
        print("❌ Order is cancelled - cannot return!")


class ReturnedState(OrderState):
    """Final state after successful return"""

    def add_item(self, item_name: str, price: float, qty: int):
        print("❌ Order is returned!")

    def pay(self, payment_method: str):
        print("❌ Order is returned!")

    def ship(self, tracking_number: str):
        print("❌ Order is returned!")

    def deliver(self):
        print("❌ Order is returned!")

    def cancel(self):
        print("❌ Order is already returned!")

    def return_order(self, reason: str):
        print("❌ Already returned!")


# ====================== CLIENT CODE (Usage) ======================
if __name__ == "__main__":
    print("🚀 Starting Rich State Pattern - Order Processing System\n")

    order = Order("ORD-20260329-001", "sai.kiran@example.com")

    order.add_item("Wireless Headphones", 2499.0)
    order.add_item("USB-C Cable", 499.0)

    order.show_status()

    order.pay("UPI")
    order.show_status()

    order.ship("TRK987654321")
    order.show_status()

    order.deliver()
    order.show_status()

    # Try invalid action
    order.pay("Card")  # Should fail

    # Return the order
    order.return_order("Defective product")
    order.show_status()

    print("\n=== Another Scenario: Cancel after Payment ===")
    order2 = Order("ORD-20260329-002", "test@example.com")
    order2.add_item("Smart Watch", 3999.0)
    order2.pay("Credit Card")
    order2.cancel()  # Triggers refund logic
    order2.show_status()
