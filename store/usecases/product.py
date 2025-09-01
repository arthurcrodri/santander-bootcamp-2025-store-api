# store/usecases/product.py

from uuid import uuid4
from datetime import datetime
from bson.decimal128 import Decimal128
from store.core.db import db_client
from store.schemas.product import ProductIn, ProductOut

class ProductUsecase:
    async def create_product(self, body: ProductIn) -> ProductOut:
        # Cria o modelo de saída com os dados de entrada
        product_model = ProductOut(
            id=uuid4(), 
            created_at=datetime.utcnow(), 
            updated_at=datetime.utcnow(), 
            **body.model_dump()
        )
        
        # Converte o modelo para um dicionário, preparando para o BSON
        product_data = product_model.model_dump()
        product_data["price"] = Decimal128(str(product_data["price"]))

        # Insere no banco de dados
        collection = db_client.get_database().get_collection("products")
        await collection.insert_one(product_data)

        return product_model

product_usecase = ProductUsecase()