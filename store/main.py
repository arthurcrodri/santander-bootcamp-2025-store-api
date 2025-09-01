from fastapi import FastAPI
from store.controllers.product import router as product_router

app = FastAPI(title="Store API")
app.include_router(product_router)