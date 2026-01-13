import uuid
import pytest
from src.customer.domain import Customer
from src.customer.repository import CustomerRepository
from src.customer import service


@pytest.fixture
def fresh_repository(monkeypatch):
    """Replace the module-level repository with a fresh instance for test isolation."""
    repo = CustomerRepository()
    monkeypatch.setattr(service, "_repository", repo)
    return repo


@pytest.fixture
def existing_customer(fresh_repository):
    """Create and store a customer for tests that need existing data."""
    customer = Customer(
        id=uuid.uuid4(),
        name="John Doe",
        email="john@example.com",
        phone="123-456-7890",
        address="123 Main St"
    )
    fresh_repository.add(customer)
    return customer


class TestCreateCustomer:
    """Tests for create_customer service function."""

    def test_create_customer(self, fresh_repository):
        """Creates customer successfully."""
        result = service.create_customer(
            name="Jane Doe",
            email="jane@example.com",
            phone="098-765-4321",
            address="456 Oak Ave"
        )
        
        assert result.name == "Jane Doe"
        assert result.email == "jane@example.com"
        assert result.phone == "098-765-4321"
        assert result.address == "456 Oak Ave"
        assert result.id is not None
        # Verify stored in repository
        assert fresh_repository.get(result.id) == result

    def test_create_customer_duplicate_email(self, existing_customer, fresh_repository):
        """Raises ValueError for duplicate email."""
        with pytest.raises(ValueError) as exc_info:
            service.create_customer(
                name="Another Person",
                email="john@example.com",  # Same email as existing_customer
                phone="111-222-3333",
                address="789 New St"
            )
        
        assert "already exists" in str(exc_info.value)


class TestGetCustomer:
    """Tests for get_customer service function."""

    def test_get_customer(self, existing_customer):
        """Retrieves customer by ID."""
        result = service.get_customer(existing_customer.id)
        
        assert result == existing_customer
        assert result.name == "John Doe"

    def test_get_customer_not_found(self, fresh_repository):
        """Raises ValueError for missing customer."""
        non_existent_id = uuid.uuid4()
        
        with pytest.raises(ValueError) as exc_info:
            service.get_customer(non_existent_id)
        
        assert "not found" in str(exc_info.value)


class TestGetAllCustomers:
    """Tests for get_all_customers service function."""

    def test_get_all_customers(self, fresh_repository):
        """Returns all customers."""
        customer1 = service.create_customer(
            name="John Doe",
            email="john@example.com",
            phone="123-456-7890",
            address="123 Main St"
        )
        customer2 = service.create_customer(
            name="Jane Doe",
            email="jane@example.com",
            phone="098-765-4321",
            address="456 Oak Ave"
        )
        
        result = service.get_all_customers()
        
        assert len(result) == 2
        assert customer1 in result
        assert customer2 in result

    def test_get_all_customers_empty(self, fresh_repository):
        """Returns empty list when no customers exist."""
        result = service.get_all_customers()
        
        assert result == []


class TestUpdateCustomer:
    """Tests for update_customer service function."""

    def test_update_customer(self, existing_customer):
        """Partial update works correctly."""
        result = service.update_customer(
            customer_id=existing_customer.id,
            name="John Updated"
        )
        
        assert result.name == "John Updated"
        # Other fields should remain unchanged
        assert result.email == existing_customer.email
        assert result.phone == existing_customer.phone
        assert result.address == existing_customer.address

    def test_update_customer_all_fields(self, existing_customer):
        """Update all fields at once."""
        result = service.update_customer(
            customer_id=existing_customer.id,
            name="Completely New Name",
            email="new@example.com",
            phone="999-888-7777",
            address="999 Different Blvd"
        )
        
        assert result.name == "Completely New Name"
        assert result.email == "new@example.com"
        assert result.phone == "999-888-7777"
        assert result.address == "999 Different Blvd"

    def test_update_customer_not_found(self, fresh_repository):
        """Raises ValueError for missing customer."""
        non_existent_id = uuid.uuid4()
        
        with pytest.raises(ValueError) as exc_info:
            service.update_customer(
                customer_id=non_existent_id,
                name="New Name"
            )
        
        assert "not found" in str(exc_info.value)

    def test_update_customer_duplicate_email(self, fresh_repository):
        """Raises ValueError when changing to existing email."""
        # Create two customers
        customer1 = service.create_customer(
            name="Customer One",
            email="customer1@example.com",
            phone="111-111-1111",
            address="Address 1"
        )
        customer2 = service.create_customer(
            name="Customer Two",
            email="customer2@example.com",
            phone="222-222-2222",
            address="Address 2"
        )
        
        # Try to update customer2's email to customer1's email
        with pytest.raises(ValueError) as exc_info:
            service.update_customer(
                customer_id=customer2.id,
                email="customer1@example.com"
            )
        
        assert "already exists" in str(exc_info.value)

    def test_update_customer_same_email(self, existing_customer):
        """Updating with same email should succeed."""
        result = service.update_customer(
            customer_id=existing_customer.id,
            email=existing_customer.email,  # Same email
            name="New Name"
        )
        
        assert result.name == "New Name"
        assert result.email == existing_customer.email


class TestDeleteCustomer:
    """Tests for delete_customer service function."""

    def test_delete_customer(self, existing_customer, fresh_repository):
        """Successfully deletes customer."""
        service.delete_customer(existing_customer.id)
        
        # Verify customer is removed
        assert fresh_repository.get(existing_customer.id) is None

    def test_delete_customer_not_found(self, fresh_repository):
        """Raises ValueError for missing customer."""
        non_existent_id = uuid.uuid4()
        
        with pytest.raises(ValueError) as exc_info:
            service.delete_customer(non_existent_id)
        
        assert "not found" in str(exc_info.value)
