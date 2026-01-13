import uuid
from typing import Optional
from decimal import Decimal
from src.employee.domain import Employee
from src.employee.repository import EmployeeRepository

_repository = EmployeeRepository()


def create_employee(
    name: str,
    email: str,
    phone: str,
    department: str,
    position: str,
    salary: Decimal
) -> Employee:
    if _repository.exists_by_email(email):
        raise ValueError(f"Employee with email '{email}' already exists")
    
    employee = Employee(
        id=uuid.uuid4(),
        name=name,
        email=email,
        phone=phone,
        department=department,
        position=position,
        salary=salary
    )
    return _repository.add(employee)


def get_employee(employee_id: uuid.UUID) -> Employee:
    employee = _repository.get(employee_id)
    if employee is None:
        raise ValueError(f"Employee with id '{employee_id}' not found")
    return employee


def get_all_employees() -> list[Employee]:
    return _repository.get_all()


def update_employee(
    employee_id: uuid.UUID,
    name: Optional[str] = None,
    email: Optional[str] = None,
    phone: Optional[str] = None,
    department: Optional[str] = None,
    position: Optional[str] = None,
    salary: Optional[Decimal] = None
) -> Employee:
    employee = _repository.get(employee_id)
    if employee is None:
        raise ValueError(f"Employee with id '{employee_id}' not found")
    
    if email and email != employee.email:
        if _repository.exists_by_email(email, exclude_id=employee_id):
            raise ValueError(f"Employee with email '{email}' already exists")
    
    updated = Employee(
        id=employee.id,
        name=name if name is not None else employee.name,
        email=email if email is not None else employee.email,
        phone=phone if phone is not None else employee.phone,
        department=department if department is not None else employee.department,
        position=position if position is not None else employee.position,
        salary=salary if salary is not None else employee.salary
    )
    return _repository.update(updated)


def delete_employee(employee_id: uuid.UUID) -> None:
    if not _repository.delete(employee_id):
        raise ValueError(f"Employee with id '{employee_id}' not found")
