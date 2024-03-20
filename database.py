from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker

url = URL.create(
    drivername="postgresql",
    username="postgres",
    password="sa",
    host="localhost",
    database="ecommerce",
    port=5432
)

engine = create_engine(url)
Session = sessionmaker(bind=engine)
session = Session()