import os
import io
import datetime
from io import BytesIO
from flask import Flask, render_template, url_for, flash, redirect, session, request
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from PIL import Image as PILImage
from wtforms import StringField, PasswordField, SubmitField, validators, ValidationError, DecimalField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp
from forex_python.converter import CurrencyRates
from config import COUNTRIES, config, db
from datetime import datetime
from wtforms import SelectField, StringField, PasswordField, SubmitField, validators, ValidationError, DecimalField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp
from forex_python.converter import CurrencyRates
from config import COUNTRIES
from datetime import datetime
from models import User

class BankForm(FlaskForm):
    amount = DecimalField('Amount', validators=[DataRequired()])
    currency = SelectField('Currency', choices=[('USD', 'US Dollar'), ('EUR', 'Euro'), ('GBP', 'British Pound')], validators=[DataRequired()])
    action = SelectField('Action', choices=[('deposit', 'Deposit'), ('withdraw', 'Withdraw'), ('trade', 'Trade'), ('transfer', 'Transfer')], validators=[DataRequired()])
    submit = SubmitField('Submit')

    def convert_currency_to_usd(self, amount, currency):
        c = CurrencyRates()
        return c.convert(currency, 'USD', amount)

    def convert_usd_to_selected_currency(self, amount, currency):
        c = CurrencyRates()
        return c.convert('USD', currency, amount)
    
class DepositForm(FlaskForm):
    NumberRange = min=50.00; max=1000.00;
    amount = DecimalField('Amount', validators=[
        DataRequired(message="Please enter an amount."),
        NumberRange(message="The amount must be positive.")
    ])
    submit = SubmitField('Deposit') 
    
class WithdrawForm(FlaskForm):
    NumberRange = min=50.00; max=1000.00;
    amount = DecimalField('Amount', validators=[
        DataRequired(message="Please enter an amount."),
        NumberRange(message="The amount must be positive.")
    ])
    submit = SubmitField('Withdraw')  
    
class DonateForm(FlaskForm):
    NumberRange = min=50.00; max=1000.00; value=0;
    amount = DecimalField('Amount', validators=[
        DataRequired(message="Please enter an amount."),
        NumberRange(message="The amount must be positive.")
    ])
    submit = SubmitField('Donate')
        
class TransferForm(FlaskForm):
    NumberRange = min=50.00; max=1000.00; value=0;
    amount = DecimalField('Amount', validators=[
        DataRequired(message="Please enter an amount."),
        NumberRange(message="The amount must be positive.")
    ])
    submit = SubmitField('Transfer')

class ChequeDepositForm(FlaskForm):
    chequeNumber = StringField('Cheque Number', validators=[DataRequired(), Regexp('^\d{4}$', message='Cheque number must be 4 digits.')])
    branchNumber = StringField('Branch Number', validators=[DataRequired(), Regexp('^\d{5}$', message='Branch number must be 5 digits.')])
    institutionNumber = StringField('Institution Number', validators=[DataRequired(), Regexp('^\d{3}$', message='Institution number must be 3 digits.')])
    designationNumber = StringField('Designation Number', validators=[DataRequired(), Regexp('^\d{4}$', message='Designation number must be 4 digits.')])
    accountNumber = StringField('Account Number', validators=[DataRequired(), Regexp('^\d{7}$', message='Account number must be 7 digits.')])
    issuer_bank_name = StringField('Issuer Bank', validators=[DataRequired(), Length(max=100)])

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email is already in use.')

class LoginForm(FlaskForm):
    username = StringField('Username')
    email = StringField('Email')
    password = PasswordField('Password', validators=[validators.DataRequired()])

    def validate(self):
        if not super(Log, self).validate():
            return False

        if not self.username.data and not self.email.data:
            msg = 'Either username or email is required.'
            self.username.errors.append(msg)
            self.email.errors.append(msg)
            return False

        return True

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[validators.DataRequired()])#can you base this data required on password from the self.user.database.password 
    new_password = PasswordField('New Password', validators=[
        validators.DataRequired(),#can you define validators for the password field
        validators.EqualTo('confirm', message='Passwords must match.')
    ])
    confirm = PasswordField('Repeat Password', validators=[validators.DataRequired()])
    
class notEditable(FlaskForm):
    fullName = StringField('Full Name', render_kw={'readonly': True})
    dob = StringField('Date of Birth', render_kw={'readonly': True})
    firstName = StringField('First Name', render_kw={'readonly': True})    
    lastName = StringField('Last Name', render_kw={'readonly': True})
    day = StringField('Day', render_kw={'readonly': True})
    month = StringField('Month', render_kw={'readonly': True})
    year = StringField('Year', render_kw={'readonly': True})
        

class Editable(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])    
    username = StringField('Username', validators=[DataRequired()])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=10)])

class Location(FlaskForm):
    street_address = StringField('Street Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    country = StringField('Country', validators=[DataRequired()])
    zip_code = StringField('Zip Code', validators=[DataRequired()])
    password = PasswordField('New Password')
    confirm_password = PasswordField('Confirm New Password', validators=[EqualTo('password')])
    submit = SubmitField('UpdateLocation')

class ImageForm(FlaskForm):
    image = FileField('Image', validators=[FileAllowed(['jpg', 'png', 'gif'])])
    category = SelectField('Category', choices=[('profile', 'Profile Picture'), ('cover', 'Cover Photo')])
    submit = SubmitField('Upload Image')

    def allowed_img(file_stream, allowed_types):
        try:
            img = PILImage.open(file_stream)
            img.verify()
            if img.format.lower() in allowed_types:
                return True
        except (IOError, SyntaxError):
             return False

class CountryForm(FlaskForm):
    country = SelectField('Country', choices=[(country, details['name']) for country, details in COUNTRIES.items()])
    submit = SubmitField('Submit')

class PhoneForm(FlaskForm):
    phone_number = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=10)])
    submit = SubmitField('Submit')

class EmailForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')
    
class verificationCode(FlaskForm):
    code = StringField('Verification Code', validators=[DataRequired(), Length(min=6, max=6)])
    submit = SubmitField('Verify Code')

class PhoneVerificationForm(FlaskForm):
    phone_number = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=10)])
    submit = SubmitField('Verify Phone Number')
    
class EmailVerificationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Verify Email')
    
class PasswordResetForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
    
class codeResend(FlaskForm):
    submit = SubmitField('Resend Code')

