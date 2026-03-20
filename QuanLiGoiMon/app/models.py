import datetime
from app import db, app
from sqlalchemy import Integer,Float, Column, String, DateTime, ForeignKey, Boolean, Enum
from enum import Enum as PyEnum
from flask_login import UserMixin

class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    active = Column(Boolean, default=True)

class UserRole(PyEnum):
    PHUCVU = 1
    NHABEP = 2
    THUNGAN = 3
    QUANLI = 4
    ADMIN = 5

ROLES = {
        UserRole.PHUCVU: {"name": "waiter", "name_vn": "Phục vụ"},
        UserRole.NHABEP: {"name": "cook", "name_vn": "Nhà Bếp"},
        UserRole.THUNGAN: {"name": "cashier", "name_vn": "Thu ngân"},
        UserRole.QUANLI: {"name": "manager", "name_vn": "Quản lí"},
        UserRole.ADMIN: {"name": "admin", "name_vn": "Quản trị viên"}
    }

class User(UserMixin, BaseModel):
    name = Column(String(50), nullable=False)
    avatar = Column(String(100), default='https://res.cloudinary.com/durpn2bki/image/upload/v1765900550/avt_ksovcr.jpg')
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    user_role = Column(Enum(UserRole), default=UserRole.PHUCVU)
    active = None

    def __str__(self):
        return self.name

class Category(BaseModel):
    name = Column(String(50), unique=True)

    def __str__(self):
        return self.name

class Food(BaseModel):
    name = Column(String(50), unique=True)
    price = Column(Integer)
    image = Column(String(100), default='https://res.cloudinary.com/dxxwcby8l/image/upload/v1647248722/r8sjly3st7estapvj19u.jpg')

    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
    category = db.relationship("Category", backref="foods", lazy=True)
    food_orders = db.relationship("FoodOrder", backref="food", lazy=True)

    def __str__(self):
        return self.name

class TableStatus(PyEnum):
    EMPTY = "EMPTY"
    SERVING = "SERVING"

class Table(BaseModel):
    name = Column(String(50), unique=True)
    status = Column(Enum(TableStatus), default=TableStatus.EMPTY)
    image = Column(String(100), default='https://res.cloudinary.com/durpn2bki/image/upload/v1765902218/banann_nbpw3u.png')

    def __str__(self):
        return self.name
    
class OrderStatus(PyEnum):
    OPEN = "OPEN"
    CLOSE = "CLOSED"

