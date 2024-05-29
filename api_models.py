from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []



@app.get('/')
async def index():
    return {
        "message": "Index API"
    }


@app.post("/items/")
async def create_item(item: Item) -> Item:
    return item


@app.get("/items/")
async def read_items() -> list:

    return [
        {
            "name": "John",
            "password": "john1"
        },
        {
            "name": "Ali",
            "password": "ali123"
        },
        {
            "name": "Mustafo",
            "password": "mustafo123"
        }
    ]

    # return [
    #     Item(name="Portal gumn", price=42.0),
    #     Item(name="Plumbs", price=32.0)
    # ]


