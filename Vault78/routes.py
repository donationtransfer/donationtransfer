import os
import json
import mailbox
import Vault78.src
import io, pyodbc, mysql.connector
from email.policy import EmailPolicy
from mysql.connector import connect
from mysql.connector import MySQLConnection, Error
from flask_sqlalchemy import SQLAlchemy, MSQL
from flask_migrate import Migrate
from Vault78.src import forms, models, config, app, db, bcrypt
from .forms import Location, RegistrationForm, LoginForm, ChangePasswordForm, Editable, ImageForm, notEditable, CountryForm, notEditable, verificationCode, EmailVerificationForm, PhoneVerificationForm, ChequeDepositForm, PasswordResetForm, BankForm, DepositForm, WithdrawForm, DepositForm, TransferForm, DonateForm
from .models import User, Image, BankAccount, BankAccount, Transaction, Foundation
from .config import Config 
from flask import render_template, url_for, flash, redirect
from flask import Flask, render_template, redirect, url_for, flash, session, request, send_file, abort
from werkzeug.utils import secure_filename, send_file, redirect, url_for, flash, session, request, abort, render_template, send_file, redirect, url_for, flash, session, request, abort, render_template 
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from flask_bcrypt import Bcrypt
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_wtf.file import FileField, FileAllowed, FileRequired
from PIL import Image, ImageDraw
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime
from json import loads, dumps, JSONEncoder, JSONDecoder, JSONDecodeError
from mailbox import Mailbox, Message
from io import BytesIO

app = Flask(__name__)
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
db.init_app(app)

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')
    
@app.route('./about')
def about():
    return render_template('about.html')

@app.route('/account', methods=['GET', 'POST'])
def account():
    if 'authenticated' not in session or not session['authenticated']:
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('home'))

    user_id = session.get('user_id')
    user = User.query.get(user_id)

    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('account'))

    return render_template('account.html', title='Account', user=user)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(email=form.email.data, hashed_password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('home.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter((User.username == form.username.data) | (User.email == form.email.data)).first()
        if user:
            password_matched = bcrypt.checkpw(form.password.data.encode('utf-8'), user.password_hash.encode('utf-8'))
            if password_matched:
                session['authenticated'] = True
                session['user_id'] = user.id
                flash('You have been successfully logged in!')
                return redirect(url_for('account'))
            else:
                flash('Login Failed. Please check username and password')
        else:
            flash('User not found. Please check your login details')
    return render_template('home.html', title='Login', form=form)

@app.route('/change-password', methods=['POST'])
def change_password():
    form = ChangePasswordForm()

    if form.validate_on_submit():
        user_id = session.get('user_id')
        user = User.query.get(user_id)

        if user:
            old_password = form.old_password.data
            new_password = form.new_password.data

            if bcrypt.checkpw(old_password.encode('utf-8'), user.password_hash.encode('utf-8')):
                hashed_new_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
                user.password_hash = hashed_new_password.decode('utf-8')
                db.session.commit()
                flash('Password updated successfully.', 'success')
                return redirect(url_for('/account'))
            else:
                flash('Old password is incorrect.', 'danger')
        else:
            flash('User not found.', 'danger')

    return redirect(url_for('home'))

@app.route('/country', methods=['GET', 'POST'])
def select_country():
    form = CountryForm()
    if form.validate_on_submit():
        selected_country = form.country.data
        flash(f'Country {selected_country} selected.', 'success')
        return redirect(url_for('home/country'))

@app.route('/logout')
def logout():
    session.pop('authenticated', None)
    session.pop('user_id', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))

@app.route('/POSTlocation', methods=['GET', 'POST'])
def updateInfo():
    if 'authenticated' not in session or not session['authenticated']:
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('home'))

    user_id = session.get('user_id')
    user = User.query.get(user_id)

    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('account'))

    form = Location(obj=user)

    if request.method == 'POST' and form.validate_on_submit():
        user.street_address = form.street_address.data
        user.city = form.city.data
        user.state = form.state.data
        user.zip_code = form.zip_code.data
        user.country = form.country.data
        user.location = form.location.data


        db.session.commit()
        flash('Your profile information has been updated successfully!', 'success')
        return redirect(url_for('account'))

    return redirect(url_for('home'))


