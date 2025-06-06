from pydantic import BaseModel
from typing import Dict

class SignUpRequirement(BaseModel):
    phone_number: str
    first_name: str
    last_name: str
    password: str

class SignUpReturn(BaseModel):
    user_id: int

class LogInRequirement(BaseModel):
    phone_number: str
    password: str

class BakeryID(BaseModel):
    bakery_id: int

class NewCustomerRequirement(BakeryID):
    hardware_customer_id: int
    bread_requirements: Dict[str, int]

class NextTicketRequirement(BakeryID):
    current_customer_id: int
    next_customer_id: int

class Initialize(BakeryID):
    bread_type_and_cook_time: Dict[str, int]

class AddBakery(BaseModel):
    name: str
    location: str

class AddBakeryResult(BakeryID):
    token: str

class AddBread(BaseModel):
    name: str

class AddBreadResult(BaseModel):
    bread_id: int

class NewAdminRequirement(BaseModel):
    user_id: int
    status: bool = False

class NewAdminResult(BaseModel):
    admin_id: int

    class Config:
        from_attributes = True