from pydantic import BaseModel
import uuid
from decimal import Decimal


class Employee(BaseModel):
    id: uuid.UUID
    name: str
    email: str
    phone: str
    department: str
    position: str
    salary: Decimal
