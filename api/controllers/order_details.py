from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..models import models, schemas
from ..dependencies.database import get_db

router = APIRouter(prefix="/order_details", tags=["Order Details"])

#Create Order_Detail
@router.post("/", response_model=schemas.OrderDetail)
def create_order_detail(order: schemas.OrderDetailCreate, db: Session = Depends(get_db)):
    db_order = models.OrderDetail(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

#Read All Order_Details
@router.get("/", response_model=list[schemas.OrderDetail])
def read_order_details(db: Session = Depends(get_db)):
    return db.query(models.OrderDetail).all()

#Read One Order_Detail
@router.get("/{order_id}", response_model=schemas.OrderDetail)
def read_one_order_detail(order_id: int, db: Session = Depends(get_db)):
    order = db.query(models.OrderDetail).filter(models.OrderDetail.id == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order detail not found")
    return order

#Update Order_Detail
@router.put("/{order_id}", response_model=schemas.OrderDetail)
def update_order_detail(order_id: int, order: schemas.OrderDetailUpdate, db: Session = Depends(get_db)):
    db_order = db.query(models.OrderDetail).filter(models.OrderDetail.id == order_id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order detail not found")

    for key, value in order.dict().items():
        setattr(db_order, key, value)

    db.commit()
    db.refresh(db_order)
    return db_order

#Delete Order_Detail
@router.delete("/{order_id}")
def delete_order_detail(order_id: int, db: Session = Depends(get_db)):
    order = db.query(models.OrderDetail).filter(models.OrderDetail.id == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order detail not found")

    db.delete(order)
    db.commit()
    return {"message": "Order detail deleted"}