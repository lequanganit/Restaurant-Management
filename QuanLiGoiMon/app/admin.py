from flask_admin import Admin, AdminIndexView
from markupsafe import Markup
from app import app, db
from flask_admin.contrib.sqla import ModelView
from app.models import User, UserRole, Category, Food, ROLES
from flask_admin import BaseView, expose
from flask_login import current_user, logout_user
from flask import redirect, abort
from wtforms import PasswordField
from flask_admin.contrib.sqla.filters import FilterEqual
from wtforms.validators import NumberRange, Regexp

class AdminAuthMixin:
    def is_accessible(self) -> bool:
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN
    # neu khong phai admin thi tra ve trang 403
    def inaccessible_callback(self, *args, **kwargs):
        if not current_user.is_authenticated:
            return redirect('/login')
        return abort(403)

class MyAdminIndexView(AdminAuthMixin, AdminIndexView):
    pass

class AdminView(AdminAuthMixin, ModelView):
    pass

class UserView(AdminView):
    column_list = ['avatar', 'name', 'username', 'user_role']
    column_labels = {
        'avatar': 'Ảnh đại diện',
        'name': 'Tên',
        'username': 'Tên người dùng',
        'user_role': 'Vai trò'
    }
    column_sortable_list = ['name', 'username', 'user_role']
    column_searchable_list = ['name', 'username']
    column_filters = ['user_role']
    can_export = True
    edit_modal = True
    column_editable_list = ['name', 'username']
    page_size = 8
    # v: value, c: context, m: model, p: property
    column_formatters = {
        'avatar': lambda v, c, m, p: Markup(f'<img src="{m.avatar}" width="35" height="35" class="rounded-circle">'),
        'user_role': lambda v, c, m, p: ROLES.get(m.user_role, {}).get("name_vn"),
    }
    # khong hien thi password
    form_overrides = {
        'password': PasswordField
    }

class CategoryView(AdminView):
    column_labels = {
        'name': 'Tên danh mục',
        'active': 'Hoạt động'
    }
    column_sortable_list = ['name']
    column_searchable_list = ['name']
    column_filters = ['name','active']
    can_export = True
    edit_modal = True
    column_editable_list = ['name', 'active']
    page_size = 10

class FoodView(AdminView):
    column_list = ['image', 'name', 'price', 'category', 'active']
    column_labels = {
        'image': 'Hình ảnh',
        'name': 'Tên món ăn',
        'price': 'Giá',
        'category': 'Danh mục',
        'active': 'Hoạt động'
    }
    column_sortable_list = ['name', 'price']
    column_searchable_list = ['name']
    # filter theo gia va ten danh muc
    column_filters = ['price', FilterEqual(Category.name,'Danh mục'), 'active']
    can_export = True
    edit_modal = True
    column_editable_list = ['name', 'price', 'active']
    page_size = 6
    column_formatters = {
        'image': lambda v, c, m, p: Markup(f'<img src="{m.image}" width="50" height="50">'),
        'price': lambda v, c, m, p: f'{int(m.price):,} VNĐ'
    }
    form_excluded_columns = ['food_orders']

    # gia lon hon 0
    form_args = {
        'price': {
            'validators': [NumberRange(min=1, message="Giá phải lớn hơn 0")]
        },
        'name': {
            'validators': [
                Regexp(r'^(?!\d+$).*$', message="Tên món ăn không được là số")]
        }
    }

class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/login')
    
    def is_accessible(self) -> bool:
        return current_user.is_authenticated

admin = Admin(app=app, name='Quản lý gọi món Admin', index_view=MyAdminIndexView())
admin.add_view(UserView(User, db.session, name='Người dùng'))
admin.add_view(CategoryView(Category, db.session, name='Danh mục món ăn'))
admin.add_view(FoodView(Food, db.session, name='Món ăn'))
admin.add_view(LogoutView(name='Đăng xuất'))