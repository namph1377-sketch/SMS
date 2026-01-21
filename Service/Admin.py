from Database.Connect import Database
from Database.User import User
from Database.ProfileStudent import ProfileStudent
from Database.Assignment import Assignment
from Database.Log import Log
from debug import debug
from datetime import datetime

class Admin:
    def __init__(self):
        self.db = Database()

    def createStudent(self):
        student_id = input("Citizen identification number: ").strip()
        full_name = input("Full name: ").strip()
        date_of_birth = input("Date of birth: ").strip()
        education_level = input("Education level: ").strip()
        training_type = input("Training type: ").strip()
        major = input("Major: ").strip()
        specialization = input("Specialization: ").strip()
        department = input("Department: ").strip()
        course = input("CourseYear: ").strip()
        enrollment_date = input("Enrollment date: ").strip()
        status = input("status: ").strip()
        personal_email = input("Personal email: ").strip()
        class_id = input("Academic Class: ").strip()

        user = User(student_id, student_id, student_id, None, "Stu", "1", 
                    full_name, date_of_birth, education_level, training_type, 
                    status, enrollment_date, specialization, course, class_id, None)
        profile = ProfileStudent(student_id, None, None, personal_email, 
                                 None, None, None, None, None, None, None, 
                                 None, None, None, None, None, None)
        user.add_user(self.db)
        profile.add_profile_student(self.db)

    def choose_student_from_list(self, students):
        print("\n=== DANH SÁCH SINH VIÊN ===")
        for i, s in enumerate(students, start=1):
            print(f"{i}. {s[0]} - {s[2]}")  # ID - FullName

        try:
            choice = int(input("Chọn số thứ tự: "))
            if 1 <= choice <= len(students):
                return User(*students[choice - 1])
        except ValueError:
            pass

        print("Lựa chọn không hợp lệ")
        return None


    def searchStudent(self):
        keyword = input("Keyword: ").strip()

        if keyword.isdigit():
            data = User.search_user_by_ID(self.db, keyword)
            return User(*data) if data else None

        elif keyword.replace(" ", "").isalpha():
            results = User.search_user_by_Name(self.db, keyword)
            if not results:
                print("Không tìm thấy sinh viên")
                return None

            return self.choose_student_from_list(results)

        else:
            print("Keyword không hợp lệ")
            return None

    def choose_status(self):
        print("\nChọn trạng thái học tập:")
        print("[1] Currently studying")
        print("[2] Reserved")
        print("[3] Graduation")
        print("[4] Forced expulsion")
        print("[Enter] Bỏ qua")

        choice = input("Lựa chọn: ").strip()

        status_map = {
            "1": "Currently studying",
            "2": "Reserved",
            "3": "Graduation",
            "4": "Forced expulsion"
        }

        return status_map.get(choice, None)

    def searchStudentByFilter(self):
        print("\n=== TÌM KIẾM THEO BỘ LỌC ===")

        department = input("Department (Enter để bỏ qua): ").strip()
        academic_class = input("Academic Class (Enter để bỏ qua): ").strip()
        status = self.choose_status()

        # không được trống cả 3
        if not department and not academic_class and not status:
            print("Phải nhập ít nhất 1 điều kiện")
            return None

        results = User.search_user_by_filler(
            self.db,
            department=department or None,
            academic_class=academic_class or None,
            status=status
        )

        if not results:
            print("Không tìm thấy sinh viên phù hợp")
            return None

        return self.choose_student_from_list(results)

    def viewStudentDetail(self, info: User):
        print("EDUCATIONAL INFORMATION")
        print(f"Full name: {info.fullname}")
        print(f"Student ID: {info.userID}")
        print(f"Date of birth: {info.dateofBirth}")
        print(f"Education level: {info.educationLevel}")
        print(f"Training type: {info.educationType}")
        print(f"Department: {info.department}")
        print(f"Major: {info.major}")
        print(f"Specialization: {info.specialization}")
        print(f"Coure: {info.courseYear}")
        print(f"status: {info.status}")
        print(f"Student Email: {info.email}")
        print(f"Enrollment date: {info.Admissiondate}")
        print(f"Academic Class: {info.ClassID}")

        print("\nDETAILED PERSONAL INFORMATION")
        print(f"Sex: {info.gender}")
        print(f"Phone number: {info.phone}")
        print(f"Emergency contact: {info.emergencyPhone}")
        print(f"Personal email: {info.personalEmail}")
        print(f"Ethnicity: {info.ethnicity}")
        print(f"Religion: {info.religion}")
        print(f"Nationality: {info.Nationality}")
        print(f"Youth Union entry date: {info.joinUnionDate}")
        print(f"Party entry date: {info.joinPartyDate}")

        print("\nDOCUMENTATION & INSURANCE INFORMATION")
        print(f"Citizen Identification Number: {info.nationId}")
        print(f"Health insurance ID: {info.insuranceCode}")
        print(f"Initial medical facility: {info.initialHospital}")
        print(f"Place of birth: {info.placeOfBirth}")
        print(f"Hometown: {info.hometown}")
        print(f"Permanent: {info.permanentResidence}")
        print(f"Bank account information: {info.bankAccount}")
    

    def updateStudent(self, info: User):
        print("THÔNG TIN HIỆN TẠI")
        print(f"Full name: {info.fullname}")
        print(f"Student ID: {info.userID}")
        print(f"Date of birth: {info.dateofBirth}")
        print(f"Education level: {info.educationLevel}")
        print(f"Training type: {info.educationType}")
        print(f"Department: {info.department}")
        print(f"Major: {info.major}")
        print(f"Specialization: {info.specialization}")
        print(f"CourseYear: {info.courseYear}")
        print(f"Student Email: {info.email}")
        print(f"Enrollment date: {info.Admissiondate}")
        print(f"status: {info.status}")
        print(f"Academic Class: {info.ClassID}")
        print(f"Curriculum_ID: {info.curriculumID}")

        print("\n=== NHẬP THÔNG TIN MỚI (Enter để giữ nguyên) ===")
        full_name = input("Full name: ").strip()
        date_of_birth = input("Date of birth: ").strip()
        education_level = input("Education level: ").strip()
        training_type = input("Training type: ").strip()
        major = input("Major: ").strip()
        specialization = input("Specialization: ").strip()
        department = input("Department: ").strip()
        course = input("CourseYear: ").strip()
        enrollment_date = input("Enrollment date: ").strip()
        status = input("status: ").strip()
        student_email = input("Student email: ").strip()
        class_id = input("Academic Class: ").strip()
        curriculum_id = input("Curriculum_ID: ").strip()

        updated = User(info.userID, 
                        full_name if full_name else info.fullname,
                        date_of_birth if date_of_birth else info.dateofBirth,
                        education_level if education_level else info.educationLevel,
                        training_type if training_type else info.educationType,
                        specialization if specialization else info.specialization,
                        course if course else info.courseYear,
                        enrollment_date if enrollment_date else info.Admissiondate,
                        status if status else info.status,
                        student_email if student_email else info.email,
                        class_id if class_id else info.ClassID,
                        curriculum_id if curriculum_id else info.curriculumID)
        success = updated.update_user(self.db)

        if success:
            print("Cập nhật thành công")

            # Ví dụ user đang đăng nhập là Admin
            current_user = "ADMIN"

            # So sánh từng field
            if info.fullname != updated.fullname:
                self.log(
                    "UPDATE",
                    "Student.FullName",
                    info.fullname,
                    current_user
                )

            if info.dateofBirth != updated.dateofBirth:
                self.log(
                    "UPDATE",
                    "Student.dateofBirth",
                    info.dateofBirth,
                    current_user
                )

            if info.educationLevel != updated.educationLevel:
                self.log(
                    "UPDATE",
                    "Student.educationLevel",
                    info.educationLevel,
                    current_user
                )

            if info.educationType != updated.educationType:
                self.log(
                    "UPDATE",
                    "Student.educationType",
                    info.educationType,
                    current_user
                )

            if info.specialization != updated.specialization:
                self.log(
                    "UPDATE",
                    "Student.specialization",
                    info.specialization,
                    current_user
                )

            if info.courseYear != updated.courseYear:
                self.log(
                    "UPDATE",
                    "Student.courseYear",
                    info.courseYear,
                    current_user
                )

            if info.status != updated.status:
                self.log(
                    "UPDATE",
                    "Student.Status",
                    info.status,
                    current_user
                )
                self.deactiveAccount(updated)

            if info.email != updated.email:
                self.log(
                    "UPDATE",
                    "Student.Email",
                    info.email,
                    current_user
                )

            if info.ClassID != updated.ClassID:
                self.log(
                    "UPDATE",
                    "Student.ClassID",
                    info.ClassID,
                    current_user
                )

            if info.curriculumID != updated.curriculumID:
                self.log(
                    "UPDATE",
                    "Student.curriculumID",
                    info.curriculumID,
                    current_user
                )
            # Cập nhật lại trạng thái đối tượng info sau khi ghi dữ liệu mới vào CSDL
            info.__dict__.update(updated.__dict__)
        else:
            print("Cập nhật thất bại")

    def log(self, logtype, log_object, old_Value, user_id):
        LogType = logtype
        LogObject = log_object
        OldValue = old_Value
        ChangeAt = datetime.now()
        User_id = user_id

        log = Log(None, LogType, LogObject, OldValue, ChangeAt, User_id)
        log.add_log(self.db)


    def deleteStudent(self, info: User):
        success = info.delete_user(self.db)
        if success:
            self.log(
                "DELETE",
                "Student",
                f"ID={info.userID}, FullName={info.fullname}",
                "ADMIN"
            )
            print("Xóa sinh viên thành công")
        else:
            print("Xóa sinh viên thất bại")

    def deactiveAccount(self, info: User):
        if info.status != "Currently studying":
            info.isActive = 0
            return info.update_user(self.db)
        return False
    
    def addCourse(self):
        courseID = input("Enter course id: ").strip()

        try:
            number_of_student = int(input("Enter the number of students: "))
        except ValueError:
            print("Số lượng sinh viên không hợp lệ")
            return

        for i in range(number_of_student):
            studentID = input(f"Enter student ID #{i+1}: ").strip()

            assigned = Assignment(courseID, studentID)

            if assigned.add_assignment_for_student(self.db):
                self.log("ASSIGN", "CourseStudent", f"{courseID}-{studentID}", "ADMIN")
            else:
                print(f"Không thể thêm sinh viên {studentID}")

