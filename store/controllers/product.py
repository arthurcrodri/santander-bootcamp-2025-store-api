# store/controllers/product.py

from fastapi import APIRouter, Body, status
from store.schemas.product import ProductIn, ProductOut
from store.usecases.product import product_usecase

router = APIRouter(prefix="/products", tags=["products"])

@router.post(path="/", status_code=status.HTTP_201_CREATED)
async def create(body: ProductIn = Body(...)) -> ProductOut:
    """
    Cria um novo produto na base de dados.
    """
    return await product_usecase.create_product(body=body)

@router.get("/{id}")
async def get(id: str):
    pass

@router.get("/")
async def query():
    pass

@router.patch("/{id}")
async def update(id: str):
    pass

@router.delete("/{id}")
async def delete(id: str):
    pass