from flask import Flask
from src.logger import logging

app = Flask(__name__)
@app.route('/',methods=['GET','POST'])
def index():
   logging.info("We are testing loggin file")
   return "welcome"


if __name__== "__main__":
   app.run(debug=True)
  