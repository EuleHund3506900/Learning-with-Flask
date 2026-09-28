from flask import Flask
from base.errorhandler import ErrorHandler

from base.jwt import init_rsa_keys
from database.db import init_db
from dotenv import load_dotenv

from router import Router

load_dotenv()  # reads variables from a .env file and sets them in os.environ


app = Flask(__name__)
ErrorHandler(app)
Router(app)




if __name__ == "__main__":
  init_db()
  init_rsa_keys()
  app.run(debug=True)