from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
import models
import schemas
from auth import get_current_user
from database import get_db

router = APIRouter(prefix="/api/inventory", tags=["Inventory"])


@router.post("", response_model=schemas.InventoryItemResponse, status_code=status.HTTP_201_CREATED)
def create_inventory_item(
    item: schemas.InventoryItemCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new inventory item."""
    # Verify product exists
    product = db.query(models.Product).filter(
        models.Product.id == item.product_id
    ).first()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    db_item = models.InventoryItem(
        **item.dict(),
        created_by=current_user.id
    )
    
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    
    return db_item


@router.get("", response_model=schemas.InventoryListResponse)
def list_inventory(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    product_id: int = Query(None),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List inventory items with optional filtering."""
    query = db.query(models.InventoryItem)
    
    if product_id:
        query = query.filter(models.InventoryItem.product_id == product_id)
    
    total = query.count()
    items = query.offset(skip).limit(limit).all()
    
    return {"total": total, "items": items}


@router.get("/{item_id}", response_model=schemas.InventoryItemResponse)
def get_inventory_item(
    item_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific inventory item."""
    item = db.query(models.InventoryItem).filter(
        models.InventoryItem.id == item_id
    ).first()
    
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inventory item not found"
        )
    
    return item


@router.put("/{item_id}", response_model=schemas.InventoryItemResponse)
def update_inventory_item(
    item_id: int,
    item_update: schemas.InventoryItemUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update an inventory item."""
    db_item = db.query(models.InventoryItem).filter(
        models.InventoryItem.id == item_id
    ).first()
    
    if not db_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inventory item not found"
        )
    
    update_data = item_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_item, key, value)
    
    db.commit()
    db.refresh(db_item)
    
    return db_item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_inventory_item(
    item_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete an inventory item."""
    db_item = db.query(models.InventoryItem).filter(
        models.InventoryItem.id == item_id
    ).first()
    
    if not db_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inventory item not found"
        )
    
    db.delete(db_item)
    db.commit()


@router.post("/{item_id}/adjust-quantity")
def adjust_inventory_quantity(
    item_id: int,
    quantity_change: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Adjust inventory quantity by a specified amount."""
    db_item = db.query(models.InventoryItem).filter(
        models.InventoryItem.id == item_id
    ).first()
    
    if not db_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inventory item not found"
        )
    
    new_quantity = db_item.quantity + quantity_change
    
    if new_quantity < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Quantity cannot be negative"
        )
    
    db_item.quantity = new_quantity
    db.commit()
    db.refresh(db_item)
    
    return {"item_id": db_item.id, "new_quantity": db_item.quantity}
