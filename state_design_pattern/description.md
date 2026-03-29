### Problem Description: Order Processing System

#### Business Context

In modern e-commerce applications like Amazon, Flipkart, or any online store, an **Order** goes through multiple distinct stages during its lifecycle. These stages are commonly referred to as **Order States**.

Typical order states include:
- **New** / Pending
- **Paid** / Confirmed
- **Shipped**
- **Delivered**
- **Cancelled**
- **Returned**

Each state has **different rules** and **allowed actions**. For example:
- You can only add items when the order is in `New` state.
- You can only ship the order after it has been `Paid`.
- You cannot cancel the order once it has been `Shipped`.
- Returns are only allowed within a specific time window after `Delivered`.

#### The Problem

When implementing such a system using traditional conditional logic (`if-elif-else`), the code becomes:

- Very complex and difficult to read
- Error-prone (easy to allow invalid actions)
- Hard to maintain and extend
- Violates the **Open-Closed Principle** (adding a new state requires modifying existing code)

As the number of states and business rules grows, managing all possible transitions and behaviors in a single class leads to **spaghetti code** and increased risk of bugs.

#### Challenges

- How to handle different behavior for the same action (`pay()`, `ship()`, `cancel()`, `deliver()`, `return_order()`) based on the current state of the order?
- How to make the system easily extensible when new states or rules are introduced?
- How to ensure invalid state transitions are prevented naturally by the design?
- How to keep the `Order` class clean and focused only on data, while delegating behavior to appropriate logic?

#### Goal

We need a design solution that:
- Encapsulates state-specific behavior in separate classes
- Allows dynamic change of behavior at runtime
- Makes the code clean, maintainable, and extensible
- Clearly expresses the business rules for each order state

This is a classic scenario where the **State Design Pattern** becomes highly useful.

---

### Why This Problem Matters

Proper handling of order states is critical in e-commerce because:
- It directly impacts customer experience
- It affects inventory, payment, and logistics systems
- Wrong state transitions can cause financial loss or operational issues
- Audit and compliance requirements demand clear tracking of state changes
