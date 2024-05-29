from database import ENGINE, Base
from models import User, Category, Order, Product


Base.metadata.create_all(ENGINE)

