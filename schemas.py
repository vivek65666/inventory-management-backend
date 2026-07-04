from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


# ==================== User Schemas ====================
class UserCreate(BaseModel):
    """Schema for creating a new user."""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)


class UserLogin(BaseModel):
    """Schema for user login."""
    username: str
    password: str


class UserResponse(BaseModel):
    """Schema for user response."""
    id: int
    username: str
    email: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# ==================== Token Schemas ====================
class Token(BaseModel):
    """Schema for authentication token."""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema for token payload data."""
    username: Optional[str] = None


# ==================== Product Schemas ====================
class ProductCreate(BaseModel):
    """Schema for creating a product."""
    sku: str = Field(..., min_length=1, max_length=100)
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    price: float = Field(..., gt=0)


class ProductUpdate(BaseModel):
    """Schema for updating a product."""
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)


class ProductResponse(BaseModel):
    """Schema for product response."""
    id: int
    sku: str
    name: str
    description: Optional[str]
    price: float
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ==================== Inventory Schemas ====================
class InventoryItemCreate(BaseModel):
    """Schema for creating an inventory item."""
    product_id: int
    quantity: int = Field(..., ge=0)
    warehouse_location: Optional[str] = None


class InventoryItemUpdate(BaseModel):
    """Schema for updating inventory item."""
    quantity: Optional[int] = Field(None, ge=0)
    warehouse_location: Optional[str] = None


class InventoryItemResponse(BaseModel):
    """Schema for inventory item response."""
    id: int
    product_id: int
    quantity: int
    warehouse_location: Optional[str]
    created_at: datetime
    updated_at: datetime
    product: ProductResponse
    
    class Config:
        from_attributes = True


class InventoryListResponse(BaseModel):
    """Schema for inventory list with pagination."""
    total: int
    items: list[InventoryItemResponse]
