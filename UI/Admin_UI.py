from Service.Admin import Admin


class Admin_UI: 

    @staticmethod
    def pause():
        input("\nPress [Enter] to continue...")

    def admin_menu():
        admin = Admin()

        while True:
            print("\n================= ADMIN MENU ================")
            print("1. Create student account")
            print("2. View student details")
            print("3. Update student profile")
            print("4. Delete student profile")
            print("5. Add course section to student")
            print("6. Change your password")
            print("7. Log out")
            print("============================================")

            choice = input("Function selection (1-7): ").strip()

            # 1. CREATE STUDENT
            if choice == "1":
                print("\n------------- CREATE STUDENT ACCOUNT-------------")
                admin.createStudent()
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
                        info = admin.searchStudent()
                    elif opt == "2":
                        info = admin.searchStudentByFilter()
                    elif opt == "3":
                        break
                    else:
                        print("Invalid choice")
                        continue

                    if info:
                        admin.viewStudentDetail(info)
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
                        info = admin.searchStudent()
                    elif opt == "2":
                        info = admin.searchStudentByFilter()
                    elif opt == "3":
                        break
                    else:
                        print("Invalid choice")
                        continue

                    if info:
                        admin.updateStudent(info)
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
                        info = admin.searchStudent()
                    elif opt == "2":
                        info = admin.searchStudentByFilter()
                    elif opt == "3":
                        break
                    else:
                        print("Invalid choice")
                        continue
                    
                    if info:
                        print("\n[VERIFY INFORMATION]")
                        print(f"- Full name: {info.fullname}")
                        print(f"- Student ID: {info.userID}")
                        print(f"- Academic Class: {info.ClassID}")
                        print(f"- Status: {info.status}")

                        confirm = input("\nAre you sure you want to delete?\n1. Delete\n2. Cancel\n=> ")
                        if confirm == "1":
                            admin.deleteStudent(info)
                    Admin_UI.pause()

            # 5. ADD COURSE
            elif choice == "5":
                print("\n---------------- ADD COURSE FOR STUDENT ----------------")
                admin.addCourse()
                Admin_UI.pause()

            # 6. CHANGE PASSWORD (placeholder)
            elif choice == "6":
                print("Change password feature is not implemented yet.")
                Admin_UI.pause()

            # 7. LOG OUT
            elif choice == "7":
                print("Logging out...")
                break

            else:
                print("Invalid selection!")
