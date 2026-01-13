from pydantic import BaseModel
import uuid

class Customer(BaseModel):
    id: uuid.UUID
    name: str
    email: str
    phone: str
    address: str
