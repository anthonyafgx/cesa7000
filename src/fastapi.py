from fastapi import FastAPI
from src.customer.api import router as customer_router
from src.employee.api import router as employee_router

app = FastAPI(title="CESA7000")

app.include_router(customer_router)
app.include_router(employee_router)