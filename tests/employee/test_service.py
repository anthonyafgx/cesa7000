import uuid
from decimal import Decimal
import pytest
from src.employee.domain import Employee
from src.employee.repository import EmployeeRepository
from src.employee import service


@pytest.fixture
def fresh_repository(monkeypatch):
    """Replace the module-level repository with a fresh instance for test isolation."""
    repo = EmployeeRepository()
    monkeypatch.setattr(service, "_repository", repo)
    return repo


@pytest.fixture
def existing_employee(fresh_repository):
    """Create and store an employee for tests that need existing data."""
    employee = Employee(
        id=uuid.uuid4(),
        name="John Doe",
        email="john@example.com",
        phone="123-456-7890",
        department="Engineering",
        position="Software Engineer",
        salary=Decimal("75000.00")
    )
    fresh_repository.add(employee)
    return employee


class TestCreateEmployee:
    """Tests for create_employee service function."""

    def test_create_employee(self, fresh_repository):
        """Creates employee successfully."""
        result = service.create_employee(
            name="Jane Doe",
            email="jane@example.com",
            phone="098-765-4321",
            department="Marketing",
            position="Marketing Manager",
            salary=Decimal("85000.00")
        )
        
        assert result.name == "Jane Doe"
        assert result.email == "jane@example.com"
        assert result.phone == "098-765-4321"
        assert result.department == "Marketing"
        assert result.position == "Marketing Manager"
        assert result.salary == Decimal("85000.00")
        assert result.id is not None
        # Verify stored in repository
        assert fresh_repository.get(result.id) == result

    def test_create_employee_duplicate_email(self, existing_employee, fresh_repository):
        """Raises ValueError for duplicate email."""
        with pytest.raises(ValueError) as exc_info:
            service.create_employee(
                name="Another Person",
                email="john@example.com",  # Same email as existing_employee
                phone="111-222-3333",
                department="Sales",
                position="Sales Rep",
                salary=Decimal("60000.00")
            )
        
        assert "already exists" in str(exc_info.value)


class TestGetEmployee:
    """Tests for get_employee service function."""

    def test_get_employee(self, existing_employee):
        """Retrieves employee by ID."""
        result = service.get_employee(existing_employee.id)
        
        assert result == existing_employee
        assert result.name == "John Doe"

    def test_get_employee_not_found(self, fresh_repository):
        """Raises ValueError for missing employee."""
        non_existent_id = uuid.uuid4()
        
        with pytest.raises(ValueError) as exc_info:
            service.get_employee(non_existent_id)
        
        assert "not found" in str(exc_info.value)


class TestGetAllEmployees:
    """Tests for get_all_employees service function."""

    def test_get_all_employees(self, fresh_repository):
        """Returns all employees."""
        employee1 = service.create_employee(
            name="John Doe",
            email="john@example.com",
            phone="123-456-7890",
            department="Engineering",
            position="Software Engineer",
            salary=Decimal("75000.00")
        )
        employee2 = service.create_employee(
            name="Jane Doe",
            email="jane@example.com",
            phone="098-765-4321",
            department="Marketing",
            position="Marketing Manager",
            salary=Decimal("85000.00")
        )
        
        result = service.get_all_employees()
        
        assert len(result) == 2
        assert employee1 in result
        assert employee2 in result

    def test_get_all_employees_empty(self, fresh_repository):
        """Returns empty list when no employees exist."""
        result = service.get_all_employees()
        
        assert result == []


class TestUpdateEmployee:
    """Tests for update_employee service function."""

    def test_update_employee(self, existing_employee):
        """Partial update works correctly."""
        result = service.update_employee(
            employee_id=existing_employee.id,
            name="John Updated"
        )
        
        assert result.name == "John Updated"
        # Other fields should remain unchanged
        assert result.email == existing_employee.email
        assert result.phone == existing_employee.phone
        assert result.department == existing_employee.department
        assert result.position == existing_employee.position
        assert result.salary == existing_employee.salary

    def test_update_employee_all_fields(self, existing_employee):
        """Update all fields at once."""
        result = service.update_employee(
            employee_id=existing_employee.id,
            name="Completely New Name",
            email="new@example.com",
            phone="999-888-7777",
            department="Finance",
            position="CFO",
            salary=Decimal("150000.00")
        )
        
        assert result.name == "Completely New Name"
        assert result.email == "new@example.com"
        assert result.phone == "999-888-7777"
        assert result.department == "Finance"
        assert result.position == "CFO"
        assert result.salary == Decimal("150000.00")

    def test_update_employee_not_found(self, fresh_repository):
        """Raises ValueError for missing employee."""
        non_existent_id = uuid.uuid4()
        
        with pytest.raises(ValueError) as exc_info:
            service.update_employee(
                employee_id=non_existent_id,
                name="New Name"
            )
        
        assert "not found" in str(exc_info.value)

    def test_update_employee_duplicate_email(self, fresh_repository):
        """Raises ValueError when changing to existing email."""
        # Create two employees
        employee1 = service.create_employee(
            name="Employee One",
            email="employee1@example.com",
            phone="111-111-1111",
            department="Engineering",
            position="Engineer",
            salary=Decimal("70000.00")
        )
        employee2 = service.create_employee(
            name="Employee Two",
            email="employee2@example.com",
            phone="222-222-2222",
            department="Sales",
            position="Sales Rep",
            salary=Decimal("65000.00")
        )
        
        # Try to update employee2's email to employee1's email
        with pytest.raises(ValueError) as exc_info:
            service.update_employee(
                employee_id=employee2.id,
                email="employee1@example.com"
            )
        
        assert "already exists" in str(exc_info.value)

    def test_update_employee_same_email(self, existing_employee):
        """Updating with same email should succeed."""
        result = service.update_employee(
            employee_id=existing_employee.id,
            email=existing_employee.email,  # Same email
            name="New Name"
        )
        
        assert result.name == "New Name"
        assert result.email == existing_employee.email


class TestDeleteEmployee:
    """Tests for delete_employee service function."""

    def test_delete_employee(self, existing_employee, fresh_repository):
        """Successfully deletes employee."""
        service.delete_employee(existing_employee.id)
        
        # Verify employee is removed
        assert fresh_repository.get(existing_employee.id) is None

    def test_delete_employee_not_found(self, fresh_repository):
        """Raises ValueError for missing employee."""
        non_existent_id = uuid.uuid4()
        
        with pytest.raises(ValueError) as exc_info:
            service.delete_employee(non_existent_id)
        
        assert "not found" in str(exc_info.value)
