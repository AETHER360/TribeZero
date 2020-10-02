import json
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
from flask_login import current_user
from tribezero.models import User, Shop


with open('tribezero/static/countries.json', 'r', encoding='utf-8') as f:
    countries_list_dicts = json.load(f)
    countries_list = []
    for country in countries_list_dicts:
        countries_list.append((country['code'], country['name']))

with open('tribezero/static/shop_categories.json', 'r', encoding='utf-8') as f:
    shop_categories_dicts = json.load(f)
    categories_list = []
    for category in shop_categories_dicts:
        categories_list.append((category['code'], category['category']))


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=8, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=8), EqualTo('password')])
    submit = SubmitField('Sign Up')


    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('''Unfortunately the tribe already has a member with that username. 
                                     Please choose a different one.''')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('''Unfortunately the tribe already has a member with that e-mail. 
                                     Please choose a different one.''')


class LoginForm(FlaskForm):
    # username = StringField('Username', validators=[DataRequired(), Length(min=8, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=8, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('''Unfortunately the tribe already has a member with that username. 
                                         Please choose a different one.''')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('''Unfortunately the tribe already has a member with that e-mail. 
                                         Please choose a different one.''')


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that e-mail. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), Length(min=8), EqualTo('password')])
    submit = SubmitField('Reset Password')


class CreateShopForm(FlaskForm):
    shop_name = StringField('Shop Name', validators=[DataRequired(), Length(min=4, max=20)])
    shop_categories = SelectField('Shop Category', choices=categories_list, validators=[DataRequired()])
    company_name = StringField('Company Name', validators=[DataRequired(), Length(min=4, max=20)])
    paypal = StringField('PayPal Account', validators=[DataRequired(), Email()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    company_street_line1 = StringField('Street Address Line 1', validators=[DataRequired(), Length(min=5)])
    company_street_line2 = StringField('Street Address Line 2')
    company_city = StringField('City', validators=[DataRequired(), Length(min=2)])
    company_country = SelectField('Country', choices=countries_list, validators=[DataRequired()])
    company_region = StringField('Region', validators=[DataRequired(), Length(min=2)])
    company_zip_code = StringField('Zip Code', validators=[DataRequired(), Length(min=3)])
    company_building_number = StringField('Building Number')
    company_apartment_number = StringField('Apartment Number')
    vat_id = StringField('VAT ID Number', validators=[DataRequired(), Length(min=6)])
    taxpayer_id = StringField('Tax Payer ID Number', validators=[DataRequired(), Length(min=6)])
    billing_is_not_company = BooleanField('Billing address is different than the company address.')
    no_vat = BooleanField("I don't have a VAT number.")
    submit = SubmitField('Open Shop')

    def validate_shop_name(self, shop_name):
        shop = Shop.query.filter_by(name=shop_name.data).first()
        if shop:
            raise ValidationError('''Unfortunately the tribe already has a shop with that name. 
                                     Please choose a different one.''')


class CreateShopContinuedForm(FlaskForm):
    billing_street_line1 = StringField('Street Address Line 1', validators=[DataRequired(), Length(min=5, max=100)])
    billing_street_line2 = StringField('Street Address Line 2')
    billing_city = StringField('City', validators=[DataRequired(), Length(min=1, max=100)])
    billing_country = SelectField('Country', choices=countries_list, validators=[DataRequired()])
    billing_region = StringField('Region', validators=[DataRequired(), Length(min=1, max=100)])
    billing_zip_code = StringField('Zip Code', validators=[DataRequired()])
    billing_building_number = StringField('Building Number', validators=[Optional()])
    billing_apartment_number = StringField('Apartment Number', validators=[Optional()])


