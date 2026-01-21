# 1. Standard Library Imports
import datetime
import os
import random
# 2. Third-Party Imports
import bcrypt
from dotenv import load_dotenv
from flask import Flask
from flask_mail import Mail, Message
# 3. Local Application Imports
from Database.Connect import Database
from Database.Log import Log
from Database.User import User
from debug import debug
from email import email


load_dotenv()
current_user = None
def create_mail_app():
    app = Flask(__name__)
    app.config.update(
        MAIL_SERVER="smtp.gmail.com",
        MAIL_PORT=587,
        MAIL_USE_TLS=True,
        MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
        MAIL_PASSWORD=os.getenv("MAIL_PASSWORD_APP"),
        MAIL_DEFAULT_SENDER=os.getenv("MAIL_USERNAME"),
    )
    return app

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed.decode()

def generate_otp(length: int = 6) -> str:
    return "".join(str(random.randint(0, 9)) for _ in range(length))

def check_effective_period(start_time: datetime.datetime,
                           expired_minutes: int = 5) -> bool:
    now = datetime.datetime.now()
    expired_time = start_time + datetime.timedelta(minutes=expired_minutes)
    return now <= expired_time

def verify_password(input_password: str, stored_hashed_password: str) -> bool:
    return bcrypt.checkpw(input_password.encode(), stored_hashed_password.encode())

class Auth:
    @staticmethod
    def login():
        global current_user

        email = input("Nhap email: ").strip()
        password = input("Nhap mat khau: ").strip()
        if User.find_by_email(email)["email"] is None:
            print("Email khong ton tai!")
            return False

        if verify_password(password, User.find_by_email(email)["password"]) is False:
            print("Mat khau khong dung!")
            return False

        current_user = User.find_by_email(email)
        print("Dang nhap thanh cong!")
        return True

    @staticmethod
    def logout():
        """
        Logout cho console:
        - Không xử lý current_user
        - Chỉ ghi log nghiệp vụ
        """

        # Ghi log logout
        return True, "Logout thanh cong"

    def changePassword(student):
        old_pass = input("Nhap mat khau cu: ").strip()
        if old_pass != User.find_by_email(current_user["email"])["password"]:
            print("Mat khau cu khong dung!")
            return
        new_pass = input("Nhap mat khau moi: ").strip()
        confirm_pass = input("Nhap lai mat khau moi: ").strip()
        if new_pass != confirm_pass:
            print("Mat khau khong trung khop!")
            return
        User.update_password(current_user["email"], hash_password(new_pass))
        print("Doi mat khau thanh cong!")
        return new_pass

    def reset_password(student):
        new_pass = input("Nhap mat khau moi: ").strip()
        confirm_pass = input("Nhap lai mat khau moi: ").strip()

        if new_pass != confirm_pass:
            print("Mat khau khong trung khop!")
            return

        User.update_password(current_user["email"], hash_password(new_pass))
        print("Dat lai mat khau thanh cong!")
        return new_pass

    def verify_otp(input_otp: str, real_otp: str) -> bool:
        return input_otp == real_otp
    def requestOTP(receiver_email: str) -> str:
        app = create_mail_app()
        mail = Mail(app)

        otp = generate_otp()

        with app.app_context():
            msg = Message(
                subject="Mã OTP xác thực",
                recipients=[receiver_email],
                body=f"Mã OTP của bạn là: {otp}\nCó hiệu lực trong 5 phút."
            )
            mail.send(msg)
        return otp
