### UML Description: Adapter Pattern (Contacts Example)

#### Purpose
The Adapter Pattern allows incompatible interfaces to work together. In this example, we have two legacy readers (`XmlContactsReader` and `JSONContactsReader`) that provide data in different formats. The Adapter Pattern converts their interfaces into a common `IContactsAdapter` interface that the client (`ContactService`) can use uniformly.

#### Key UML Relationships

- **`IContactsAdapter`** (Interface)  
  → Defined using **Realization** (dotted line with hollow triangle).

- **`XmlContactsAdapter`** and **`JsonContactsAdapter`**  
  → Inherit from / implement `IContactsAdapter` using **Realization** (dotted line + hollow triangle △).

- **`XmlContactsReader`** and **`JSONContactsReader`** (Adaptees)  
  → Connected to their respective adapters using **Composition** (solid line with filled diamond ◆).  
  This means the Adapter **owns** the Reader. If the adapter is destroyed, the reader is also destroyed.

- **Dependency** (`<<creates>>`)  
  → Shown from Adapter classes to `Contact` class, indicating that adapters create `Contact` objects.

#### Visual UML Summary
