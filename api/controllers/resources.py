from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..models import models, schemas
from ..dependencies.database import get_db

router = APIRouter(prefix="/resources", tags=["Resources"])

#Create Resource
@router.post("/", response_model=schemas.Resource)
def create_resource(resource: schemas.ResourceCreate, db: Session = Depends(get_db)):
    db_resource = models.Resource(**resource.dict())
    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)
    return db_resource

#Read All Resources
@router.get("/", response_model=list[schemas.Resource])
def read_resources(db: Session = Depends(get_db)):
    return db.query(models.Resource).all()

#Read One Resource
@router.get("/{resource_id}", response_model=schemas.Resource)
def read_one_resource(resource_id: int, db: Session = Depends(get_db)):
    resource = db.query(models.Resource).filter(models.Resource.id == resource_id).first()
    if resource is None:
        raise HTTPException(status_code=404, detail="Resource not found")
    return resource

#Update Resource
@router.put("/{resource_id}", response_model=schemas.Resource)
def update_resource(resource_id: int, resource: schemas.ResourceUpdate, db: Session = Depends(get_db)):
    db_resource = db.query(models.Resource).filter(models.Resource.id == resource_id).first()
    if db_resource is None:
        raise HTTPException(status_code=404, detail="Resource not found")

    for key, value in resource.dict().items():
        setattr(db_resource, key, value)

    db.commit()
    db.refresh(db_resource)
    return db_resource

#Delete Resource
@router.delete("/{resource_id}")
def delete_resource(resource_id: int, db: Session = Depends(get_db)):
    resource = db.query(models.Resource).filter(models.Resource.id == resource_id).first()
    if resource is None:
        raise HTTPException(status_code=404, detail="Resource not found")

    db.delete(resource)
    db.commit()
    return {"message": "Resource deleted"}