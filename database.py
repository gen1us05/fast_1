from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

ENGINE = create_engine(f'postgresql://postgres:password@localhost:5432/fast_3', echo=True)
Base = declarative_base()
session = sessionmaker()