class Order(BaseModel):
    status = Column(Enum(OrderStatus), default=OrderStatus.OPEN)
    created_date = Column(DateTime, default=datetime.datetime.now)

    table_id = Column(Integer, ForeignKey(Table.id), nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    table = db.relationship("Table", backref="orders")
    order_foods = db.relationship("FoodOrder", backref="order", lazy=True)
    active = None

class FoodOrderStatus(PyEnum):
    PENDING = "pending"     # chưa nấu
    COOKING = "cooking"     # đang nấu
    DONE = "done"           # hoàn tất

class FoodOrder(BaseModel):
    quantity = Column(Integer, default=1)
    price = Column(Integer)
    note = Column(String(100), default='')
    status = Column(Enum(FoodOrderStatus), default=FoodOrderStatus.PENDING)
    created_date = Column(DateTime, default=datetime.datetime.now)

    food_id = Column(Integer, ForeignKey('food.id'), nullable=False)
    order_id = Column(Integer, ForeignKey('order.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    active = None

    def __str__(self):
        return str(self.quantity)


class VAT(BaseModel):
    vat= Column(Float, default=0.1)
    active = None

    def __str__(self):
        return str(self.vat)
    
class Discount(BaseModel):
    discount= Column(Float, default=0.0)
    active = None

    def __str__(self):
        return self.discount

class Bill(BaseModel):
    created_date= Column(DateTime, default=datetime.datetime.now)
    total_amount = Column(Float, default=0.0)
    order_id = Column(Integer, ForeignKey(Order.id), nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    vat_id= Column(Integer, ForeignKey(VAT.id), nullable=False)
    discount_id= Column(Integer, ForeignKey(Discount.id), nullable=False)
    active = None

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        import hashlib
        u = User(name="Admin", username="admin", password=str(hashlib.md5("1".encode('utf-8')).hexdigest()),
                 user_role=UserRole.ADMIN)
        db.session.add(u)

        phuc_vu1 = User(name="Phuc Vu 1", username="phucvu1", password=str(hashlib.md5("1".encode('utf-8')).hexdigest()),
                        user_role=UserRole.PHUCVU)
        
        phuc_vu2 = User(name="Phuc Vu 2", username="phucvu2", password=str(hashlib.md5("1".encode('utf-8')).hexdigest()),
                        user_role=UserRole.PHUCVU)
        
        nha_bep1 = User(name="Nha Bep 1", username="nhabep1", password=str(hashlib.md5("1".encode('utf-8')).hexdigest()),
                        user_role=UserRole.NHABEP)
        
        nha_bep2 = User(name="Nha Bep 2", username="nhabep2", password=str(hashlib.md5("1".encode('utf-8')).hexdigest()),
                        user_role=UserRole.NHABEP)
        
        quan_li1 = User(name="Quan Li 1", username="quanli1", password=str(hashlib.md5("1".encode('utf-8')).hexdigest()),
                        user_role=UserRole.QUANLI)
        
        quan_li2 = User(name="Quan Li 2", username="quanli2", password=str(hashlib.md5("1".encode('utf-8')).hexdigest()),
                        user_role=UserRole.QUANLI)
        
        thu_ngan1 = User(name="Thu Ngan 1", username="thungan1", password=str(hashlib.md5("1".encode('utf-8')).hexdigest()),
                        user_role=UserRole.THUNGAN)
        
        thu_ngan2 = User(name="Thu Ngan 2", username="thungan2", password=str(hashlib.md5("1".encode('utf-8')).hexdigest()),
                        user_role=UserRole.THUNGAN)
        
        db.session.add_all([phuc_vu1, phuc_vu2, nha_bep1, nha_bep2, quan_li1, quan_li2, thu_ngan1, thu_ngan2])
        db.session.commit()
        c1 = Category(name="Seafood")
        c2 = Category(name="Beef")
        c3 = Category(name="Pork")
        c4 = Category(name="Dessert")
        c5 = Category(name="Drink")
        db.session.add_all([c1,c2,c3,c4,c5])
        db.session.commit()

        t1 = Table(name="Table 01")
        t2 = Table(name="Table 02")
        t3 = Table(name="Table 03")
        t4 = Table(name="Table 04")
        t5 = Table(name="Table 05")
        t6 = Table(name="Table 06")
        t7 = Table(name="Table 07")
        t8 = Table(name="Table 08")
        t9 = Table(name="Table 09")
        t10 = Table(name="Table 10")
        t11 = Table(name="Table 11")
        t12 = Table(name="Table 12")
        db.session.add_all([t1,t2,t3,t4,t5,t6,t7,t8,t9,t10,t11,t12])
        db.session.commit()

        v1= VAT(vat=0.1)
        db.session.add(v1)
        db.session.commit()

        d1= Discount(discount=0.05)
        db.session.add(d1)
        db.session.commit()


        foods = [{
            "name": "Ghẹ hấp bia",
            "price": 155000,
            "image": "https://res.cloudinary.com/durpn2bki/image/upload/v1765901828/ghehapbia_le6nm9.jpg",
            "category_id": 1
        }, {
            "name": "Tôm hùm nướng tỏi",
            "price": 360000,
            "image": "https://res.cloudinary.com/durpn2bki/image/upload/v1765901826/tomhumnuongbotoi_shco53.jpg",
            "category_id": 1
        }, {
            "name": "Lẫu hải sản",
            "price": 455000,
            "image": "https://res.cloudinary.com/durpn2bki/image/upload/v1765901828/lauhaisan_coavhx.jpg",
            "category_id": 1
        }, {
            "name": "Hàu nướng mỡ hành",
            "price": 150000,
            "image": "https://res.cloudinary.com/durpn2bki/image/upload/v1765901831/haunuongmohanh_rn2yt0.jpg",
            "category_id": 1
        }, {
            "name": "Nghêu hấp sả",
            "price": 235000,
            "image": "https://res.cloudinary.com/durpn2bki/image/upload/v1765901832/ngheuhapsa_fbkvwd.jpg",
            "category_id": 1
        }, {
            "name": "Cá hồi sashimi",
            "price": 350000,
            "image": "https://res.cloudinary.com/durpn2bki/image/upload/v1765901833/cahoisashimi_kjmnzs.jpg",
            "category_id": 1
        }, {
            "name": "Mực xào sa tế",
            "price": 195000,
            "image": "https://res.cloudinary.com/durpn2bki/image/upload/v1765901840/mucxaosate_yjvgop.jpg",
            "category_id": 1
        }, {
            "name": "Cá hồi áp chảo",
            "price": 250000,
            "image": "https://res.cloudinary.com/durpn2bki/image/upload/v1765901839/cahoiapchao_afyj2y.jpg",
            "category_id": 1
        }, {
            "name": "Mực chiên giòn",
            "price": 155000,
            "image": "https://res.cloudinary.com/durpn2bki/image/upload/v1765901845/mucchiengion_uz4ja8.jpg",
            "category_id": 1
        }, {
            "name": "Tôm hấp sả",
            "price": 370000,
            "image": "https://res.cloudinary.com/durpn2bki/image/upload/v1765901849/tomhapsa_pja1gq.jpg",
            "category_id": 1
        }, {
            "name": "Bò xào hành tây",
            "price": 120000,
            "image": "https://res.cloudinary.com/durpn2bki/image/upload/v1765900191/boxaohanhtay_zfs3nr.jpg",
            "category_id": 2
        }, {
            "name": "Salat bò nướng",
            "price": 150000,
            "image": "https://res.cloudinary.com/durpn2bki/image/upload/v1765900191/salatbonuong_nqfspu.jpg",
            "category_id": 2
        }, {
            "name": "Bò nướng lá lốt",
            "price": 130000,
            "image": "https://res.cloudinary.com/durpn2bki/image/upload/v1765900191/bonuonglalot_ekbt67.jpg",
            "category_id": 2
        }, {
            "name": "Thịt bò roast beef",
            "price": 160000,
            "image": "https://res.cloudinary.com/durpn2bki/image/upload/v1765900191/boroasr_phldlt.jpg",
            "category_id": 2
        }, {
            "name": "Sườn bò nướng",
            "price": 250000,
            "image": "https://res.cloudinary.com/durpn2bki/image/upload/v1765900191/suonbonuong_cldxu2.jpg",
            "category_id": 2
        }, {
            "name": "Bò lúc lắc",
            "price": 150000,
            "image": "https://res.cloudinary.com/durpn2bki/image/upload/v1765900192/boluclac_dlhnhm.jpg",
            "category_id": 2
        }, {
            "name": "Bò wellington",
            "price": 250000,
            "image": "https://res.cloudinary.com/durpn2bki/image/upload/v1765900191/bowalington_mwlzjd.jpg",
            "category_id": 2
        }, {
            "name": "Bò cuộn phô mai",
            "price": 220000,
            "image": "https://res.cloudinary.com/durpn2bki/image/upload/v1765900192/bocuonphomai_rjznie.jpg",
            "category_id": 2
        }, {
            "name": "Bò sốt đỏ",
            "price": 270000,
            "image": "https://res.cloudinary.com/durpn2bki/image/upload/v1765900391/bosovangdo_nm2q1g.jpg",
            "category_id": 2
        }, {
            "name": "Bò sốt tiêu đen",
            "price": 260000,
            "image": "https://res.cloudinary.com/durpn2bki/image/upload/v1765900392/bosottieuden_e4viqe.jpg",
            "category_id": 2
        }, {
            "name": "Bò sốt nấm",
            "price": 280000,
            "image": "https://res.cloudinary.com/durpn2bki/image/upload/v1765900392/bosotnam_ijytpv.jpg",
            "category_id": 2
        }, {
            "name": "Thịt heo xào sả ớt",
            "price": 140000,
            "image": "https://res.cloudinary.com/durpn2bki/image/upload/v1765901079/thitheoxaoxaot_sm8hyh.jpg",
            "category_id": 3
        }, {
            "name": "Chả giò ",
            "price": 180000,
            "image": "https://res.cloudinary.com/durpn2bki/image/upload/v1765901079/chagio_getqhf.jpg",
            "category_id": 3
        }, {
            "name": "Thịt heo phô mai",
            "price": 190000,
            "image": "https://res.cloudinary.com/durpn2bki/image/upload/v1765901079/thitheophomai_lrelmv.webp",
            "category_id": 3
        }, {
            "name": "Thịt heo chiên giòn",
            "price": 180000,
            "image": "https://res.cloudinary.com/durpn2bki/image/upload/v1765901081/thitheochienxu_g1e1kv.jpg",
            "category_id": 3
        }, {
            "name": "Thịt heo luộc chắm mắm tôm",
            "price": 150000,
            "image": "https://res.cloudinary.com/durpn2bki/image/upload/v1765901080/thitheoluocmamton_adcoik.jpg",
            "category_id": 3
        }, {
            "name": "Thịt heo nướng mật ong",
            "price": 180000,
            "image": "https://res.cloudinary.com/durpn2bki/image/upload/v1765901092/thitheonuongmatong_p0a5gb.jpg",
            "category_id": 3
        }, {
            "name": "Thịt heo quay giòn",
            "price": 190000,
            "image": "https://res.cloudinary.com/durpn2bki/image/upload/v1765901093/thitheoquay_iyuu9e.jpg",
            "category_id": 3
        }, {
            "name": "Sườn xào chua ngọt",
            "price": 170000,
            "image": "https://res.cloudinary.com/durpn2bki/image/upload/v1765901093/suonxaochuangot_ufnafb.jpg",
            "category_id": 3
        }, {
            "name": "Thịt heo rang muối",
            "price": 160000,
            "image": "https://res.cloudinary.com/durpn2bki/image/upload/v1765901095/thitheorangchaycanh_cydy2x.jpg",
            "category_id": 3
        }, {
            "name": "Thịt kho tàu",
            "price": 150000,
            "image": "https://res.cloudinary.com/durpn2bki/image/upload/v1765901094/thitkhotau_oxtnb6.jpg",
            "category_id": 3
        }, {
            "name": "Kem vani",
            "price": 40000,
            "image": "https://res.cloudinary.com/durpn2bki/image/upload/v1765901556/kemvani_mggedf.jpg",
            "category_id": 4
        }, {
            "name": "Chè Thái",
            "price": 50000,
            "image": "https://res.cloudinary.com/durpn2bki/image/upload/v1765901577/Ch%C3%A8_o2nugc.jpg",
            "category_id": 4
        }, {
            "name": "Bánh mousse socola",
            "price": 50000,
            "image": "https://res.cloudinary.com/durpn2bki/image/upload/v1765901578/banhmoussesocola_eacbr7.jpg",
            "category_id": 4
        }, {
            "name": "Bánh su kem",
            "price": 40000,
            "image": "https://res.cloudinary.com/durpn2bki/image/upload/v1765901578/B%C3%A1nh_su_kem_y7snjz.jpg",
            "category_id": 4
        }, {
            "name": "Trái cây",
            "price": 150000,
            "image": "https://res.cloudinary.com/durpn2bki/image/upload/v1765901580/traicay_vgilyl.jpg",
            "category_id": 4
        }, {
            "name": "Thạch rau câu",
            "price": 40000,
            "image": "https://res.cloudinary.com/durpn2bki/image/upload/v1765901579/thachraucau_he7aw9.jpg",
            "category_id": 4
        }, {
            "name": "Cheese cake",
            "price": 35000,
            "image": "https://res.cloudinary.com/durpn2bki/image/upload/v1765901583/chessecake_an90yo.jpg",
            "category_id": 4
        }, {
            "name": "Panna cotta",
            "price": 45000,
            "image": "https://res.cloudinary.com/durpn2bki/image/upload/v1765901584/panacotta_nmqzxg.jpg",
            "category_id": 4
        }, {
            "name": "Tiramisu",
            "price": 50000,
            "image": "https://res.cloudinary.com/durpn2bki/image/upload/v1765901584/tiramisu_vjepin.jpg",
            "category_id": 4
        }, {
            "name": "Bánh flan",
            "price": 55000,
            "image": "https://res.cloudinary.com/durpn2bki/image/upload/v1765901586/banhflan_rjca3h.png",
            "category_id": 4
        }, {
            "name": "Strong bow",
            "price": 12000,
            "image": "https://res.cloudinary.com/durpn2bki/image/upload/v1765899369/strongbow_cw2wgb.jpg",
            "category_id": 5
        }, {
            "name": "Bia Heniken",
            "price": 15000,
            "image": "https://res.cloudinary.com/durpn2bki/image/upload/v1765899369/heniken_z2ytr1.jpg",
            "category_id": 5
        }, {
            "name": "Bia Sài Gòn",
            "price": 15000,
            "image": "https://res.cloudinary.com/durpn2bki/image/upload/v1765899369/saigon_tn2ill.jpg",
            "category_id": 5
        }, {
            "name": "Coca cola",
            "price": 10000,
            "image": "https://res.cloudinary.com/durpn2bki/image/upload/v1765899371/coca_dfuh79.webp",
            "category_id": 5
        }, {
            "name": "Bò húc",
            "price": 12000,
            "image": "https://res.cloudinary.com/durpn2bki/image/upload/v1765899370/bohuc_ezm4xq.jpg",
            "category_id": 5
        }, {
            "name": "Sprite",
            "price": 10000,
            "image": "https://res.cloudinary.com/durpn2bki/image/upload/v1765899370/sprite_oderig.jpg",
            "category_id": 5
        }, {
            "name": "Bia Huda",
            "price": 15000,
            "image": "https://res.cloudinary.com/durpn2bki/image/upload/v1765899370/huda_svdamr.jpg",
            "category_id": 5
        }, {
            "name": "Sting dâu",
            "price": 12000,
            "image": "https://res.cloudinary.com/durpn2bki/image/upload/v1765899370/sting_mlxfjg.jpg",
            "category_id": 5
        }, {
            "name": "Nước suối",
            "price": 8000,
            "image": "https://res.cloudinary.com/durpn2bki/image/upload/v1765899370/aquafina_hcu97j.jpg",
            "category_id": 5
        }, {
            "name": "Pepsi",
            "price": 10000,
            "image": "https://res.cloudinary.com/durpn2bki/image/upload/v1765899371/pepsi_gpbd2c.jpg",
            "category_id": 5
        }, {
            "name": "Sá xị",
            "price": 10000,
            "image": "https://res.cloudinary.com/durpn2bki/image/upload/v1765899370/xaxi_f26ssj.jpg",
            "category_id": 5
        }, ]

        for f in foods:
            foo = Food(**f)
            db.session.add(foo)

        db.session.commit()