### UML Description: Strategy Pattern (Payment Processing Example)

#### Purpose
The Strategy Pattern defines a family of algorithms (different payment methods), encapsulates each one, and makes them interchangeable. The `ShoppingCart` (Context) can switch between different payment strategies at runtime without changing its own code.

#### Key UML Relationships

- **`PaymentStrategy`** (Interface)  
  → Abstract strategy that declares the common `pay()` method.

- **`CreditCardStrategy`**, **`PayPalStrategy`**, **`UPIStrategy`**, **`CashOnDeliveryStrategy`**  
  → These are **Concrete Strategies**. They implement the `PaymentStrategy` interface using **Realization** (dotted line with hollow triangle △).

- **`ShoppingCart`** (Context)  
  → Has a reference to `PaymentStrategy` using **Association** / **Aggregation** (solid line with arrow).

- **Client**  
  → Creates concrete strategy objects and injects them into the `ShoppingCart`.

#### Visual UML Summary
