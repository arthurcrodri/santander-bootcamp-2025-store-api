from typing import Optional
from decimal import Decimal
from pydantic import BaseModel, Field, UUID4
from datetime import datetime

class ProductBase(BaseModel):
    name: str = Field(..., description="Product name")
    quantity: int = Field(..., description="Product quantity")
    price: Decimal = Field(..., description="Product price")
    status: bool = Field(..., description="Product status")

class ProductIn(ProductBase):
    ...

class ProductOut(ProductIn):
    id: UUID4 = Field(..., description="Product identifier")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

class ProductUpdate(BaseModel):
    quantity: Optional[int] = Field(None, description="Product quantity")
    price: Optional[Decimal] = Field(None, description="Product price")
    status: Optional[bool] = Field(None, description="Product status")
    # Para cumprir o requisito de poder modificar updated_at manualmente
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")