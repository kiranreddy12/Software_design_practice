from abc import ABC, abstractmethod
from typing import List, Dict, Any
import json
import xml.etree.ElementTree as ET
from dataclasses import dataclass


# ====================== TARGET (Domain Object) ======================
@dataclass
class Contact:
    """Final uniform representation (what the client expects)"""

    full_name: str
    email: str
    phone_number: str
    is_friend: bool

    def __str__(self):
        return f"{self.full_name} | {self.email} | {self.phone_number} | Friend: {self.is_friend}"


# ====================== ADAPTER INTERFACE ======================
class IContactsAdapter(ABC):
    """Abstract Adapter Interface"""

    @abstractmethod
    def getContacts(self) -> List[Contact]:
        pass


# ====================== ADAPTEES (Legacy / Incompatible Classes) ======================
class XmlContactsReader:
    """Adaptee - Legacy XML Reader"""

    def __init__(self):
        self._xml_data = """
        <contacts>
            <contact>
                <fullName>Alice Johnson</fullName>
                <email>alice@email.com</email>
                <phone>9876543210</phone>
                <isFriend>true</isFriend>
            </contact>
            <contact>
                <fullName>Bob Smith</fullName>
                <email>bob@email.com</email>
                <phone>8765432109</phone>
                <isFriend>false</isFriend>
            </contact>
        </contacts>
        """

    def getContactsXml(self) -> str:
        """Returns raw XML string"""
        return self._xml_data


class JSONContactsReader:
    """Adaptee - Legacy JSON Reader"""

    def __init__(self):
        self._json_data = [
            {
                "fullName": "Charlie Brown",
                "email": "charlie@email.com",
                "phoneNumber": "7654321098",
                "friend": True,
            },
            {
                "fullName": "Diana Prince",
                "email": "diana@email.com",
                "phoneNumber": "6543210987",
                "friend": False,
            },
        ]

    def getContactsJSON(self) -> str:
        """Returns raw JSON string"""
        return json.dumps(self._json_data)


# ====================== CONCRETE ADAPTERS ======================
class XmlContactsAdapter(IContactsAdapter):
    """Concrete Adapter for XML - Uses Composition (Filled Diamond)"""

    def __init__(self):
        self._reader: XmlContactsReader = XmlContactsReader()  # Composition

    def getContacts(self) -> List[Contact]:
        xml_str = self._reader.getContactsXml()
        root = ET.fromstring(xml_str)

        contacts = []
        for contact_elem in root.findall("contact"):
            contact = Contact(
                full_name=contact_elem.find("fullName").text,
                email=contact_elem.find("email").text,
                phone_number=contact_elem.find("phone").text,
                is_friend=contact_elem.find("isFriend").text.lower() == "true",
            )
            contacts.append(contact)

        return contacts


class JsonContactsAdapter(IContactsAdapter):
    """Concrete Adapter for JSON - Uses Composition"""

    def __init__(self):
        self._reader: JSONContactsReader = JSONContactsReader()  # Composition

    def getContacts(self) -> List[Contact]:
        json_str = self._reader.getContactsJSON()
        data = json.loads(json_str)

        contacts = []
        for item in data:
            contact = Contact(
                full_name=item["fullName"],
                email=item["email"],
                phone_number=item.get("phoneNumber", item.get("phone", "")),
                is_friend=item.get("friend", False),
            )
            contacts.append(contact)

        return contacts


# ====================== CLIENT CODE ======================
class ContactService:
    """Client code that works only with IContactsAdapter"""

    def __init__(self, adapter: IContactsAdapter):
        self._adapter = adapter

    def show_all_contacts(self):
        print("📇 All Contacts:\n")
        contacts = self._adapter.getContacts()
        for i, contact in enumerate(contacts, 1):
            print(f"{i}. {contact}")
        print("-" * 60)


# ====================== MAIN ======================
if __name__ == "__main__":
    print("=== Adapter Pattern Demo ===\n")

    # Using XML Adapter
    print("1. Using XML Contacts Adapter:")
    xml_adapter = XmlContactsAdapter()
    service1 = ContactService(xml_adapter)
    service1.show_all_contacts()

    # Using JSON Adapter
    print("\n2. Using JSON Contacts Adapter:")
    json_adapter = JsonContactsAdapter()
    service2 = ContactService(json_adapter)
    service2.show_all_contacts()

    # Demonstrating Composition (Filled Diamond)
    print("\n=== Demonstrating Composition (Filled Diamond) ===")
    adapter = XmlContactsAdapter()
    print(f"Adapter created with reader: {type(adapter._reader).__name__}")

    # If adapter is deleted, its reader should also be garbage collected (composition)
    del adapter
    print("Adapter deleted → Its internal XmlContactsReader should also be destroyed")
