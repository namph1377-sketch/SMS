from Service.Admin import Admin
from UI.Auth_UI import UIAuth as Auth_UI

class Admin_UI: 
    def __init__(self, user):
        self.user = user
        self.admin = Admin(user["userID"])

    @staticmethod
    def pause(): 
        input("\nPress [Enter] to continue...")

    def admin_menu(self, user): 
        print(f"\nWelcome Admin: {user['username']}")

        while True:
            print("\n================= ADMIN MENU ================")
            print("1. Create student account")
            print("2. View student details")
            print("3. Update student profile")
            print("4. Delete student profile")
            print("5. Add course section to student")
            print("6. Change password")
            print("7. Log out")
            print("============================================")

            choice = input("Function selection (1-7): ").strip()

            # 1. CREATE STUDENT
            if choice == "1":
                print("\n------------- CREATE STUDENT ACCOUNT-------------")
                self.admin.createStudent()
                Admin_UI.pause()

            # 2. VIEW STUDENT
            elif choice == "2":
                while True:
                    print("\n---------------- VIEW STUDENT DETAILS ----------------")
                    print("[1] Search by Student ID or Name (Keyword)")
                    print("[2] Filter by Department / Academic Class / Status")
                    print("[3] Return Admin menu")

                    opt = input("Enter selection: ").strip()

                    if opt == "1":
                        info = self.admin.searchStudent()
                    elif opt == "2":
                        info = self.admin.searchStudentByFilter()
                    elif opt == "3":
                        break
                    else:
                        print("Invalid choice")
                        continue

                    if info:
                        self.admin.viewStudentDetail(info)
                        Admin_UI.pause()

            # 3. UPDATE STUDENT
            elif choice == "3":
                while True:
                    print("\n---------------- UPDATE STUDENT PROFILE ----------------")
                    print("[1] Search by Student ID or Name (Keyword)")
                    print("[2] Filter by Department / Academic Class / Status")
                    print("[3] Return Admin menu")

                    opt = input("Enter selection: ").strip()

                    if opt == "1":
                        info = self.admin.searchStudent()
                    elif opt == "2":
                        info = self.admin.searchStudentByFilter()
                    elif opt == "3":
                        break
                    else:
                        print("Invalid choice")
                        continue

                    if info:
                        self.admin.updateStudent(info)
                    Admin_UI.pause()

            # 4. DELETE STUDENT
            elif choice == "4":
                while True:
                    print("\n---------------- DELETE STUDENT PROFILE ----------------")
                    print("[1] Search by Student ID or Name (Keyword)")
                    print("[2] Filter by Department / Academic Class / Status")
                    print("[3] Return Admin menu")

                    opt = input("Enter selection: ").strip()

                    if opt == "1":
                        info = self.admin.searchStudent()
                    elif opt == "2":
                        info = self.admin.searchStudentByFilter()
                    elif opt == "3":
                        break
                    else:
                        print("Invalid choice")
                        continue
                    
                    if info:
                        print("\n[VERIFY INFORMATION]")
                        print(f"- Full name: {info['fullName']}")
                        print(f"- Student ID: {info['userID']}")
                        print(f"- Academic Class: {info['class']['ClassID']}")
                        print(f"- Status: {info['status']}")

                        while True:
                            confirm = input("\nAre you sure you want to delete?\n1. Delete\n2. Cancel\n=> ")
                            if confirm == "1":
                                self.admin.deleteStudent(info)
                                break
                            elif confirm == "2":
                                print("Deletion cancelled successfully")
                                break
                            else:
                                print("Invalid choice")
                                continue
                        Admin_UI.pause()

            # 5. ADD COURSE
            elif choice == "5":
                print("\n---------------- ADD COURSE FOR STUDENT ----------------")
                self.admin.addCourse()
                Admin_UI.pause()

            # 6. CHANGE PASSWORD (placeholder)
            elif choice == "6":
                Auth_UI.ui_change_password(self.user)
                Admin_UI.pause()

            # 7. LOG OUT
            elif choice == "7":
                confirm = input("Are you sure you want to log out of the system? (y/n): ").lower()
                if confirm == "y":
                    return True

                print("Invalid selection")

            # NHẬP KHÔNG PHẢI 1–7
            else:
                print("Invalid selection! Please choose a number from 1 to 7.")
