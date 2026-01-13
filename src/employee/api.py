import uuid
from typing import Optional
from decimal import Decimal
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from src.employee.service import (
    create_employee,
    get_employee,
    get_all_employees,
    update_employee,
    delete_employee,
)


# Request/Response Models
class CreateEmployeeRequest(BaseModel):
    name: str
    email: EmailStr
    phone: str
    department: str
    position: str
    salary: Decimal


class UpdateEmployeeRequest(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    department: Optional[str] = None
    position: Optional[str] = None
    salary: Optional[Decimal] = None


class EmployeeResponse(BaseModel):
    id: uuid.UUID
    name: str
    email: EmailStr
    phone: str
    department: str
    position: str
    salary: Decimal


# Router
router = APIRouter(prefix="/employees", tags=["employees"])


@router.post("", response_model=EmployeeResponse, status_code=201)
def create_employee_endpoint(request: CreateEmployeeRequest):
    try:
        employee = create_employee(
            name=request.name,
            email=request.email,
            phone=request.phone,
            department=request.department,
            position=request.position,
            salary=request.salary
        )
        return employee
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{employee_id}", response_model=EmployeeResponse)
def get_employee_endpoint(employee_id: uuid.UUID):
    try:
        return get_employee(employee_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("", response_model=list[EmployeeResponse])
def list_employees_endpoint():
    return get_all_employees()


@router.put("/{employee_id}", response_model=EmployeeResponse)
def update_employee_endpoint(employee_id: uuid.UUID, request: UpdateEmployeeRequest):
    try:
        return update_employee(
            employee_id=employee_id,
            name=request.name,
            email=request.email,
            phone=request.phone,
            department=request.department,
            position=request.position,
            salary=request.salary
        )
    except ValueError as e:
        if "not found" in str(e):
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{employee_id}", status_code=204)
def delete_employee_endpoint(employee_id: uuid.UUID):
    try:
        delete_employee(employee_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
