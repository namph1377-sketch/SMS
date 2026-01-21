import datetime
from Auth import Auth, current_user
from Auth import (
    check_effective_period,
    verify_otp,
    reset_password,
    requestOTP
)
class UIAuth:
    # ================== LOGIN UI ==================
    def ui_login():
        if current_user is not None:
            print("Ban dang dang nhap roi!")
            return
        print("=== DANG NHAP ===")

        success = Auth.login()
        if not success:
            print("Dang nhap that bai!")

    # ================== LOGOUT UI ==================
    def ui_logout():
        print("=== DANG XUAT ===")
        print("bạn co muon dang xuat khong? (y/n)")
        choice = input().strip().lower()
        if choice != 'y':
            print("Huy dang xuat.")
            return
        else:
            message = Auth.logout()
            print(message)

    # ================== DOI MAT KHAU ==================
    def ui_change_password():
        if current_user is None:
            print("Vui long dang nhap truoc!")
            return
        print("=== DOI MAT KHAU ===")

        Auth.changePassword(current_user)

    # ================== QUEN MAT KHAU ==================
    def ui_reset_password(student):
        while True:
            print("=== QUEN MAT KHAU ===")
            print("1. Gui OTP")
            print("2. Thoat")
            choice = input("Chon chuc nang: ").strip()

            if choice == "1":
                email = input("Nhap email nhan OTP: ").strip()

                if email != student["email"]:
                    print("Email khong ton tai!")
                    continue

                try:
                    real_otp = requestOTP(email)
                    otp_created_time = datetime.datetime.now()
                    print("Gui OTP thanh cong!")

                    input_otp = input("Nhap ma OTP: ").strip()

                    if not check_effective_period(otp_created_time):
                        print("OTP da het han!")
                        continue

                    if verify_otp(input_otp, real_otp):
                        print("OTP hop le!")
                        reset_password(student)
                    else:
                        print("OTP khong dung!")

                except Exception as e:
                    print("Loi gui OTP:", e)

            elif choice == "2":
                break
            else:
                print("Lua chon khong hop le!")

            print()
