from Database.Connect import Database
from Database.User import User
from Database.ProfileStudent import ProfileStudent
from Database.Contain import Contain
from Database.Grade import Grade
from Database.Course import Course
from Database.Log import Log
from debug import debug
from datetime import datetime


class Student:
    # Hàm khởi tạo
    def __init__(self, user_id):
        self.db = Database()
        self.user = User(self.db)
        self.profile = ProfileStudent(self.db)
        self.contain = Contain(self.db)
        self.grade = Grade(self.db)
        self.course = Course(self.db)
        self.log = Log(self.db)

        self.user_id = user_id
        self.student_id = self.user.get_student_id(user_id)

    # 1. Xem hồ sơ cá nhân
    def viewProfile(self):
        return self.profile.get_by_student_id(self.student_id)

    # 2. Cập nhật thông tin cá nhân (chỉ personal info)
    # Ngoài hàm cập nhật thì cần gọi hàm để lưu thay đổi vào Log
    def updateProfile(self, new_data: dict):
        old_data = self.profile.get_by_student_id(self.student_id)
        if not old_data:
            return False

        if "personal_email" in new_data and "@" not in new_data["personal_email"]:
            return False

        success = self.profile.update_personal_info(self.student_id, new_data)

        if success:
            self.log.insert(
                user_id=self.user_id,
                action="UPDATE_PERSONAL_INFO",
                object_id=self.student_id,
                old_data=old_data,
                new_data=new_data,
                timestamp=datetime.now()
            )
        return success


    # 3. Xem chương trình đào tạo
    def viewCurriculum(self):
        profile = self.profile.get_by_student_id(self.student_id)
        if not profile:
            return None

        return self.course.get_curriculum(
            profile.get("major"),
            profile.get("education_level")
        )

    # 4. Xem điểm
    def viewGrade(self):
        return self.grade.get_by_student_id(self.student_id)


    # 5. Xem thời khóa biểu
    def ViewSchedule(self):
        return self.contain.get_schedule_by_student_id(self.student_id)

