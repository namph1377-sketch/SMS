from Service.Student import Student
from UI.Auth_UI import UIAuth
from debug import (
    debug_phone,
    debug_date,
    debug_citizen_id,
    validate_entry_date
)


class Student_UI:
    def __init__(self, user_id):
        self.student = Student(user_id)
        profile = self.student.viewProfile()   # lấy thông tin user

        self.user = {
            "userID": user_id,
            "username": profile["username"]     # BẮT BUỘC
        }

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
                    return True
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
        department = profile.get("department", {})
        print(f"- Department           : {department.get('DepartmentName', '')}")
        major = profile.get("major",{})
        print(f"- Major                : {major.get('MajorName','')}")
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
        # ===== PHONE NUMBER =====
        while True:
            phone = input("- Phone number: ").strip()

            if not phone:
                break  # cho phép bỏ trống

            phone_value, phone_error = debug_phone(phone)

            if phone_error:
                print("ERROR:", phone_error)
                continue
            else:
                phone = phone_value
                break

        while True:
            emergency = input("- Emergency contact    : ")

            if not emergency:
                break  # cho phép bỏ trống

            emergency_value, emergency_error = debug_phone(emergency)

            if emergency_error:
                print("ERROR:", emergency_error)
                continue
            else:
                emergency = emergency_value
                break

        email = input("- Personal email       : ")
        ethnicity = input("- Ethnicity            : ")
        religion = input("- Religion             : ")
        nationality = input("- Nationality          : ")
        # ===== YOUTH UNION & PARTY ENTRY DATE =====
        while True:
            youth_date = None
            party_date = None

            youth_input = input("- Youth Union entry date: ").strip()
            party_input = input("- Party entry date: ").strip()

            # cho phép bỏ trống cả hai
            if not youth_input and not party_input:
                break

            # nếu chỉ nhập 1 trong 2 → cho qua
            if youth_input and not party_input:
                youth_date = youth_input
                break

            if party_input and not youth_input:
                party_date = party_input
                break

            # nếu cả hai đều có → kiểm tra thứ tự
            check, youth_input, party_input = validate_entry_date(youth_input, party_input)
            if not check:
                print("Please re-enter both dates.\n")
                continue
            
            youth_date = youth_input
            party_date = party_input
            break

        print("\nII. IDENTIFICATION & INSURANCE INFORMATION")
        while True:
            citizen_id = input("- Citizen identification number: ").strip()

            if not citizen_id:
                break

            cid = debug_citizen_id(citizen_id)

            if cid is None:
                continue
            else:
                citizen_id = cid
                break

        while True:
            issue_date = input("- Issue date: ").strip()

            if not issue_date:
                break

            date_value, date_error = debug_date(issue_date)

            if date_error:
                print("ERROR:", date_error)
                continue
            else:
                issue_date = date_value
                break
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
            if v is None:
                continue

            if isinstance(v, str):
                if v.strip():
                    new_data[k] = v
            else:
                # datetime / int / kiểu khác
                new_data[k] = v


        print("--------------------------------------------------------")
        input("Press [Enter] to continue")

        if new_data:
            if self.student.updateProfile(new_data):
                print("Personal information updated successfully")
            else:
                print("Failed to update personal information")
        else:
            print("No changes were made")

        print("Return to student menu")


    # ========== 3. VIEW CURRICULUM ==========
    def view_curriculum(self):
        print("================================================")
        print("                CURRICULUM FRAMEWORK")
        print("================================================")

        curriculum = self.student.viewCurriculum()  # ← dict

        for semester in range(1, 9):
            print(f"SEMESTER {semester}:")
            subjects = curriculum.get(semester, [])
            for s in subjects:
                print(
                    f"- {s['subjectID']} | "
                    f"{s['subjectName']} | "
                    f"{s['Credits']}"
                )
            print()

        input("Press [Enter] to continue")
        print("Return to student menu")



    # ========== 4. VIEW GRADES ==========
    def view_grades(self):
        print("---------------- View Grades---------------")

        grades = self.student.viewGrade()

        print("No |CourseID |Subject         |Credits|CA |Final |FinalGrade|GPA |Letter |Classfication |Pass |Note")

        if not grades:
            print("No grade data")
            return

        for i, g in enumerate(grades, start=1):
            course = g["course"]
            subject = course["subject"]
            grade = g["grade"]

            print(
                f"{i:<3} "
                f"{course['CourseID']:<9} "
                f"{subject['subjectName']:<15} "
                f"{subject['Credits']:<7} "
                f"{grade['CAscore']:<4} "
                f"{grade['Finalscore']:<6} "
                f"{grade['FinalGrade']:<10} "
                f"{grade['GPA']:<4} "
                f"{grade['LetterGrade']:<7} "
                f"{grade['classification']:<8} "
                f"{grade['Pass']:<5} "
                f"{grade['Notes'] or ''}"
            )

        print("\nReturn to student menu")




    # ========== 5. VIEW SCHEDULE ==========
    def view_schedule(self):
        print("--------------- View Schedule -----------------")

        schedule = self.student.viewSchedule()

        print("CourseID | Course Time | Subject                      | Credits | Start                 | End         ")

        if not schedule:
            print("No schedule available")
            return

        for s in schedule:
            subject = s["subject"]

            course_time = s.get("CourseTime")

            if course_time:
                course_time = course_time.strftime("%H:%M")
            else:
                course_time = ""


            start = s.get("Startdate", "")
            end = s.get("Enddate", "")

            print(
                f"{s['CourseID']:<8} | "
                f"{course_time:<6}      | "
                f"{subject['subjectName']:<28} | "
                f"{subject['Credits']:<7} | "
                f"{start} | "
                f"{end}"
            )

        print("Return to student menu")



    # ========== 6. CHANGE PASSWORD ==========
    def change_password(self):

        UIAuth.ui_change_password(self.user)

        print("Return to student menu")

    # ========== 7. LOGOUT ==========
    def logout(self):
        confirm = input("Are you sure you want to log out of the system? (y/n): ").lower()
        if confirm.lower() == "y":
            return confirm
        print("Invalid selection")
