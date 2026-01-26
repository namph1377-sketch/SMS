from Database.Connect import Database
from Database.User import User
from Database.StudentProfile import StudentProfile
from Database.Assignment import Assignment
from Database.AcademicClass import AcademicClass
from Database.Log import Log
from Database.Grade import Grade
from Service.Auth import hash_password, Auth
from debug import (
    debug_phone,
    debug_date,
    debug_citizen_id,
    validate_entry_date
)
from datetime import datetime
import os
import json

SESSION_FILE = r"C:\Users\AD\Downloads\SMS-main (4)\SMS-main\SMS-main\session.json"

def load_session():
    if not os.path.exists(SESSION_FILE):
        return {"user": None, "is_logged_in": False}
    with open(SESSION_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def convert_status(value: str, to_db: bool = True) -> str:
    """
    Chuyển đổi trạng thái sinh viên giữa dạng hiển thị và dạng lưu DB.

    to_db = True  : từ mô tả đầy đủ -> mã lưu DB
    to_db = False : từ mã DB -> mô tả đầy đủ
    """

    status_map = {
        "Currently studying": "STUDY",
        "Reserved": "RESV",
        "Graduation": "GRAD",
        "Forced expulsion": "EXPEL"
    }

    if to_db:
        if value not in status_map:
            raise ValueError(f"Invalid status: {value}")
        return status_map[value]
    else:
        reverse_map = {v: k for k, v in status_map.items()}
        if value not in reverse_map:
            raise ValueError(f"Invalid status code: {value}")
        return reverse_map[value]

class Admin:
    def __init__(self, user_id):
        self.db = Database()
        self.user_id = user_id   


    def createStudent(self):

        while True:
            # ===== STUDENT ID =====
            while True:
                student_id = input("Citizen identification number: ").strip()

                if not student_id:
                    print("Student ID must not be empty")
                    continue

                if len(student_id) != 5:
                    print("Student ID must be exactly 5 characters long")
                    continue

                if User.search_user_by_ID(self.db, student_id):
                    print("Student ID already exists")
                    continue

                break

            # ===== PERSONAL EMAIL =====
            while True:
                personal_email = input("Personal email: ").strip()

                if not personal_email:
                    print("Personal email must not be empty")
                    continue

                if "@" not in personal_email:
                    print("Invalid email")
                    continue

                if User.search_user_by_personal_email(self.db, personal_email):
                    print("Personal email already exists")
                    continue

                break

            # ===== FULL NAME =====
            while True:
                full_name = input("Full name: ").strip()
                if full_name:
                    break
                print("Full name must not be empty")

            # ===== DATE OF BIRTH =====
            while True:
                dob_input = input("Date of birth: ").strip()

                if not dob_input:
                    print("ERROR: Date of birth must not be empty")
                    continue

                dob, err = debug_date(dob_input)
                if err:
                    print("ERROR:", err)
                    continue

                date_of_birth = dob
                break

            # ===== EDUCATION LEVEL =====
            while True:
                education_level = input("Education level: ").strip()
                if education_level:
                    break
                print("Education level must not be empty")

            # ===== TRAINING TYPE =====
            while True:
                training_type = input("Training type: ").strip()
                if training_type:
                    break
                print("Training type must not be empty")

            # ===== MAJOR =====
            while True:
                major = input("Major: ").strip()
                if major:
                    break
                print("Major must not be empty")

            # ===== SPECIALIZATION =====
            while True:
                specialization = input("Specialization: ").strip()
                if specialization:
                    break
                print("Specialization must not be empty")

            # ===== DEPARTMENT =====
            while True:
                department = input("Department: ").strip()
                if department:
                    break
                print("Department must not be empty")

            # ===== COURSE YEAR =====
            while True:
                course = input("CourseYear: ").strip()
                if course:
                    break
                print("CourseYear must not be empty")

            # ===== ENROLLMENT DATE =====
            while True:
                enroll_input = input("Enrollment date: ").strip()

                if not enroll_input:
                    print("ERROR: Enrollment date must not be empty")
                    continue

                enroll, err = debug_date(enroll_input)
                if err:
                    print("ERROR:", err)
                    continue

                enrollment_date = enroll
                break

            # ===== STATUS =====
            while True:
                status = input(
                    "Status (Currently studying / Reserved / Graduation / Forced expulsion): "
                ).strip()
                if status:
                    break
                print("Status must not be empty")

            # ===== CLASS ID =====
            while True:
                class_id = input("Academic Class: ").strip()
                if class_id:
                    break
                print("Academic Class must not be empty")

            # ===== VALIDATE STRUCTURE =====
            if not AcademicClass.validate_structure(self.db, class_id, major, department):
                    print("Invalid class, major, or department information\n")
                    continue

            break

        # ===== TẠO USER & PROFILE =====
        password = hash_password(student_id)

        user = User(
            student_id,
            student_id,
            password,
            None,
            "STU",
            "1",
            full_name,
            date_of_birth,
            education_level,
            training_type,
            convert_status(status, True),
            enrollment_date,
            specialization,
            course,
            class_id,
            None
        )

        profile = StudentProfile(
            student_id,
            None,
            personal_email,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None
        )

        if not user.add_user(self.db):
            print("Error while adding user")
            return

        if not profile.add_student_profile(self.db):
            print("Error while adding student profile")
            return

        Auth.send_accout(student_id, personal_email)
        print("Student account created successfully")


    def choose_student_from_list(self, students):
        print("\n=== STUDENT LIST ===")
        for i, s in enumerate(students, start=1):
            print(f"{i}. {s['userID']} - {s['fullName']}")  # ID - FullName

        try:
            choice = int(input("Select an option number: "))
            if 1 <= choice <= len(students):
                return students[choice - 1]
        except ValueError:
            pass

        print("Invalid selection")
        return None


    def searchStudent(self):
        keyword = input("Keyword: ").strip()

        if not keyword:
            print("Keyword must not be empty")
            return None

        # 1️ Ưu tiên tìm theo ID
        data = User.search_user_by_ID(self.db, keyword)
        if data:
            return data

        # 2️ Không phải ID → tìm theo tên (cho phép chữ + số)
        results = User.search_user_by_Name(self.db, keyword)
        if results:
            students = [u for u in results if u['Role'] == "STU"]

            if not students:
                print("No matching students found")
                return None

            return self.choose_student_from_list(students)

        # 3️ Không tìm thấy
        print("No matching students found")
        return None


    def choose_status(self):
        print("\nSelect study status:")
        print("[1] Currently studying")
        print("[2] Reserved")
        print("[3] Graduation")
        print("[4] Forced expulsion")
        print("[Enter] Skip")

        choice = input("Choice: ").strip()

        status_map = {
            "1": "Currently studying",
            "2": "Reserved",
            "3": "Graduation",
            "4": "Forced expulsion"
        }

        return status_map.get(choice, None)

    def searchStudentByFilter(self):

        department = input("Department (Press Enter to skip): ").strip()
        academic_class = input("Academic Class (Press Enter to skip): ").strip()
        status = self.choose_status()

        # không được trống cả 3
        if not department and not academic_class and not status:
            print("Please provide at least one filter condition")
            return None

        results = User.search_user_by_filter(
            self.db,
            DepartmentName=department or None,
            ClassName=academic_class or None,
            status = convert_status(status, True) if status is not None else None
        )

        if not results:
            print("No matching students found")
            return None

        return self.choose_student_from_list(results)

    def viewStudentDetail(self, info: User):
        print("\nEDUCATIONAL INFORMATION")
        print(f"Full name: {info['fullName']}")
        print(f"Student ID: {info['userID']}")
        print(f"Date of birth: {info['dateofBirth']}")
        print(f"Education level: {info['educationLevel']}")
        print(f"Training type: {info['educationType']}")
        print(f"Department: {info['department']['DepartmentName']}")
        print(f"Major: {info['major']['MajorName']}")
        print(f"Specialization: {info['Specialization']}")
        print(f"Coure: {info['courseYear']}")
        print(f"status: {convert_status(info['status'], False)}")
        print(f"Student Email: {info['email']}")
        print(f"Enrollment date: {info['Admissiondate']}")
        print(f"Academic Class: {info['class']['ClassID']}")

        print("\nDETAILED PERSONAL INFORMATION")
        print(f"Sex: {info['profile']['gender']}")
        print(f"Phone number: {info['profile']['phone']}")
        print(f"Emergency contact: {info['profile']['emergencyPhone']}")
        print(f"Personal email: {info['profile']['personalEmail']}")
        print(f"Ethnicity: {info['profile']['ethnicity']}")
        print(f"Religion: {info['profile']['religion']}")
        print(f"Nationality: {info['profile']['Nationality']}")
        print(f"Youth Union entry date: {info['profile']['joinUnionDate']}")
        print(f"Party entry date: {info['profile']['joinPartyDate']}")

        print("\nDOCUMENTATION & INSURANCE INFORMATION")
        print(f"Citizen Identification Number: {info['profile']['nationalID']}")
        print(f"Health insurance ID: {info['profile']['insuranceCode']}")
        print(f"Initial medical facility: {info['profile']['initialHospital']}")
        print(f"Place of birth: {info['profile']['placeOfBirth']}")
        print(f"Hometown: {info['profile']['hometown']}")
        print(f"Permanent: {info['profile']['permanentResidence']}")
        print(f"Bank account information: {info['profile']['bankAccount']}")
    

    def updateStudent(self, info: User):
        print("\nCURRENT INFORMATION")
        print(f"Full name: {info['fullName']}")
        print(f"Student ID: {info['userID']}")
        print(f"Date of birth: {info['dateofBirth']}")
        print(f"Education level: {info['educationLevel']}")
        print(f"Training type: {info['educationType']}")
        print(f"Department: {info['department']['DepartmentName']}")
        print(f"Major: {info['major']['MajorName']}")
        print(f"Specialization: {info['Specialization']}")
        print(f"CourseYear: {info['courseYear']}")
        print(f"Student Email: {info['email']}")
        print(f"Enrollment date: {info['Admissiondate']}")
        print(f"status: {convert_status(info['status'], False)}")
        print(f"Academic Class: {info['class']['ClassID']}")
        print(f"Curriculum_ID: {info['curriculumID']}")

        print("\n=== UPDATE INFORMATION (Press Enter to keep current value) ===")
        full_name = input("Full name: ").strip()
        full_name = full_name if full_name else info['fullName']

        # ===== DATE OF BIRTH =====
        while True:
            dob_input = input("Date of birth: ").strip()

            # Enter → giữ nguyên
            if not dob_input:
                date_of_birth = info['dateofBirth']
                break

            dob, err = debug_date(dob_input)
            if err:
                print("ERROR:", err)
                continue

            date_of_birth = dob
            break


        education_level = input("Education level: ").strip()
        education_level = education_level if education_level else info['educationLevel']

        training_type = input("Training type: ").strip()
        training_type = training_type if training_type else info['educationType']

        major = input("Major: ").strip()
        major = major if major else info['major']['MajorName']

        specialization = input("Specialization: ").strip()
        specialization = specialization if specialization else info['Specialization']

        department = input("Department: ").strip()
        department = department if department else info['department']['DepartmentName']

        course = input("CourseYear: ").strip()
        course = course if course else info['courseYear']

        # ===== ENROLLMENT DATE =====
        while True:
            enroll_input = input("Enrollment date: ").strip()

            # Enter → giữ nguyên
            if not enroll_input:
                enrollment_date = info['Admissiondate']
                break

            enroll, err = debug_date(enroll_input)
            if err:
                print("ERROR:", err)
                continue

            enrollment_date = enroll
            break

        status_input = input("status(Currently studying/Reserved/Graduation/Forced expulsion): ").strip()
        status = convert_status(status_input, True) if status_input else info['status']

        student_email = input("Student email: ").strip()
        student_email = student_email if student_email else info['email']

        class_id = input("Academic Class: ").strip()
        class_id = class_id if class_id else info['class']['ClassID']

        curriculum_input = input("Curriculum_ID: ").strip()
        curriculum_id = curriculum_input if curriculum_input else info['curriculumID']


        
        if curriculum_id:
            is_valid = AcademicClass.validate_structure(
                self.db, class_id, major, department, curriculum_id
            )
        else:
            is_valid = AcademicClass.validate_structure(
                self.db, class_id, major, department
            )

        if not is_valid:
            print("Invalid class, major, department, or curriculum information")
            return


        update_data = {
            "email": student_email,
            "fullName": full_name,
            "dateofBirth": date_of_birth,
            "educationLevel": education_level,
            "educationType": training_type,
            "status": status,
            "Admissiondate": enrollment_date,
            "Specialization": specialization,
            "courseYear": course,
            "ClassID": class_id,
            "curriculumID": curriculum_id
        }

        success = User.update_student_profile(self.db, info['userID'], update_data)


        if success:
            print("UPDATE SUCCESSFUL")

            # Ví dụ user đang đăng nhập là Admin
            current_user = self.user_id

            # So sánh từng field
            if info['fullName'] != update_data['fullName']:
                self.log(
                    "UPDATE",
                    "Student.FullName",
                    info['fullName'],
                    current_user
                )

            if info['dateofBirth'] != update_data['dateofBirth']:
                self.log(
                    "UPDATE",
                    "Student.dateofBirth",
                    info['dateofBirth'],
                    current_user
                )

            if info['educationLevel'] != update_data['educationLevel']:
                self.log(
                    "UPDATE",
                    "Student.educationLevel",
                    info['educationLevel'],
                    current_user
                )

            if info['educationType'] != update_data['educationType']:
                self.log(
                    "UPDATE",
                    "Student.educationType",
                    info['educationType'],
                    current_user
                )

            if info['Specialization'] != update_data['Specialization']:
                self.log(
                    "UPDATE",
                    "Student.Specialization",
                    info['Specialization'],
                    current_user
                )

            if info['courseYear'] != update_data['courseYear']:
                self.log(
                    "UPDATE",
                    "Student.courseYear",
                    info['courseYear'],
                    current_user
                )

            if info['status'] != update_data['status']:
                self.log(
                    "UPDATE",
                    "Student.Status",
                    info['status'],
                    current_user
                )
                self.deactiveAccount(info['userID'], update_data['status'])

            if info['email'] != update_data['email']:
                self.log(
                    "UPDATE",
                    "Student.Email",
                    info['email'],
                    current_user
                )

            if info['class']['ClassID'] != update_data['ClassID']:
                self.log(
                    "UPDATE",
                    "Student.ClassID",
                    info['class']['ClassID'],
                    current_user
                )

            if info['curriculumID'] != update_data['curriculumID']:
                self.log(
                    "UPDATE",
                    "Student.curriculumID",
                    info['curriculumID'],
                    current_user
                )
            # Cập nhật lại trạng thái đối tượng info sau khi ghi dữ liệu mới vào CSDL
            info.update(update_data)
        else:
            print("UPDATE FAILED")

    def log(self, logtype, log_object, old_Value, user_id):
        LogType = logtype
        LogObject = log_object
        OldValue = old_Value
        ChangeAt = datetime.now()
        User_id = user_id

        log = Log(None, LogType, LogObject, ChangeAt, User_id, OldValue)
        log.add_log(self.db)


    def deleteStudent(self, info: User):
        current_user = self.user_id

        try: 
            self.log(
                "DELETE",
                "Student",
                f"ID={info['userID']}, FullName={info['fullName']}",
                current_user
            )

            success = User.delete_user(self.db, info['userID'])

            if success: 
                print("Student deleted successfully")
            else:
                print("Failed to delete student:")

        except Exception as e:
            print("Failed to delete student:", e)

    def deactiveAccount(self, user_id, new_status):
        if new_status != "STUDY":
            return User.deactivate_account(self.db, user_id)
        return False
    
    def addCourse(self):

        current_user = self.user_id

        while True:
            courseID = input("Enter course id: ").strip()
            existed = Assignment.search_by_courseID(self.db, courseID)
            if not existed:
                print("This course class does not exist!\n")
                continue
            break

        try:
            number_of_student = int(input("Enter the number of students: "))
            if number_of_student <= 0:
                raise ValueError
        except ValueError:
            print("Invalid number of students")
            return

        for i in range(number_of_student):
            while True:
                studentID = input(f"Enter student ID #{i+1}: ").strip()

                # 1️⃣ Check student tồn tại
                student = User.search_user_by_ID(self.db, studentID)
                if not student:
                    print("Student ID does not exist. Please enter again.\n")
                    continue

                # 2️⃣ Check đã có trong lớp học phần chưa
                if Assignment.is_student_assigned(self.db, courseID, studentID):
                    print("The student is already enrolled in this course class.\n")
                    continue

                # 3️⃣ Insert
                assigned = Assignment(courseID, studentID)
                result_assign = assigned.add_assignment_for_student(self.db)
                result_grade = Grade.add_student(self.db, courseID, studentID)

                if result_assign and result_grade:
                    self.log(
                        "ASSIGN",
                        "CourseStudent",
                        f"{courseID}-{studentID}",
                        current_user
                    )
                    break
                else:
                    print(f"Unable to add student {studentID}. Please enter again.\n")


