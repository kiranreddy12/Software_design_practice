from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Optional, Set
from enum import Enum
import uuid


# ====================== ENUMS ======================
class OrderStatus(Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    PREPARING = "PREPARING"
    DISPATCHED = "DISPATCHED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


# ====================== DOMAIN MODELS ======================
@dataclass
class MenuItem:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    price: float
    is_available: bool = True

    def __str__(self):
        return f"{self.name} - ₹{self.price:.2f}"


@dataclass
class Order:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    restaurant_id: int
    restaurant_name: str
    items: Dict[MenuItem, int] = field(default_factory=dict)  # Item -> Quantity
    total_price: float = 0.0
    status: OrderStatus = OrderStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    customer_name: str = ""

    def calculate_total(self):
        self.total_price = sum(item.price * qty for item, qty in self.items.items())
        return self.total_price


@dataclass
class Restaurant:
    id: int
    name: str
    address: str
    processing_capacity: int  # Max orders it can handle simultaneously
    menu: Dict[str, MenuItem] = field(default_factory=dict)  # item_name -> MenuItem
    orders_completed: int = 0

    def add_menu_item(self, item: MenuItem):
        self.menu[item.name] = item

    def get_menu(self) -> List[MenuItem]:
        return list(self.menu.values())

    def has_capacity(self) -> bool:
        return self.orders_completed < self.processing_capacity


# ====================== STRATEGY PATTERN ======================
class RestaurantStrategy(ABC):
    @abstractmethod
    def find_restaurant(
        self, restaurants: List[Restaurant], items: List[str]
    ) -> Optional[Restaurant]:
        pass


class ProcessingCapacityRestaurantStrategy(RestaurantStrategy):
    """Strategy: Choose restaurant with highest remaining capacity"""

    def find_restaurant(
        self, restaurants: List[Restaurant], items: List[str]
    ) -> Optional[Restaurant]:
        available_restaurants = [r for r in restaurants if r.has_capacity()]
        if not available_restaurants:
            return None
        # Return restaurant with maximum remaining capacity
        return max(
            available_restaurants,
            key=lambda r: r.processing_capacity - r.orders_completed,
        )


# ====================== SERVICES ======================
class RestaurantService:
    def __init__(self):
        self.restaurants: Dict[int, Restaurant] = {}
        self.strategy: RestaurantStrategy = ProcessingCapacityRestaurantStrategy()

    def add_restaurant(self, restaurant: Restaurant):
        self.restaurants[restaurant.id] = restaurant

    def update_processing_capacity(self, restaurant_id: int, new_capacity: int) -> bool:
        if restaurant_id in self.restaurants:
            self.restaurants[restaurant_id].processing_capacity = new_capacity
            return True
        return False

    def find_best_restaurant(self, items: List[str]) -> Optional[Restaurant]:
        return self.strategy.find_restaurant(list(self.restaurants.values()), items)

    def get_all_restaurants(self) -> List[Restaurant]:
        return list(self.restaurants.values())


class OrderService:
    def __init__(self, restaurant_service: RestaurantService):
        self.restaurant_service = restaurant_service
        self.dispatched_orders: List[Order] = []
        self.all_orders: List[Order] = []

    def create_and_place_order(
        self, customer_name: str, restaurant_name: str, item_quantities: Dict[str, int]
    ) -> Optional[Order]:

        # Find restaurant by name (you can improve this)
        restaurant = next(
            (
                r
                for r in self.restaurant_service.get_all_restaurants()
                if r.name.lower() == restaurant_name.lower()
            ),
            None,
        )

        if not restaurant or not restaurant.has_capacity():
            print(
                f"❌ Restaurant '{restaurant_name}' not available or at full capacity."
            )
            return None

        # Create order
        order = Order(
            restaurant_id=restaurant.id,
            restaurant_name=restaurant.name,
            customer_name=customer_name,
        )

        # Add items
        for item_name, qty in item_quantities.items():
            if item_name in restaurant.menu:
                menu_item = restaurant.menu[item_name]
                order.items[menu_item] = qty
            else:
                print(f"Warning: Item '{item_name}' not found in menu.")

        order.calculate_total()

        # Update restaurant stats
        restaurant.orders_completed += 1
        order.status = OrderStatus.ACCEPTED

        self.all_orders.append(order)
        self.dispatched_orders.append(order)

        print(
            f"✅ Order {order.id} placed successfully at {restaurant.name} | Total: ₹{order.total_price:.2f}"
        )
        return order

    def show_dispatched_orders(self):
        print("\n📋 Dispatched Orders:")
        for order in self.dispatched_orders:
            print(
                f"Order {order.id} | {order.restaurant_name} | ₹{order.total_price:.2f} | {order.status.value}"
            )


# ====================== COMMAND PROCESSOR ======================
class CommandProcessor:
    def __init__(self, order_service: OrderService):
        self.order_service = order_service

    def process_input_command(self, command: List[str]):
        """Simple command processor - can be extended"""
        if not command:
            return

        cmd = command[0].lower()

        if cmd == "place_order" and len(command) > 3:
            customer = command[1]
            restaurant = command[2]
            # Simple parsing: item1:qty1,item2:qty2
            items_str = command[3]
            item_dict = {}
            for item in items_str.split(","):
                if ":" in item:
                    name, qty = item.split(":")
                    item_dict[name.strip()] = int(qty.strip())

            self.order_service.create_and_place_order(customer, restaurant, item_dict)

        elif cmd == "show_orders":
            self.order_service.show_dispatched_orders()


# ====================== USAGE EXAMPLE ======================
if __name__ == "__main__":
    # Setup
    restaurant_service = RestaurantService()
    order_service = OrderService(restaurant_service)
    command_processor = CommandProcessor(order_service)

    # Create Restaurants
    r1 = Restaurant(1, "Punjabi Tadka", "Sector 12", processing_capacity=5)
    r2 = Restaurant(2, "South Indian Delight", "Sector 18", processing_capacity=8)

    # Add Menu Items
    r1.add_menu_item(MenuItem(name="Butter Chicken", price=320.0))
    r1.add_menu_item(MenuItem(name="Paneer Tikka", price=280.0))
    r1.add_menu_item(MenuItem(name="Naan", price=50.0))

    r2.add_menu_item(MenuItem(name="Masala Dosa", price=180.0))
    r2.add_menu_item(MenuItem(name="Idli Sambar", price=140.0))

    restaurant_service.add_restaurant(r1)
    restaurant_service.add_restaurant(r2)

    # Place Orders using Command Pattern
    print("=== Restaurant Management System ===\n")

    command_processor.process_input_command(
        ["place_order", "Sai Kiran", "Punjabi Tadka", "Butter Chicken:2,Naan:3"]
    )

    command_processor.process_input_command(
        [
            "place_order",
            "Rahul Sharma",
            "South Indian Delight",
            "Masala Dosa:1,Idli Sambar:2",
        ]
    )

    order_service.show_dispatched_orders()
