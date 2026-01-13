import uuid
from typing import Optional
from src.customer.domain import Customer
from src.customer.repository import CustomerRepository

_repository = CustomerRepository()


def create_customer(name: str, email: str, phone: str, address: str) -> Customer:
    if _repository.exists_by_email(email):
        raise ValueError(f"Customer with email '{email}' already exists")
    
    customer = Customer(
        id=uuid.uuid4(),
        name=name,
        email=email,
        phone=phone,
        address=address
    )
    return _repository.add(customer)


def get_customer(customer_id: uuid.UUID) -> Customer:
    customer = _repository.get(customer_id)
    if customer is None:
        raise ValueError(f"Customer with id '{customer_id}' not found")
    return customer


def get_all_customers() -> list[Customer]:
    return _repository.get_all()


def update_customer(
    customer_id: uuid.UUID,
    name: Optional[str] = None,
    email: Optional[str] = None,
    phone: Optional[str] = None,
    address: Optional[str] = None
) -> Customer:
    customer = _repository.get(customer_id)
    if customer is None:
        raise ValueError(f"Customer with id '{customer_id}' not found")
    
    if email and email != customer.email:
        if _repository.exists_by_email(email, exclude_id=customer_id):
            raise ValueError(f"Customer with email '{email}' already exists")
    
    updated = Customer(
        id=customer.id,
        name=name if name is not None else customer.name,
        email=email if email is not None else customer.email,
        phone=phone if phone is not None else customer.phone,
        address=address if address is not None else customer.address
    )
    return _repository.update(updated)


def delete_customer(customer_id: uuid.UUID) -> None:
    if not _repository.delete(customer_id):
        raise ValueError(f"Customer with id '{customer_id}' not found")
