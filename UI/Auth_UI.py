import datetime
from Service.Auth import Auth, check_effective_period
from Database.Connect import Database
from Database.User import User
from Database.StudentProfile import StudentProfile
from Service.Auth import Auth
from Database.Connect import Database
import datetime
class UIAuth:
    # ================== LOGIN UI ==================
    def ui_login(db, username, password):
        print("=== LOGIN ===")

        user = Auth.login(db, username, password)
        if not user:
            print("Login failed!")
        return user

    # ================== LOGOUT UI ==================
    @staticmethod
    def ui_logout():
        return Auth.logout()
        

    # ================== DOI MAT KHAU ==================
    @staticmethod
    def ui_change_password( user_id):
        print("=== CHANGE PASSWORD ===") 
        db = Database()

        Auth.changePassword(db, user_id)

    # ================== QUEN MAT KHAU ==================
    def ui_reset_password(username):
        db = Database()

        # 1. Lấy user theo username
        user = User.find_by_username(db, username)
        if not user:
            print("Account does not exist")
            return False

        # 2. Lấy email từ student_profile
        email = StudentProfile.get_email_by_user_id(db, user["userID"])
        if not email:
            email = User.find_by_email(db, user["userID"])
            if not email:
                print("This account does not have an email")
                return False
            email = email[0]   # hoặc email_record[0]

        while True:
            print("\n=== FORGOT PASSWORD ===")
            print("1. Send OTP")
            print("2. Exit")
            choice = input("Choose: ").strip()

            if choice == "1":
                input_email = input(
                    "Enter the email to receive OTP (Press Enter to cancel): "
                ).strip()

                if input_email == "":
                    print("OTP sending canceled")
                    continue

                if input_email != email:
                    print("Incorrect email!")
                    continue

                real_otp = Auth.requestOTP(email)
                otp_time = datetime.datetime.now()
                print("OTP has been sent!")
                print("(Enter OTP | Press Enter to cancel | 0 to exit)")

                input_otp = input("Enter OTP: ").strip()

                # ==== CHO PHEP THOAT ====
                if input_otp == "" or input_otp.lower() in ("0", "q", "exit"):
                    print("OTP verification canceled")
                    continue

                if not check_effective_period(otp_time):
                    print("OTP has expired!")
                    continue

                if Auth.verify_otp(input_otp, real_otp):
                    Auth.reset_password(user, db)
                    return True
                else:
                    print("Incorrect OTP!")

            elif choice == "2":
                print("Exit forgot password")
                return False

            else:
                print("Invalid choice!")
