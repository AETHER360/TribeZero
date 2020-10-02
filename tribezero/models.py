from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from tribezero import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    shop = db.relationship('Shop', backref='owner', lazy=True)
    transaction = db.relationship('TransactionHistory', backref='owner', lazy=True)
    account_status = db.relationship('AccountStatus', backref='owner', lazy=True)
    account = db.relationship('Account', backref='owner', lazy=True)
    contact = db.relationship('Contact', backref='owner', lazy=True)

    def get_reset_token(self, expires_seconds=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_seconds)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


class Shop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    image_file = db.Column(db.String(20), nullable=False, default='default_shop.jpg')
    total_orders = db.Column(db.Integer, default=0)
    total_sales = db.Column(db.Integer, default=0)
    cancelled_sales = db.Column(db.Integer, default=0)
    active_listings = db.Column(db.Integer, default=0)
    inactive_listings = db.Column(db.Integer, default=0)
    cover_image = db.Column(db.String(20), nullable=False, default='default_cover.jpg')
    description = db.Column(db.String(2000))
    response_rate = db.Column(db.Float(precision=2))
    times_favorited = db.Column(db.Integer, default=0)
    times_viewed = db.Column(db.Integer, default=0)
    expired_listings = db.Column(db.Integer, default=0)
    shop_categories = db.Column(db.String(30), default='None')
    listing = db.relationship('Listing', backref='shop', lazy=True)
    financial = db.relationship('Financial', backref='shop', lazy=True)
    company_address = db.relationship('CompanyAddress', backref='shop', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Shop('{self.name}', '{self.id}','{self.user_id}')"


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class Financial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vat_id = db.Column(db.String(20))
    taxpayer_id = db.Column(db.String(20))
    revenue = db.Column(db.Integer, default=0)
    paypal_account = db.Column(db.String(120), unique=True, default=None)
    amount_due = db.Column(db.Integer, default=0)
    shop_id = db.Column(db.Integer, db.ForeignKey('shop.id'), nullable=False)


class CompanyAddress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(20), unique=True)
    company_street_line1 = db.Column(db.String(500), nullable=False)
    company_street_line2 = db.Column(db.String(500), nullable=False)
    company_city = db.Column(db.String(50), nullable=False)
    company_country = db.Column(db.String(2), nullable=False)
    company_zip_code = db.Column(db.String(10), nullable=False)
    company_building_number = db.Column(db.String(6))
    company_apartment_number = db.Column(db.String(6))
    company_region = db.Column(db.String(50), nullable=False)
    company_coordinates_lat = db.Column(db.Float())
    company_coordinates_lon = db.Column(db.Float())
    shop_id = db.Column(db.Integer, db.ForeignKey('shop.id'), nullable=False)


class BillingAddress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    billing_street_line1 = db.Column(db.String(500), nullable=False)
    billing_street_line2 = db.Column(db.String(500), nullable=False)
    billing_city = db.Column(db.String(50), nullable=False)
    billing_country = db.Column(db.String(2), nullable=False)
    billing_postal_code = db.Column(db.String(10), nullable=False)
    billing_building_number = db.Column(db.String(6))
    billing_apartment_number = db.Column(db.String(6))
    billing_region = db.Column(db.String(50), nullable=False)
    shop_id = db.Column(db.Integer, db.ForeignKey('shop.id'), nullable=False)


class TransactionHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    purchases = db.Column(db.Integer, default=0)
    orders = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class AccountStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email_confirmed = db.Column(db.Boolean(create_constraint=True, name=None), default=False)
    account_frozen = db.Column(db.Boolean(create_constraint=True, name=None), default=False)
    account_closed = db.Column(db.Boolean(create_constraint=True, name=None), default=False)
    setup_complete = db.Column(db.Boolean(create_constraint=True, name=None), default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(256), nullable=False)
    last_name = db.Column(db.String(256), nullable=False)
    middle_name = db.Column(db.String(256))
    joined = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    last_access = db.Column(db.DateTime)
    language = db.Column(db.String(2), default="en")
    region = db.Column(db.String(2), default="ireland")
    currency = db.Column(db.String(3), default="EUR")
    birthday = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class Listing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    tags = db.Column(db.JSON)
    images = db.Column(db.JSON, default=lambda: {"image1": "default_listing.jpg"})
    shop_id = db.Column(db.Integer, db.ForeignKey('shop.id'), nullable=False)

