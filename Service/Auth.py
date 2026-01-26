# 1. Standard Library Imports
import datetime
import os
import random
import json
# 2. Third-Party Imports
import bcrypt
from dotenv import load_dotenv
from flask import Flask
from flask_mail import Mail, Message
# 3. Local Application Imports
from Database.Connect import Database
from Database.Log import Log
from Database.User import User
#from debug import debug



SESSION_FILE = r"C:\Users\AD\Downloads\SMS-main (4)\SMS-main\SMS-main\session.json"

load_dotenv()
current_user = None

app = Flask(__name__)
app.config.update(
MAIL_SERVER="smtp.gmail.com",
MAIL_PORT=587,
MAIL_USE_TLS=True,
MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
MAIL_PASSWORD=os.getenv("MAIL_PASSWORD_APP"),
MAIL_DEFAULT_SENDER=os.getenv("MAIL_USERNAME"),
)
mail = Mail(app)

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
    def send_accout(user_id, email):
        username = user_id
        password = user_id
        with app.app_context():
            msg = Message(
                subject="Student account",
                recipients=[email],
                body=f"Your username is: {username}\nYour password is: {password}."
            )
            mail.send(msg)

    @staticmethod
    def login(db, username, password):
        user = User.find_by_username(db, username)
        if not user:
            return None

        if not verify_password(password, user["password"]):
            return None

        if user["isActive"] == 0:
            return "BLOCKED"


        return user   


    @staticmethod
    def logout():
        session = {
            "user": None,
            "is_logged_in": False
        }
        with open(SESSION_FILE, "w", encoding="utf-8") as f:
            json.dump(session, f)

        return True
    def changePassword(db, user):
        old_pass = input("Enter current password: ").strip()

        db_user = User.find_by_username(db, user["username"])
        if not db_user:
            print("User does not exist!")
            return

        if not verify_password(old_pass, db_user["password"]):
            print("Incorrect current password!")
            return

        new_pass = input("Enter new password: ").strip()
        confirm_pass = input("Re-enter new password: ").strip()

        if new_pass != confirm_pass:
            print("Passwords do not match!")
            return

        User.update_password(db, user["userID"], hash_password(new_pass))


        print("Password changed successfully!")


    def reset_password(user, db):
        new_pass = input("Enter new password: ").strip()
        confirm_pass = input("Re-enter new password: ").strip()

        if new_pass != confirm_pass:
            print("Passwords do not match!")
            return

        User.update_password(db,user["userID"], hash_password(new_pass))
        print("Password reset successfully!")
        return new_pass

    def verify_otp(input_otp: str, real_otp: str) -> bool:
        return input_otp == real_otp
    def requestOTP(receiver_email: str) -> str:


        otp = generate_otp()

        with app.app_context():
            msg = Message(
                subject="OTP Verification Code",
                recipients=[receiver_email],
                body=f"Your OTP code is: {otp}\nIt is valid for 5 minutes."
            )
            mail.send(msg)
        return otp
