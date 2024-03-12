from Vault78.src import db
from flask_sqlalchemy import SQLAlchemy
from Vault78.src import config
from config import COUNTRIES  
from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect, session
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators, ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp
from flask_bcrypt import Bcrypt
from PIL import Image as PILImage
import io
import os

from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    hashed_password = db.Column(db.String(128), nullable=False)
    username = db.Column(db.String(80), unique=True)
    first_name = StringField('First Name', db.String(120))
    last_name = StringField('Last Name', db.String(120))
    fullNAme = first_name + last_name
    street_address = StringField('Street Address')
    city = StringField('City')
    state = StringField('State')
    zip_code = StringField('Zip')
    country = StringField('Country')
    country_code = StringField('Country Code')
    location = street_address +city + state + country + zip_code
    day = datetime.strftime('%d')
    month = datetime.strftime('%m')
    year = datetime.strftime('%Y')
    dob = day.strftime('%d') + month.strftime('%m') + year.strftime('%Y')
    today = datetime.now()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    phone_number = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=10)])
    phone_number_verification_code = db.Column(db.String(6), nullable=True)
    phone_number_verified = db.Column(db.Boolean, default=False, nullable=False)
    email_verification_code = db.Column(db.String(6), nullable=True)
    email_verified = db.Column(db.Boolean, default=False, nullable=False)

    def set_password(self, password):
        self.hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(hashed_password, password):
        return bcrypt.check_password_hash(hashed_password, password)

    def display_user_shown(self):
        fullname = f"{self.first_name} {self.last_name}"
        location = f"{self.street_address}, {self.city}, {self.state}, {self.country}, {self.zip_code}"
        age = datetime.now().year - self.dob.year - ((datetime.now().month, datetime.now().day) < (self.dob.month, self.dob.day))
        return {
            "fullname": fullname,
            "location": location,
            "age": age
        }
    
class BankAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    account_balance = db.Column(db.Float, nullable=False, default=0.0)
    account_type = db.Column(db.String(50), nullable=False)
    transactions = db.Column(db.Text)
    user = db.relationship('User', backref='bank_account')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255))
    bank_account_id = db.Column(db.Integer, db.ForeignKey('bank_account.id'), nullable=True)
    foundation_id = db.Column(db.Integer, db.ForeignKey('foundation.id'), nullable=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    bank_account = db.relationship('BankAccount', backref='transactions')
    foundation = db.relationship('Foundation', backref='transactions')

class TransactionHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transaction.id'), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    modified_timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    
class Foundation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    bank_name = db.Column(db.String(100), nullable=False)
    account_number = db.Column(db.String(50), nullable=False)
    routing_number = db.Column(db.String(50), nullable=True)

class Image(db.Model):
        userID = db.Column(db.Integer, primary_key=True)
        filename = db.Column(db.String(100), nullable=False)
        data = db.Column(db.LargeBinary, nullable=False)
        mime_type = db.Column(db.String(50), nullable=False)
        category = db.Column(db.String(50), nullable=False)
        timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

        def __repr__(self):
            return f"Image('{self.filename}', '{self.mime_type}', '{self.category}')"

        def allowed_img(file):
            try:
                img = PILImage.open(io.BytesIO(img.read()))
                img.verify()
                img.seek(0)
                return img.content_type in ALLOWED_TYPES
            except (IOError, SyntaxError):
                return False

    