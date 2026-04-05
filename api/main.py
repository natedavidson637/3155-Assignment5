from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .models import models, schemas
from .dependencies.database import engine, get_db

# Import routers
from .controllers import sandwiches, resources, recipes, order_details, orders

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# Orders Endpoints (existing)
# -------------------------

@app.post("/orders/", response_model=schemas.Order, tags=["Orders"])
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    return orders.create(db=db, order=order)

@app.get("/orders/", response_model=list[schemas.Order], tags=["Orders"])
def read_orders(db: Session = Depends(get_db)):
    return orders.read_all(db)

@app.get("/orders/{order_id}", response_model=schemas.Order, tags=["Orders"])
def read_one_order(order_id: int, db: Session = Depends(get_db)):
    order = orders.read_one(db, order_id=order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@app.put("/orders/{order_id}", response_model=schemas.Order, tags=["Orders"])
def update_one_order(order_id: int, order: schemas.OrderUpdate, db: Session = Depends(get_db)):
    order_db = orders.read_one(db, order_id=order_id)
    if order_db is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return orders.update(db=db, order=order, order_id=order_id)

@app.delete("/orders/{order_id}", tags=["Orders"])
def delete_one_order(order_id: int, db: Session = Depends(get_db)):
    order = orders.read_one(db, order_id=order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return orders.delete(db=db, order_id=order_id)

# -------------------------
# Include Routers
# -------------------------

app.include_router(sandwiches.router)
app.include_router(resources.router)
app.include_router(recipes.router)
app.include_router(order_details.router)