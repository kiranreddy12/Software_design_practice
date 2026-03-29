from pydantic import BaseModel, Field, ConfigDict
from typing import List, Dict, Optional
from datetime import datetime


# ====================== EMBEDDED ITEM MODEL ======================
class MenuItem(BaseModel):
    """Embedded object for each menu item"""

    name: str
    price: float = Field(ge=0, description="Price of the item")
    max_capacity: int = Field(ge=0, description="Maximum available quantity")
    description: Optional[str] = None
    is_available: bool = True

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Margherita Pizza",
                "price": 249.0,
                "max_capacity": 20,
                "description": "Classic pizza with fresh basil",
                "is_available": True,
            }
        }
    )

    def reduce_capacity(self, quantity: int) -> bool:
        """Reduce capacity when item is ordered"""
        if self.max_capacity >= quantity:
            self.max_capacity -= quantity
            if self.max_capacity == 0:
                self.is_available = False
            return True
        return False


# ====================== MENU CLASS ======================
class Menu(BaseModel):
    """Main Menu class containing multiple items"""

    menu_id: str = Field(
        default_factory=lambda: f"menu_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    )
    name: str = "Main Menu"
    items: List[MenuItem] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)
    last_updated: datetime = Field(default_factory=datetime.now)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Restaurant Menu",
                "items": [
                    {"name": "Margherita Pizza", "price": 249.0, "max_capacity": 20},
                    {"name": "Butter Naan", "price": 45.0, "max_capacity": 50},
                ],
            }
        }
    )

    def add_item(
        self,
        name: str,
        price: float,
        max_capacity: int,
        description: Optional[str] = None,
    ):
        """Add a new item to the menu"""
        item = MenuItem(
            name=name, price=price, max_capacity=max_capacity, description=description
        )
        self.items.append(item)
        self.last_updated = datetime.now()
        print(f"✅ Added item: {name} (₹{price}, Capacity: {max_capacity})")

    def get_item(self, item_name: str) -> Optional[MenuItem]:
        """Get item by name"""
        for item in self.items:
            if item.name.lower() == item_name.lower():
                return item
        return None

    def show_menu(self):
        """Display the menu nicely"""
        print(f"\n📋 {self.name.upper()}".center(60))
        print("=" * 60)
        print(f"{'Item Name':<25} {'Price':<10} {'Max Capacity':<15} {'Status'}")
        print("-" * 60)

        for item in self.items:
            status = "✅ Available" if item.is_available else "❌ Out of Stock"
            print(
                f"{item.name:<25} ₹{item.price:<8.2f} {item.max_capacity:<15} {status}"
            )
        print("=" * 60)

    def update_item_capacity(self, item_name: str, new_capacity: int):
        """Update max capacity of an item"""
        item = self.get_item(item_name)
        if item:
            item.max_capacity = new_capacity
            item.is_available = new_capacity > 0
            self.last_updated = datetime.now()
            print(f"Updated capacity for {item_name} to {new_capacity}")
        else:
            print(f"Item '{item_name}' not found!")


# ====================== USAGE EXAMPLE ======================
if __name__ == "__main__":
    # Create menu
    menu = Menu(name="Indian Spice Restaurant")

    # Add items using embedded MenuItem logic
    menu.add_item("Margherita Pizza", 249.0, 15, "Classic cheese pizza")
    menu.add_item("Butter Naan", 45.0, 50)
    menu.add_item("Paneer Butter Masala", 320.0, 12, "Cottage cheese in rich gravy")
    menu.add_item("Veg Biryani", 280.0, 8)
    menu.add_item("Mango Lassi", 90.0, 30)

    # Show menu
    menu.show_menu()

    # Example: Reduce capacity when order is placed
    pizza = menu.get_item("Margherita Pizza")
    if pizza:
        pizza.reduce_capacity(3)  # Ordered 3 pizzas
        print(f"Remaining capacity for Margherita Pizza: {pizza.max_capacity}")

    # Update capacity
    menu.update_item_capacity("Veg Biryani", 5)

    # Show updated menu
    menu.show_menu()
