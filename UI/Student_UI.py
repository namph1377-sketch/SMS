from Service.Student import Student


class Student_UI:
    def __init__(self, user_id):
        self.student = Student(user_id)

    def run(self):
        while True:
            print("\n================ STUDENT MENU ================")
            print("1. View personal profile")
            print("2. Update personal information")
            print("3. View curriculum framework")
            print("4. View Grades")
            print("5. View Schedule")
            print("6. Change password")
            print("7. Logout")
            print("-----------------------------------------------")
            choice = input("Select function: ")

            if choice == "1":
                self.view_profile()

            elif choice == "2":
                self.update_personal_information()

            elif choice == "3":
                self.view_curriculum()

            elif choice == "4":
                self.view_grades()

            elif choice == "5":
                self.view_schedule()

            elif choice == "6":
                self.change_password()

            elif choice == "7":
                if self.logout():
                    break
            else:
                print("Invalid selection!")

    # ========== 1. VIEW PROFILE ==========
    def view_profile(self):
        print("================================================")
        print("                STUDENT PROFILE")
        print("================================================")

        profile = self.student.viewProfile()

        if not profile:
            print("Return to student menu")
            return

        print("I. ACADEMIC INFORMATION (Basic)")
        print(f"- Full name : {profile.get('full_name','')}")
        print(f"- Student ID           : {profile.get('student_id','')}             [Read-only]")
        print(f"- Date of birth        : {profile.get('date_of_birth','')}")
        print(f"- Education level      : {profile.get('education_level','')}")
        print(f"- Training type        : {profile.get('training_type','')}")
        print(f"- Department             : {profile.get('department','')}")
        print(f"- Major                : {profile.get('major','')}")
        print(f"- Specialization       : {profile.get('specialization','')}")
        print(f"- Course               : {profile.get('course','')}")
        print(f"- Status               : {profile.get('status','')}")
        print(f"- Student email        : {profile.get('student_email','')}")
        print(f"- Enrollment date      : {profile.get('enrollment_date','')}")
        print(f"- Academic Class       : {profile.get('academic_class','')}")

        print("II. DETAILED PERSONAL INFORMATION")
        print(f"- Phone number         : {profile.get('phone_number','')}")
        print(f"- Emergency contact    : {profile.get('emergency_contact','')}")
        print(f"- Personal email       : {profile.get('personal_email','')}")
        print(f"- Ethnicity            : {profile.get('ethnicity','')}")
        print(f"- Religion             : {profile.get('religion','')}")
        print(f"- Nationality          : {profile.get('nationality','')}")
        print(f"- Youth Union entry date: {profile.get('youth_union_date','')}")
        print(f"- Party entry date     : {profile.get('party_entry_date','')}")

        print("III. IDENTIFICATION & INSURANCE INFORMATION")
        print(f"- Citizen identification number      : {profile.get('citizen_id','')}")
        print(f"- Issue date           : {profile.get('issue_date','')}")
        print(f"- Place of issue       : {profile.get('place_of_issue','')}")
        print(f"- Health insurance ID  : {profile.get('health_insurance_id','')}")
        print(f"- Initial medical facility: {profile.get('initial_medical_facility','')}")
        print(f"- Place of birth       : {profile.get('place_of_birth','')}")
        print(f"- Native place         : {profile.get('native_place','')}")
        print(f"- Hometown             : {profile.get('hometown','')}")
        print(f"- Permanent residence  : {profile.get('permanent_residence','')}")
        print(f"- Bank account information: {profile.get('bank_account','')}")

        print("--------------------------------------------------------")
        print("(View only – academic information cannot be edited)")
        print("========================================================")
        input("\nReturn to student menu")


    # ========== 2. UPDATE PERSONAL INFO ==========
    def update_personal_information(self):
        print("\n================================================")
        print("        UPDATE STUDENT PERSONAL INFORMATION")
        print("================================================")

        new_data = {}

        print("\nI. DETAILED PERSONAL INFORMATION")
        phone = input("- Phone number         : ")
        emergency = input("- Emergency contact    : ")
        email = input("- Personal email       : ")
        ethnicity = input("- Ethnicity            : ")
        religion = input("- Religion             : ")
        nationality = input("- Nationality          : ")
        youth_date = input("- Youth Union entry date: ")
        party_date = input("- Party entry date     : ")

        print("\nII. IDENTIFICATION & INSURANCE INFORMATION")
        citizen_id = input("- Citizen identification number      : ")
        issue_date = input("- Issue date           : ")
        place_issue = input("- Place of issue       : ")
        health_id = input("- Health insurance ID  : ")
        medical_place = input("- Initial medical facility: ")
        place_birth = input("- Place of birth       : ")
        native_place = input("- Native place         : ")
        hometown = input("- Hometown             : ")
        residence = input("- Permanent residence  : ")
        bank = input("- Bank account information: ")

        # gom dữ liệu (chỉ thêm nếu người dùng nhập)
        fields = {
            "phone_number": phone,
            "emergency_contact": emergency,
            "personal_email": email,
            "ethnicity": ethnicity,
            "religion": religion,
            "nationality": nationality,
            "youth_union_date": youth_date,
            "party_date": party_date,
            "citizen_id": citizen_id,
            "issue_date": issue_date,
            "place_of_issue": place_issue,
            "health_insurance_id": health_id,
            "initial_medical_facility": medical_place,
            "place_of_birth": place_birth,
            "native_place": native_place,
            "hometown": hometown,
            "permanent_residence": residence,
            "bank_account": bank,
        }

        for k, v in fields.items():
            if v.strip():
                new_data[k] = v

        print("--------------------------------------------------------")
        input("Press [Enter] to continue")

        self.student.updateProfile(new_data)

        print("Return to student menu")

    # ========== 3. VIEW CURRICULUM ==========
    def view_curriculum(self):
        print("================================================")
        print("                CURRICULUM FRAMEWORK")
        print("================================================")

        curriculum = self.student.viewCurriculum()

        if curriculum:
            for semester in range(1, 9):
                print(f"SEMESTER {semester}:")
                subjects = curriculum.get(semester, [])
                for s in subjects:
                    print(
                        f"- {s['course_id']} | {s['subject_name']} | {s['credits']}"
                    )
                print()
        else:
            for semester in range(1, 9):
                print(f"SEMESTER {semester}:\n")

        input("Press [Enter] to continue")
        print("Return to student menu")


    # ========== 4. VIEW GRADES ==========
    def view_grades(self):
        print("---------------- View Grades---------------")
        print("Select function 4")

        grades = self.student.viewGrade()

        print("Number|Course ID|Subject | Credits|CA score|Final score|Final grade|GPA|Letter grade| Classification| Pass|Note")

        if grades:
            for i, g in enumerate(grades, start=1):
                print(
                    f"{i:<6} "
                    f"{g['course_id']:<8} "
                    f"{g['subject_name']:<15} "
                    f"{g['credits']:<6} "
                    f"{g['ca_score']:<15} "
                    f"{g['final_score']:<17} "
                    f"{g['final_grade']:<10} "
                    f"{g['gpa']:<7} "
                    f"{g['letter_grade']:<15} "
                    f"{g['classification']:<15} "
                    f"{g['pass']:<6} "
                    f"{g.get('note','')}"
                )

        print("\nReturn to student menu")



    # ========== 5. VIEW SCHEDULE ==========
    def view_schedule(self):
        print("--------------- View Schedule  -----------------")
        print("Select function 5")

        schedule = self.student.ViewSchedule()

        print("Day        |   Course time   |   Subject                  |   Course ID            |  Location")

        if schedule:
            for s in schedule:
                print(
                    f"{s['day']:<10}|"
                    f"{s['course_time']:^17}|"
                    f"{s['subject_name']:<26}|"
                    f"{s['course_id']:^24}|"
                    f"{s['location']:^10}"
                )

        print("Return to student menu")


    # ========== 6. CHANGE PASSWORD ==========
    def change_password(self):
        print("\n----- CHANGE PASSWORD -----")
        current = input("Enter current password: ")
        new = input("Enter new password     : ")
        confirm = input("Confirm new password   : ")
        input("Press [ENTER] to continue")

        self.user.changePassword(current, new, confirm)

        print("Return to student menu")

    # ========== 7. LOGOUT ==========
    def logout(self):
        print("\nAre you sure you want to log out of the system?")
        confirm = input("Confirm (y/n): ")
        if confirm.lower() == "y":
            print("Logged out successfully")
            print("Return to student management system")
            return True
        return False
