from sqlalchemy.orm import Session
from sqlalchemy import update, insert, delete
import models, schemas
from auth import hash_password_md5


def get_user_by_phone_number(db: Session, phone_number: int):
    return db.query(models.User).filter(models.User.phone_number == phone_number).first()


def add_credit_to_user(db: Session, user_id: int, credit: int):
    add_credit = (
        update(models.User)
        .where(models.User.user_id == user_id)
        .values(credit=models.User.credit + credit)
        .returning(models.User)
    )
    result = db.execute(add_credit)
    db.commit()

    return result.scalar()


def create_user(db: Session, user: schemas.SignUpRequirement):
    hash_password = hash_password_md5(user.password)
    db_user = models.User(first_name=user.first_name, phone_number=user.phone_number, hashed_password=hash_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def new_customer_no_commit(db: Session, customer_id, bakery_id, datetime):
    customer = models.Customer(customer_id=customer_id, bakery_id=bakery_id, register_date=datetime)
    db.add(customer)
    db.flush()
    return customer.id
