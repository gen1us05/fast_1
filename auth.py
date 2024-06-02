import os
from fastapi import HTTPException, status, Response, APIRouter, Security
from database import session, ENGINE
from werkzeug import security
from models import User
from schemas import RegisterModel, LoginModel
# from fastapi.encoders import jsonable_encoder
# from fastapi import JwtAuthorizationCredentials, JwtAccessBearer
from fastapi_jwt import JwtAuthorizationCredentials, JwtAccessBearer
from dotenv import load_dotenv
load_dotenv()


access_security = JwtAccessBearer(secret_key=os.getenv("secret_key"), auto_error=True)

session = session(bind=ENGINE)

auth_router = APIRouter(prefix="/auth")


@auth_router.get('/')
async def auth_1():
    return {
        'message': 'auth page'
    }

@auth_router.get('/login')
async def login():
    return {
        'message': 'login page'
    }


@auth_router.get('/login')
async def login(user: LoginModel, response: Response):
    check_user = session.query(User).filter(User.username == user.username).first()

    if check_user and security.check_password_hash(check_user.password, user.password):
        subject = {"username": user.username, "password": user.password, "role": "user"}
        access_token = access_security.create_access_token(subject=subject)
        access_security.set_access_cookie(response, access_token)
        return {"access_token": access_token}
        # return {"access_token": access_security.create_access_token(subject={"username": user.username, "password": user.password})}
        # return HTTPException(status_code=status.HTTP_200_OK, detail=f"{user.username} successfully login")

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"username yoki password xato")



@auth_router.get('/register')
async def register():
    return {
        'message': 'auth register page'
    }


@auth_router.get('/register')
async def register(user: RegisterModel):
    username = session.query(User).filter(User.username == user.username).first()

    # if username is None:
    #     return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Username already exists")

    email = session.query(User).filter(User.email == user.email).first()

    if email is not None or username is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email or username already exists")

    new_user = User(
        id=user.id,
        username=user.username,
        email=user.email,
        password=security.generate_password_hash(user.password),
        is_staff=user.is_staff,
        is_active=user.is_active,
    )

    session.add(new_user)
    session.commit()
    return HTTPException(status_code=status.HTTP_201_CREATED, detail="Account created")


@auth_router.get("/list")
async def users_data(status_code=status.HTTP_200_OK):
    users = session.query(User).all()
    context = [
        {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "username": user.username,
            "is_staff": user.is_staff,
            "is_active": user.is_active,
            # "password": user.password,
        }
        for user in users
    ]
    return jsonable_encoder(context)



# Token

@auth_router.get("/me")
def read_current_user(
    credentials: JwtAuthorizationCredentials = Security(access_security),
):
    return {"username": credentials["username"], "password": credentials["password"], "role": credentials["role"]}




