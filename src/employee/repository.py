import uuid
from typing import Optional
from src.employee.domain import Employee


class EmployeeRepository:
    """In-memory repository for Employee entities."""

    def __init__(self):
        self._storage: dict[uuid.UUID, Employee] = {}

    def add(self, employee: Employee) -> Employee:
        self._storage[employee.id] = employee
        return employee

    def get(self, employee_id: uuid.UUID) -> Optional[Employee]:
        return self._storage.get(employee_id)

    def get_all(self) -> list[Employee]:
        return list(self._storage.values())

    def update(self, employee: Employee) -> Employee:
        self._storage[employee.id] = employee
        return employee

    def delete(self, employee_id: uuid.UUID) -> bool:
        if employee_id in self._storage:
            del self._storage[employee_id]
            return True
        return False

    def exists_by_email(self, email: str, exclude_id: Optional[uuid.UUID] = None) -> bool:
        for employee in self._storage.values():
            if employee.email == email and employee.id != exclude_id:
                return True
        return False
