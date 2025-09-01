# store/usecases/product.py

from uuid import UUID, uuid4
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from bson.decimal128 import Decimal128
from fastapi import HTTPException, status
from typing import List, Optional

from store.core.db import db_client
from store.schemas.product import ProductIn, ProductOut, ProductUpdate, ProductUpdateOut

class ProductUsecase:
    def __init__(self) -> None:
        self.client: AsyncIOMotorClient = db_client.client
        self.database: AsyncIOMotorDatabase = self.client.get_database()
        self.collection = self.database.get_collection("products")

    async def create_product(self, body: ProductIn) -> ProductOut:
        # 1. Prepara o modelo Pydantic para a resposta (com tipos Python)
        product_model = ProductOut(id=uuid4(), created_at=datetime.utcnow(), updated_at=datetime.utcnow(), **body.model_dump())

        # 2. Prepara os dados para o banco de dados (convertendo tipos)
        product_db_data = product_model.model_dump()
        product_db_data["_id"] = product_db_data.pop("id")
        product_db_data["price"] = Decimal128(str(product_db_data["price"]))

        # 3. Insere no banco
        await self.collection.insert_one(product_db_data)

        # 4. Retorna o modelo Pydantic original
        return product_model

    async def get_product(self, id: UUID) -> ProductOut:
        result = await self.collection.find_one({"_id": id})
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product not found with id: {id}")
        
        # Converte o Decimal128 do banco para string antes de validar com Pydantic
        result["price"] = str(result["price"])
        result["id"] = result.pop("_id")
        return ProductOut(**result)

    async def query_products(self, min_price: Optional[float], max_price: Optional[float]) -> List[ProductOut]:
        query = {}
        if min_price is not None:
            query["price"] = {"$gt": Decimal128(str(min_price))}
        if max_price is not None:
            if "price" in query:
                query["price"]["$lt"] = Decimal128(str(max_price))
            else:
                query["price"] = {"$lt": Decimal128(str(max_price))}
        
        # Converte os dados do banco para um formato compatível com Pydantic
        items = [
            ProductOut(**{**item, "id": item.pop("_id"), "price": str(item["price"])}) 
            async for item in self.collection.find(query)
        ]
        return items

    async def update_product(self, id: UUID, body: ProductUpdate) -> ProductUpdateOut:
        update_data = body.model_dump(exclude_unset=True)

        if "updated_at" not in update_data:
            update_data["updated_at"] = datetime.utcnow()
        
        if "price" in update_data:
            update_data["price"] = Decimal128(str(update_data["price"]))

        result = await self.collection.find_one_and_update(
            filter={"_id": id},
            update={"$set": update_data},
            return_document=True
        )

        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product not found with id: {id}")
        
        result["price"] = str(result["price"])
        result["id"] = result.pop("_id")
        return ProductUpdateOut(**result)

    async def delete_product(self, id: UUID) -> bool:
        result = await self.collection.delete_one({"_id": id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product not found with id: {id}")
        return True

product_usecase = ProductUsecase()