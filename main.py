from UI.Admin_UI import Admin_UI
from UI.Auth_UI import Auth_UI
from UI.Teacher_UI import Teacher_UI
from UI.Student_UI import Student_UI

def main():
    while True:
        print("===== STUDENT MANAGEMENT SYSTEM =====")
        username = input("Username: ")
        password = input("Password: ")

        user = Auth_UI.login(username, password)

        if not user:
            print("Login failed")
            continue

        role = user.role.lower()

        if role == "admin":
            Admin_UI(user).run()

        elif role == "teacher":
            Teacher_UI(user).run()

        elif role == "student":
            Student_UI(user).run()

        else:
            print("Invalid role")

if __name__ == "__main__":
    main()
