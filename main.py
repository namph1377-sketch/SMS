from UI.Admin_UI import Admin_UI
from UI.Auth_UI import UIAuth
from UI.Teacher_UI import Teacher_UI
from UI.Student_UI import Student_UI
import json
import os
from Database.Connect import Database

db = Database()

SESSION_FILE = r"C:\Users\AD\Downloads\SMS-main (4)\SMS-main\SMS-main\session.json"


# ================= SESSION =================
def load_session():
    if not os.path.exists(SESSION_FILE):
        return {"user": None, "is_logged_in": False}
    with open(SESSION_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_session(session):
    session_copy = {
        "user": None,
        "is_logged_in": session.get("is_logged_in", False)
    }

    if session.get("user"):
        user = session["user"]
        session_copy["user"] = {
            "userID": user["userID"],
            "username": user["username"],
            "Role": user["Role"]
        }

    with open(SESSION_FILE, "w", encoding="utf-8") as f:
        json.dump(session_copy, f, ensure_ascii=False, indent=4)


# ================= MAIN =================
def main():
    session = load_session()

    while True:
        print("\n===== STUDENT MANAGEMENT SYSTEM =====")

        # ================== CHƯA ĐĂNG NHẬP ==================
        if not session.get("user"):
            print("1. Log in")
            print("2. Forgot password")
            print("0. Exit")

            choice = input("Choice: ").strip()

            if choice == "1":
                username = input("Username: ").strip()
                password = input("Password: ").strip()

                user = UIAuth.ui_login(db, username=username, password=password)
                if user == "BLOCKED":
                    print("Your account has been locked!")
                    continue

                if not user:
                    print("Incorrect username or password")
                    continue

                session["user"] = user
                session["is_logged_in"] = True
                save_session(session)

            elif choice == "2":
                username = input("Enter username: ").strip()
                UIAuth.ui_reset_password(username)
                continue

            elif choice == "0":
                print("Exit program")
                break

            else:
                print("Invalid choice")
                continue

        # ================== ĐÃ ĐĂNG NHẬP → VÀO THẲNG MENU ==================
        user = session["user"]
        role = user["Role"].upper()

        if role == "ADM":
            logout = Admin_UI(user).admin_menu(user)

        elif role == "TEA":
            logout = Teacher_UI(user).run()
        elif role == "STU":
            logout = Student_UI(user_id=user["userID"]).run()
        else:
            print("Invalid role")
            logout = True

        # ====== SAU KHI LOGOUT TỪ MENU ======
        if logout:
            session["user"] = None
            session["is_logged_in"] = False
            save_session(session)
            print("Logged out successfully")


if __name__ == "__main__":
    main()
