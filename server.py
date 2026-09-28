from flask import Flask
from base.errorhandler import ErrorHandler

from base.jwt import init_rsa_keys
from database.db import init_db
from dotenv import load_dotenv

from router import Router

import logging

load_dotenv()  # reads variables from a .env file and sets them in os.environ

logger = logging.getLogger(__name__)

app = Flask(__name__)
ErrorHandler(app)
Router(app)

logging.basicConfig(filename='logs/app.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

if __name__ == "__main__":
  init_db()
  logger.info("Database initialized.")
  init_rsa_keys()
  logger.info("Starting the application...")
  app.run(debug=True)