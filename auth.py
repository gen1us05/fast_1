from fastapi import APIRouter
from database import session, ENGINE
from werkzeug import security
from models import User
from schemas import RegisterModel, LoginModel
from fastapi import HTTPException
from fastapi import status

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
async def login(user: LoginModel):
    username = session.query(User).filter(User.username == user.username).first()
    if username is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='username xato!!!')

    # password = session.query(User).filter(User.password == security.generate_password_hash(user.password)).first()

    user_check = session.query(User).filter(User.username == user.username).first()

    if security.check_password_hash(user_check.password, user.password):
        return HTTPException(status_code=status.HTTP_200_OK, detail=F"{user.username} login")


    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='username yoki parol xato!!!')


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
