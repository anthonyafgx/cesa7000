import uuid
from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from src.customer.service import (
    create_customer,
    get_customer,
    get_all_customers,
    update_customer,
    delete_customer,
)


# Request/Response Models
class CreateCustomerRequest(BaseModel):
    name: str
    email: EmailStr
    phone: str
    address: str


class UpdateCustomerRequest(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None


class CustomerResponse(BaseModel):
    id: uuid.UUID
    name: str
    email: EmailStr
    phone: str
    address: str


# Router
router = APIRouter(prefix="/customers", tags=["customers"])


@router.post("", response_model=CustomerResponse, status_code=201)
def create_customer_endpoint(request: CreateCustomerRequest):
    try:
        customer = create_customer(
            name=request.name,
            email=request.email,
            phone=request.phone,
            address=request.address
        )
        return customer
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer_endpoint(customer_id: uuid.UUID):
    try:
        return get_customer(customer_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("", response_model=list[CustomerResponse])
def list_customers_endpoint():
    return get_all_customers()


@router.put("/{customer_id}", response_model=CustomerResponse)
def update_customer_endpoint(customer_id: uuid.UUID, request: UpdateCustomerRequest):
    try:
        return update_customer(
            customer_id=customer_id,
            name=request.name,
            email=request.email,
            phone=request.phone,
            address=request.address
        )
    except ValueError as e:
        if "not found" in str(e):
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{customer_id}", status_code=204)
def delete_customer_endpoint(customer_id: uuid.UUID):
    try:
        delete_customer(customer_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
