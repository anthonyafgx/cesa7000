import uuid
import pytest
from src.customer.domain import Customer
from src.customer.repository import CustomerRepository


@pytest.fixture
def repository():
    """Create a fresh repository instance for each test."""
    return CustomerRepository()


@pytest.fixture
def sample_customer():
    """Create a sample customer for testing."""
    return Customer(
        id=uuid.uuid4(),
        name="John Doe",
        email="john@example.com",
        phone="123-456-7890",
        address="123 Main St"
    )


class TestCustomerRepository:
    """Unit tests for CustomerRepository."""

    def test_add_customer(self, repository, sample_customer):
        """Verify customer is stored correctly."""
        result = repository.add(sample_customer)
        
        assert result == sample_customer
        assert repository.get(sample_customer.id) == sample_customer

    def test_get_customer(self, repository, sample_customer):
        """Retrieve existing customer by ID."""
        repository.add(sample_customer)
        
        result = repository.get(sample_customer.id)
        
        assert result == sample_customer
        assert result.name == "John Doe"
        assert result.email == "john@example.com"

    def test_get_customer_not_found(self, repository):
        """Returns None for missing ID."""
        non_existent_id = uuid.uuid4()
        
        result = repository.get(non_existent_id)
        
        assert result is None

    def test_get_all_customers(self, repository):
        """Returns all stored customers."""
        customer1 = Customer(
            id=uuid.uuid4(),
            name="John Doe",
            email="john@example.com",
            phone="123-456-7890",
            address="123 Main St"
        )
        customer2 = Customer(
            id=uuid.uuid4(),
            name="Jane Doe",
            email="jane@example.com",
            phone="098-765-4321",
            address="456 Oak Ave"
        )
        repository.add(customer1)
        repository.add(customer2)
        
        result = repository.get_all()
        
        assert len(result) == 2
        assert customer1 in result
        assert customer2 in result

    def test_get_all_customers_empty(self, repository):
        """Returns empty list when no customers exist."""
        result = repository.get_all()
        
        assert result == []

    def test_update_customer(self, repository, sample_customer):
        """Update existing customer data."""
        repository.add(sample_customer)
        updated_customer = Customer(
            id=sample_customer.id,
            name="John Updated",
            email="john.updated@example.com",
            phone="111-222-3333",
            address="789 New St"
        )
        
        result = repository.update(updated_customer)
        
        assert result == updated_customer
        stored = repository.get(sample_customer.id)
        assert stored.name == "John Updated"
        assert stored.email == "john.updated@example.com"

    def test_delete_customer(self, repository, sample_customer):
        """Successfully delete existing customer."""
        repository.add(sample_customer)
        
        result = repository.delete(sample_customer.id)
        
        assert result is True
        assert repository.get(sample_customer.id) is None

    def test_delete_customer_not_found(self, repository):
        """Returns False for missing ID."""
        non_existent_id = uuid.uuid4()
        
        result = repository.delete(non_existent_id)
        
        assert result is False

    def test_exists_by_email(self, repository, sample_customer):
        """Check email uniqueness logic."""
        repository.add(sample_customer)
        
        assert repository.exists_by_email("john@example.com") is True
        assert repository.exists_by_email("other@example.com") is False

    def test_exists_by_email_with_exclude(self, repository, sample_customer):
        """Exclude specific ID from email check."""
        repository.add(sample_customer)
        
        # Same email but excluded ID should return False
        result = repository.exists_by_email(
            "john@example.com", 
            exclude_id=sample_customer.id
        )
        assert result is False
        
        # Same email with different excluded ID should return True
        other_id = uuid.uuid4()
        result = repository.exists_by_email(
            "john@example.com",
            exclude_id=other_id
        )
        assert result is True