@app.route('/GETlocation', methods=['GET', 'POST'])
def getInfo():

    if 'authenticated' not in session or not session['authenticated']:
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('home'))

    user = User.query.get(User.id == form.id.data)
    user_id = session.add(user)
    form = Location(obj=user)

    if form.validate_on_submit():
        user.street_address = form.street_address.data
        user.city = form.city.data
        user.state = form.state.data
        user.zip_code = form.zip_code.data
        user.country = form.country.data
        user.location = form.location.data

        db.session.commit()
        flash('Your profile informations have been updated successfully!')
        return redirect(url_for('/account'))

    elif request.method == 'GET':
        form.username.data = user.username
        form.fullName = user.fullName
        form.location = user.location
        form.age = user.age

    return render_template('home.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_image():
    form = ImageForm()
    if form.validate_on_submit():
        image_file = form.image.data
        category = form.category.data
        try:
            pil_image = Image.open(image_file)
        except IOError:
            flash('Invalid image file!', 'danger')
            return redirect(url_for('account'))

        if pil_image.format not in ['JPEG', 'PNG', 'GIF']:
            flash('Image format not supported!', 'danger')
            return redirect(url_for('account'))

        output_size = (500, 500)
        pil_image.thumbnail(output_size, Image.ANTIALIAS)
        img_byte_arr = io.BytesIO()
        pil_image.save(img_byte_arr, format=pil_image.format)
        img_byte_arr = img_byte_arr.getvalue()

        mime_type = 'image/jpeg' if pil_image.format == 'JPEG' else 'image/png'

        new_image = Image(
            filename=secure_filename(image_file.filename),
            data=img_byte_arr,
            mime_type=mime_type,
            category=category
        )
        db.session.add(new_image)
        db.session.commit()

        flash('Your image has been uploaded and processed!', 'success')
        return redirect(url_for('account'))

    return render_template('account.html', title='Upload Image', form=form)
    
@app.route('/image/<int:image_id>')
def get_image(image_id):
    image = Image.query.get_or_404(image_id)
    return send_file(
        io.BytesIO(image.data),
        mimetype=image.mime_type,
        as_attachment=True,
        attachment_filename=image.filename
    )

@app.route('/verify_email', methods=['GET', 'POST'])
def verify_email():
    form = EmailVerificationForm()
    if form.validate_on_submit():
        email = form.email.data
        # Here, integrate with your service to send a verification code to the email
        verification_code = send_verification_code(email)
        
        # Store the verification code in session for later verification
        session['verification_code'] = verification_code
        session['email_to_verify'] = email
        
        return redirect(url_for('confirm_email_code'))
    return render_template('verify_email.html', form=form)

@app.route('/confirm_email_code', methods=['GET', 'POST'])
def confirm_email_code():
    form = VerificationCodeForm()
    if form.validate_on_submit():
        user_code = form.verification_code.data
        verification_code = session.get('verification_code', '')
        
        if user_code == verification_code:
            # Verification successful, proceed with your logic, e.g., update user status
            flash('Email verified successfully!', 'success')
            session.pop('verification_code', None)
            session.pop('email_to_verify', None)
            return redirect(url_for('home'))
        else:
            flash('Invalid verification code. Please try again.', 'danger')
            
    return render_template('confirm_verification_code.html', form=form)

@app.route('/verify_phone', methods=['GET', 'POST'])
def verify_phone():
    form = PhoneVerificationForm()
    if form.validate_on_submit():
        phone_number = form.phone_number.data
        # Here, integrate with your service to send a verification code to the phone number
        verification_code = send_verification_code(phone_number)
        
        # Store the verification code in session for later verification
        session['verification_code'] = verification_code
        session['phone_to_verify'] = phone_number
        
        return redirect(url_for('confirm_phone_code'))
    return render_template('verify_phone.html', form=form)

@app.route('/confirm_phone_code', methods=['GET', 'POST'])
def confirm_phone_code():
    form = VerificationCodeForm()
    if form.validate_on_submit():
        user_code = form.verification_code.data
        verification_code = session.get('verification_code', '')
        
        if user_code == verification_code:
            # Verification successful, proceed with your logic, e.g., update user status
            flash('Phone number verified successfully!', 'success')
            session.pop('verification_code', None)
            session.pop('phone_to_verify', None)
            return redirect(url_for('home'))
        else:
            flash('Invalid verification code. Please try again.', 'danger')
            
    return render_template('confirm_verification_code.html', form=form) 

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    form = PasswordResetForm()
    if form.validate_on_submit():
        email = EmailPolicy.data
        Mailbox(User.email)
        flash('Password reset link sent to your email.', 'success')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password_with_token(token):
    # Here, validate the token and proceed with password reset
    return render_template('reset_password_with_token.html')
    
@app.route('/bank', methods=['GET', 'POST'])
def bank():
    form = BankForm()
    if form.validate_on_submit():
        amount = form.amount.data
        currency = form.currency.data
        action = form.action.data
        # Convert to USD if necessary
        if currency != 'USD':
            if action in ['deposit', 'transfer']:
                amount = form.convert_currency_to_usd(amount, currency)
            elif action in ['withdraw', 'trade']:
                amount = form.convert_usd_to_selected_currency(amount, currency)

        record_transaction(amount, currency, action)
        flash('Transaction recorded.', 'success')
        return redirect(url_for('bank_history'))

    return render_template('bank.html', title='Bank Actions', form=form)

@app.route('/bank_history')
def bank_history():
    # Fetch and display user's bank history
    return render_template('bank_history.html')

@app.route('/cheque_deposit', methods=['GET', 'POST'])
def cheque_deposit():
    form = ChequeDepositForm()
    if form.validate_on_submit():
        # Process cheque deposit
        flash('Cheque deposit processed.', 'success')
        return redirect(url_for('bank_history'))
    return render_template('cheque_deposit.html', form=form)

@app.route('/bank/account')
@login_required
def view_account():
    bank_account = BankAccount.query.filter_by(user_id=current_user.id).first()
    if bank_account:
        return render_template('view_account.html', account=bank_account)
    else:
        flash('Bank account not found.')
        return redirect(url_for('index'))

@app.route('/bank/deposit', methods=['GET', 'POST'])
@login_required
def deposit_money():
    if request.method == 'POST':
        amount = request.form.get('amount', type=float)
        if amount > 0:
            bank_account = BankAccount.query.filter_by(user_id=current_user.id).first()
            if bank_account:
                bank_account.account_balance += amount
                add_transaction(bank_account, amount, "deposit")
                db.session.commit()
                flash('Deposit successful.')
            else:
                flash('Bank account not found.')
        else:
            flash('Invalid deposit amount.')
        return redirect(url_for('view_account'))
    return render_template('deposit_money.html')

@app.route('/bank/withdraw', methods=['GET', 'POST'])
@login_required
def withdraw_money():
    if request.method == 'POST':
        amount = request.form.get('amount', type=float)
        bank_account = BankAccount.query.filter_by(user_id=current_user.id).first()
        if bank_account and amount <= bank_account.account_balance and amount > 0:
            bank_account.account_balance -= amount
            add_transaction(bank_account, amount, "withdraw")
            db.session.commit()
            flash('Withdrawal successful.')
        else:
            flash('Invalid withdrawal amount or insufficient funds.')
        return redirect(url_for('view_account'))
    return render_template('withdraw_money.html')

from datetime import datetime

@app.route('/bank/donate', methods=['GET', 'POST'])
@login_required
def donate_money():
    if request.method == 'POST':
        amount = request.form.get('amount', type=float)
        foundation_id = request.form.get('foundation_id', type=int)  # Ensure you get foundation_id from the form
        bank_account = BankAccount.query.filter_by(user_id=current_user.id).first()
        foundation = Foundation.query.filter_by(id=foundation_id).first()

        if bank_account and foundation and amount <= bank_account.account_balance and amount > 0:
            bank_account.account_balance -= amount
            user_transaction = Transaction(amount=amount, description=f"Donation to {foundation.name}", bank_account_id=bank_account.id)
            db.session.add(user_transaction)

            foundation_transaction = Transaction(amount=amount, description=f"Donation from {current_user.username}", foundation_id=foundation.id)
            db.session.add(foundation_transaction)

            pdf_bytes = BytesIO()
            c = canvas.Canvas(pdf_bytes)
            msgcontent = c.drawString(100, 750, f"Donation Receipt: ${amount} to {foundation.name}")

            c.save()
            pdf_bytes(id).seek(0)

            mail = Mailbox(app)
            msg = Message("Donation Receipt", content=[msgcontent(id)], sender="shurukn@donationtransfer.com", recipients=[current_user.email])
            msg.body = "Thank you for your donation."
            msg.attach("receipt.pdf", "application/pdf", pdf_bytes.read())
            mail.send(msg)            
            db.session.commit()
            flash('Donation successful. Receipt emailed to you.')
        else:
            flash('Invalid donation amount or insufficient funds.')
        return redirect(url_for('view_account'))

    return render_template('donate.html', user_id=current_user.id)


@app.route('/bank/transfer', methods=['GET', 'POST'])
@login_required
def transfer_money():
    if request.method == 'POST':
        target_account_id = request.form.get('target_account_id', type=int)
        amount = request.form.get('amount', type=float)
        source_account = BankAccount.query.filter_by(user_id=current_user.id).first()
        target_account = BankAccount.query.get(target_account_id)
        if source_account and target_account and amount <= source_account.account_balance and amount > 0:
            source_account.account_balance -= amount
            target_account.account_balance += amount
            add_transaction(source_account, amount, "transfer_out", target_account_id=target_account_id)
            add_transaction(target_account, amount, "transfer_in", source_account_id=source_account.id)
            db.session.commit()
            flash('Transfer successful.')
        else:
            flash('Invalid transfer details or insufficient funds.')
        return redirect(url_for('view_account'))
    return render_template('transfer_money.html')

@app.route('/bank/history')
@login_required
def view_transactions():
    bank_account = BankAccount.query.filter_by(user_id=current_user.id).first()
    if bank_account:
        transactions = json.loads(bank_account.transactions or '[]')
        return render_template('history.html', transactions=transactions)
    else:
        flash('Bank account not found.')
        return redirect(url_for('index'))

def add_transaction(bank_account, amount, action, **kwargs):
    transactions = json.loads(bank_account.transactions or '[]')
    transaction = {
        "timestamp": datetime.now().isoformat(),
        "amount": amount,
        "action": action,
        **kwargs
    }
    transactions.append(transaction)
    bank_account.transactions = json.dumps(transactions)



