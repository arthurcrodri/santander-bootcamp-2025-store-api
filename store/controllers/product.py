from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Body, Depends, HTTPException, Query, status
from store.schemas.product import ProductIn, ProductOut, ProductUpdate, ProductUpdateOut
from store.usecases.product import product_usecase

router = APIRouter(prefix="/products", tags=["products"])

@router.post(path="/", status_code=status.HTTP_201_CREATED)
async def create(body: ProductIn = Body(...)) -> ProductOut:
    try:
        return await product_usecase.create_product(body=body)
    except Exception as e:
        
        import traceback
        traceback.print_exc()

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get(path="/{id}", status_code=status.HTTP_200_OK)
async def get(id: UUID) -> ProductOut:
    return await product_usecase.get_product(id=id)

@router.get(path="/", status_code=status.HTTP_200_OK)
async def query(
    min_price: Optional[float] = Query(None, alias="min_price"),
    max_price: Optional[float] = Query(None, alias="max_price")
) -> List[ProductOut]:
    # Requisito: aplicar um filtro de preço
    return await product_usecase.query_products(min_price=min_price, max_price=max_price)

@router.patch(path="/{id}", status_code=status.HTTP_200_OK)
async def update(id: UUID, body: ProductUpdate = Body(...)) -> ProductUpdateOut:
    # Requisito: retornar not found e mensagem amigável
    return await product_usecase.update_product(id=id, body=body)

@router.delete(path="/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: UUID) -> None:
    await product_usecase.delete_product(id=id)