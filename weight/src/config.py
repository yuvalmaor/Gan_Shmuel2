import os
import logging
from dotenv import load_dotenv

load_dotenv()

#variables for the MYSQL connection header
DATABASE_USER = os.environ.get('DATABASE_USER')
DATABASE_NAME = os.environ.get('DATABASE_NAME')
DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD')
HOST = os.environ.get('HOST')
PORT = int(os.environ.get('PORT'))

#logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename="./logs/weight-logs.txt")
logger = logging.getLogger(__name__)

class Config:
    SQLALCHEMY_DATABASE_URI =  f"mysql+pymysql://{DATABASE_USER}:{DATABASE_PASSWORD}@{HOST}:{PORT}/{DATABASE_NAME}"
