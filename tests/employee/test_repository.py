import uuid
from decimal import Decimal
import pytest
from src.employee.domain import Employee
from src.employee.repository import EmployeeRepository


@pytest.fixture
def repository():
    """Create a fresh repository instance for each test."""
    return EmployeeRepository()


@pytest.fixture
def sample_employee():
    """Create a sample employee for testing."""
    return Employee(
        id=uuid.uuid4(),
        name="John Doe",
        email="john@example.com",
        phone="123-456-7890",
        department="Engineering",
        position="Software Engineer",
        salary=Decimal("75000.00")
    )


class TestEmployeeRepository:
    """Unit tests for EmployeeRepository."""

    def test_add_employee(self, repository, sample_employee):
        """Verify employee is stored correctly."""
        result = repository.add(sample_employee)
        
        assert result == sample_employee
        assert repository.get(sample_employee.id) == sample_employee

    def test_get_employee(self, repository, sample_employee):
        """Retrieve existing employee by ID."""
        repository.add(sample_employee)
        
        result = repository.get(sample_employee.id)
        
        assert result == sample_employee
        assert result.name == "John Doe"
        assert result.email == "john@example.com"
        assert result.department == "Engineering"
        assert result.position == "Software Engineer"
        assert result.salary == Decimal("75000.00")

    def test_get_employee_not_found(self, repository):
        """Returns None for missing ID."""
        non_existent_id = uuid.uuid4()
        
        result = repository.get(non_existent_id)
        
        assert result is None

    def test_get_all_employees(self, repository):
        """Returns all stored employees."""
        employee1 = Employee(
            id=uuid.uuid4(),
            name="John Doe",
            email="john@example.com",
            phone="123-456-7890",
            department="Engineering",
            position="Software Engineer",
            salary=Decimal("75000.00")
        )
        employee2 = Employee(
            id=uuid.uuid4(),
            name="Jane Doe",
            email="jane@example.com",
            phone="098-765-4321",
            department="Marketing",
            position="Marketing Manager",
            salary=Decimal("85000.00")
        )
        repository.add(employee1)
        repository.add(employee2)
        
        result = repository.get_all()
        
        assert len(result) == 2
        assert employee1 in result
        assert employee2 in result

    def test_get_all_employees_empty(self, repository):
        """Returns empty list when no employees exist."""
        result = repository.get_all()
        
        assert result == []

    def test_update_employee(self, repository, sample_employee):
        """Update existing employee data."""
        repository.add(sample_employee)
        updated_employee = Employee(
            id=sample_employee.id,
            name="John Updated",
            email="john.updated@example.com",
            phone="111-222-3333",
            department="Sales",
            position="Sales Lead",
            salary=Decimal("90000.00")
        )
        
        result = repository.update(updated_employee)
        
        assert result == updated_employee
        stored = repository.get(sample_employee.id)
        assert stored.name == "John Updated"
        assert stored.email == "john.updated@example.com"
        assert stored.department == "Sales"
        assert stored.salary == Decimal("90000.00")

    def test_delete_employee(self, repository, sample_employee):
        """Successfully delete existing employee."""
        repository.add(sample_employee)
        
        result = repository.delete(sample_employee.id)
        
        assert result is True
        assert repository.get(sample_employee.id) is None

    def test_delete_employee_not_found(self, repository):
        """Returns False for missing ID."""
        non_existent_id = uuid.uuid4()
        
        result = repository.delete(non_existent_id)
        
        assert result is False

    def test_exists_by_email(self, repository, sample_employee):
        """Check email uniqueness logic."""
        repository.add(sample_employee)
        
        assert repository.exists_by_email("john@example.com") is True
        assert repository.exists_by_email("other@example.com") is False

    def test_exists_by_email_with_exclude(self, repository, sample_employee):
        """Exclude specific ID from email check."""
        repository.add(sample_employee)
        
        # Same email but excluded ID should return False
        result = repository.exists_by_email(
            "john@example.com", 
            exclude_id=sample_employee.id
        )
        assert result is False
        
        # Same email with different excluded ID should return True
        other_id = uuid.uuid4()
        result = repository.exists_by_email(
            "john@example.com",
            exclude_id=other_id
        )
        assert result is True
