from fastapi import APIRouter, status, HTTPException
from models import Product, Category
from schemas import ProductModel, CategoryModel
from database import session, ENGINE
from fastapi.encoders import jsonable_encoder


product_router = APIRouter(prefix='/product')
session = session(bind=ENGINE)

@product_router.get('/')
async def product_list():
    products = session.query(Product).all()
    contex = [
        {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "category_id": product.category_id,
        }
        for product in products
    ]
    return jsonable_encoder(contex)


@product_router.post('/create')
async def product_create(product: ProductModel):
    check_product_id = session.query(Product).filter(Product.id == product.id).first()
    check_category_id = session.query(Category).filter(Category.id == product.category_id).first()
    if (check_product_id and check_category_id) or (check_product_id and check_category_id is None):
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bu Product oldin yaratilgan")


    new_product = Product(
        id=product.id,
        name=product.name,
        description=product.description,
        price=product.price,
        category_id=product.category_id
    )

    session.add(new_product)
    session.commit()

    data = {
        "core":200,
        "success":True,
        "msg":"Created new product",
        "data":{
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "category_id": product.category_id
        }
    }

    return data




@product_router.get('/{id}')
async def product_id(id:int):
    check_product = session.query(Product).filter(Product.id == id).first()
    if check_product:
        contex ={
            "id": check_product.id,
            "name": check_product.name,
            "description": check_product.description,
            "price": check_product.price,
            "category_id": check_product.category_id,
        }
        return jsonable_encoder(contex)
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bunday product mavjud emas")




@product_router.put('/{id}')
async def product_update(id: int, data: ProductModel):
    product = session.query(Product).filter(Product.id == id).first()
    check_category_id = session.query(Category).filter(Category.id == data.category_id).first()

    if product:
        if check_category_id:
            for key, value in data.dict(exclude_unset=True).items():
                setattr(product, key, value)
            session.commit()
            data = {
                "code": 200,
                "message": "Product updated"
            }
            return jsonable_encoder(data)
        else:
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Field")

    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Field")


@product_router.delete('/{id}')
async def product_delete(id: int):
    check_product = session.query(Product).filter(Product.id == id).first()
    if check_product:
        session.delete(check_product)
        session.commit()
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Successfully deleated")

    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")



