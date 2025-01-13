from peewee import *
import os

from dotenv import load_dotenv
load_dotenv()
db_name = os.getenv("db_name")
user = os.getenv("db_user")
password = os.getenv("db_password")
host = os.getenv("db_host")
port = os.getenv("db_port")

db = PostgresqlDatabase(db_name, user=user, password=password, host=host, port=port)