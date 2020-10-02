from datetime import datetime
from sqlalchemy import func
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import current_user, login_required
from tribezero import db
from tribezero.users.forms import CreateShopForm
from tribezero.models import Shop, CompanyAddress, Contact
from tribezero.config import Config
import requests


user_shops = Blueprint('shops', __name__)


@user_shops.route("/open_shop", methods=['GET', 'POST'])
@login_required
def open_shop():
    form = CreateShopForm(company_country="IE")

    if current_user.shop:
        flash('Sorry but you already have a shop. Only one per account.', 'warning')
        return redirect(url_for('main.home'))

    if form.validate_on_submit():
        shop = Shop(name=form.shop_name.data,
                    created=datetime.utcnow(),
                    owner=current_user,
                    shop_categories=form.shop_categories.data
                    )

        key = Config.GOOGLE_MAPS_API_KEY
        google_maps_api_url = "https://maps.googleapis.com/maps/api/geocode/json?"
        address = f"address={form.company_street_line1.data},{form.company_street_line2.data},{form.company_city.data}," \
            f"{form.company_region.data},{form.company_zip_code.data},{dict(form.company_country.choices).get(form.company_country.data)}"
        coordinates_response = requests.get(google_maps_api_url + address + "&key=" + key).json()
        response = coordinates_response["results"][0]

        company_address = CompanyAddress(company_name=form.company_name.data,
                                         company_street_line1=form.company_street_line1.data,
                                         company_street_line2=form.company_street_line2.data,
                                         company_city=form.company_city.data,
                                         company_country=form.company_country.data,
                                         company_region=form.company_region.data,
                                         company_zip_code=form.company_zip_code.data,
                                         company_building_number=form.company_building_number.data,
                                         company_apartment_number=form.company_apartment_number.data,
                                         company_coordinates_lat=response["geometry"]["location"]["lat"],
                                         company_coordinates_lon=response["geometry"]["location"]["lng"],
                                         shop=current_user)

        contact = Contact(email=form.email.data,
                          shop=current_user)

        db.session.add(shop)
        db.session.add(company_address)
        db.session.add(contact)
        db.session.commit()

        flash('Your shop has been opened!', 'success')
        return redirect(url_for('main.home'))
    return render_template('open_shop.html', title='Open Shop', form=form)


@user_shops.route("/shop/<string:name>")
def shop(name):
    shop_id = Shop.query.filter(func.lower(Shop.name) == func.lower(name)).first().id
    shop_info = Shop.query.get_or_404(shop_id)
    return render_template('shop.html', title=name, shop_info=shop_info)


@user_shops.route("/shops")
def shops():
    page = request.args.get('page', 1, type=int)
    shops = Shop.query.order_by(Shop.name.asc()).paginate(page=page, per_page=10)
    return render_template('shops.html', title='Shops', shops=shops)


@user_shops.route("/shop_manager")
@login_required
def shop_manager():
    users_shop = Shop.query.filter_by(owner=current_user).first().name
    return render_template('shop_manager.html', title=users_shop, users_shop=users_shop)


