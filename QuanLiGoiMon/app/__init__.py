from flask import Flask
from urllib.parse import quote
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:%s@localhost/restaurantdb?charset=utf8mb4' % quote('root') # truyen passwork mysql
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["FOOD_SIZE"] = 8
app.config["ORDER_SIZE"] = 5
app.config["TABLE_SIZE"] = 8
app.config["RERENDER"] = False
app.config['SECRET_KEY'] = 'khong_muoi_hoi_phi'
db = SQLAlchemy(app=app)
login = LoginManager(app=app)

# dung cho thong bao waiter
notifications = {
    "id" : []
}