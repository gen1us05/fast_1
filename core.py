from fastapi import FastAPI
from auth import auth_router
from category import category_router
from orders import order_router
from product import product_router


app = FastAPI()
app.include_router(auth_router)
app.include_router(category_router)
app.include_router(order_router)
app.include_router(product_router)


@app.get("/")
async def landing():
    return {
        "Hello": "World landing"
    }


@app.get("/test")
async def test():
    return {
        "Hello": "World test"
    }


@app.get("/user")
async def intro():
    return {
        "Hello": "World user page"
    }

@app.get("/user/{id}")
async def intro(id: int):
    return {
        "message": f"user - {id}"
    }


@app.post("/test")
async def test2():
    return {
        "Hello": "World test post request"
    }



