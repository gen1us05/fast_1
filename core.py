from fastapi import FastAPI
from auth import auth_router
from api_models import create_item


app = FastAPI()
app.include_router(auth_router)
app.include_router(create_item)



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



