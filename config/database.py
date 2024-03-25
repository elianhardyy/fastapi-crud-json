from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import dotenv_values
env = dotenv_values(".env")

DATABASE_URL = "mysql+pymysql://root:@localhost:3306/pyfastapi"
#mysql://root:@localhost:3306/pyfastapi
db_engine = create_engine(env["DATABASE_URL"])

SessionLocal =sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
Base =declarative_base()

