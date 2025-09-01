from fastapi import APIRouter

router = APIRouter(prefix="/products")

@router.post("/")
async def create():
    pass

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