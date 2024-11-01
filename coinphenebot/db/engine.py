from sqlalchemy import create_engine
from db.models import BaseModel
from sqlalchemy.orm import Session

db_url = "sqlite:///db.sqlite3"

engine = create_engine(db_url, echo=True)

with engine.connect() as connection:
    BaseModel.metadata.create_all(bind=engine)
    print(f"connected to db")

session = Session(bind=engine)


def init_db():
    print("database initialized")
