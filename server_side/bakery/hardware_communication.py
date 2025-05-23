from typing import Optional
from fastapi import APIRouter, HTTPException, Header
import crud
import schemas, tasks
from database import SessionLocal

router = APIRouter(
    prefix='/hc',
    tags=['hardware_communication']
)

bakery_token = {}

def get_token(bakery_id):
    if bakery_id not in bakery_token:
        db = SessionLocal()
        try:
            bakery = crud.get_bakery(db, bakery_id)
            if not bakery: raise ValueError
            bakery_token[bakery_id] = bakery.token
        finally:
            db.close()
    return bakery_token[bakery_id]


def verify_token(token: str, bakery_id: int) -> bool:
    return get_token(bakery_id) == token

@router.post('/nc')
async def new_customer(
    customer: schemas.NewCustomerRequirement,
    authorization: Optional[str] = Header(None)
):
    if authorization is None or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=400, detail="Invalid or missing Authorization header")

    token = authorization[len("Bearer "):]
    if not verify_token(token, customer.bakery_id):
        raise HTTPException(status_code=401, detail="Invalid token")

    tasks.register_new_customer.delay(customer.hardware_customer_id, customer.bakery_id, customer.bread_requirements)
    return {'status': 'Processing'}


@router.post('/nt')
async def next_ticket(
    ticket: schemas.NextTicketRequirement,
    authorization: Optional[str] = Header(None)
):
    if authorization is None or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=400, detail="Invalid or missing Authorization header")

    token = authorization[len("Bearer "):]
    if not verify_token(token, ticket.bakery_id):
        raise HTTPException(status_code=401, detail="Invalid token")
    tasks.next_ticket_process.delay(ticket.current_customer_id, ticket.bakery_id)
    return {'status': 'Processing'}


@router.get('/hardware_init')
async def hardware_initialize(bakery_id: int):
    db = SessionLocal()
    try:
        all_bakery_bread = crud.get_bakery_breads(db, bakery_id)
        bread_time = {}
        for bakery_bread in all_bakery_bread:
            bread_time[bakery_bread.bread_type_id] = bakery_bread.cook_time_s
        return bread_time
    finally:
        db.close()

