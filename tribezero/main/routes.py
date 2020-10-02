from flask import render_template, request, Blueprint, url_for, redirect
from flask_login import current_user
import requests
from tribezero.models import Post, CompanyAddress, Shop
from tribezero.config import Config
from tribezero import db

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    return render_template('home.html', title='Home')


@main.route("/about")
def about():
    return render_template('about.html', title='About')


@main.route("/welcome")
def welcome():
    return render_template('welcome.html', title='Welcome!')


@main.route("/map")
def sellers_map():
    key = Config.GOOGLE_MAPS_API_KEY

    shops = Shop.query.join(CompanyAddress, Shop.id == CompanyAddress.shop_id)\
        .add_columns(Shop.name, CompanyAddress.company_coordinates_lat, CompanyAddress.company_coordinates_lon,\
                     CompanyAddress.shop_id, Shop.id, Shop.shop_categories, Shop.description)\
        .filter(Shop.id == CompanyAddress.shop_id)
    return render_template('map.html', title='Map', key=key, shops=shops)


@main.route("/blog")
def blog():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('blog.html', posts=posts)


