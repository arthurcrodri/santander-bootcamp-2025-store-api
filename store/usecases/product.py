from uuid import UUID
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
        product_model = ProductOut(**body.model_dump())
        
        product_data = product_model.model_dump(exclude={"id"})
        product_data["_id"] = product_model.id
        product_data["price"] = Decimal128(str(product_data["price"]))

        await self.collection.insert_one(product_data)
        return product_model

    async def get_product(self, id: UUID) -> ProductOut:
        result = await self.collection.find_one({"_id": id})
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product not found with id: {id}")
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
        
        return [ProductOut(**item) async for item in self.collection.find(query)]

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
        
        return ProductUpdateOut(**result)

    async def delete_product(self, id: UUID) -> bool:
        result = await self.collection.delete_one({"_id": id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product not found with id: {id}")
        return True

product_usecase = ProductUsecase()