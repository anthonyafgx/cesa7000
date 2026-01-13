import uuid
from typing import Optional
from src.customer.domain import Customer


class CustomerRepository:
    """In-memory repository for Customer entities."""

    def __init__(self):
        self._storage: dict[uuid.UUID, Customer] = {}

    def add(self, customer: Customer) -> Customer:
        self._storage[customer.id] = customer
        return customer

    def get(self, customer_id: uuid.UUID) -> Optional[Customer]:
        return self._storage.get(customer_id)

    def get_all(self) -> list[Customer]:
        return list(self._storage.values())

    def update(self, customer: Customer) -> Customer:
        self._storage[customer.id] = customer
        return customer

    def delete(self, customer_id: uuid.UUID) -> bool:
        if customer_id in self._storage:
            del self._storage[customer_id]
            return True
        return False

    def exists_by_email(self, email: str, exclude_id: Optional[uuid.UUID] = None) -> bool:
        for customer in self._storage.values():
            if customer.email == email and customer.id != exclude_id:
                return True
        return False
