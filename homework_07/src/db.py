import pathlib

from configparser import ConfigParser  # to parse config files

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

file_config = pathlib.Path(__file__).parent.parent.joinpath("config.ini")
config = ConfigParser()
config.read(file_config)

username = config.get("DB", "USER")
password = config.get("DB", "PASSWORD")
db_name = config.get("DB", "DB_NAME")
domain = config.get("DB", "DOMAIN")
port = config.get("DB", "PORT")

# postgresql://username:password@domain_name:port/database_name
url = f"postgresql://{username}:{password}@{domain}:{port}/{db_name}"
Base = declarative_base()
engine = create_engine(url, echo=False, pool_size=5)  # psycopg2 - db driver

DBSession = sessionmaker(bind=engine)
session = DBSession()
