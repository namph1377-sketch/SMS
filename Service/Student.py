from Database.Connect import Database
from Database.User import User 
from Database.StudentProfile import StudentProfile
from Database.Contain import Contain
from Database.Grade import Grade
from Database.Course import Course
from Database.Log import Log
#from debug import debug
from datetime import datetime


class Student:
    def __init__(self, user_id):
        self.db = Database()
        self.user_id = user_id   

    def viewProfile(self): 
        
        return User.search_user_by_ID(self.db, self.user_id)  

    def updateProfile(self, new_data: dict):
        user_info = User.search_user_by_ID(self.db, self.user_id)
        if not user_info:
            return False

        old_profile = user_info.get("profile", {})

        # Validate email
        if "personal_email" in new_data and new_data.get("personal_email"):
            if "@" not in new_data["personal_email"]:
                return False

        mapped_data = {
            "phone": new_data.get("phone_number"),
            "emergencyPhone": new_data.get("emergency_contact"),
            "personalEmail": new_data.get("personal_email"),
            "ethnicity": new_data.get("ethnicity"),
            "religion": new_data.get("religion"),
            "Nationality": new_data.get("nationality"),
            "joinUnionDate": new_data.get("youth_union_date"),
            "joinPartyDate": new_data.get("party_date"),
            "nationalId": new_data.get("citizen_id"),
            "insuranceCode": new_data.get("health_insurance_id"),
            "initialHospital": new_data.get("initial_medical_facility"),
            "placeOfBirth": new_data.get("place_of_birth"),
            "hometown": new_data.get("hometown"),
            "permanentResidence": new_data.get("permanent_residence"),
            "bankAccount": new_data.get("bank_account"),
        }

        # Loại bỏ None
        mapped_data = {k: v for k, v in mapped_data.items() if v is not None}

        updated = {**old_profile, **mapped_data}

        profile = StudentProfile(
            userID=self.user_id,
            phone=updated.get("phone"),
            emergencyPhone=updated.get("emergencyPhone"),
            personalEmail=updated.get("personalEmail"),
            ethnicity=updated.get("ethnicity"),
            religion=updated.get("religion"),
            Nationality=updated.get("Nationality"),
            joinUnionDate=updated.get("joinUnionDate"),
            joinPartyDate=updated.get("joinPartyDate"),
            nationalId=updated.get("nationalId"),
            insuranceCode=updated.get("insuranceCode"),
            initialHospital=updated.get("initialHospital"),
            placeOfBirth=updated.get("placeOfBirth"),
            hometown=updated.get("hometown"),
            permanentResidence=updated.get("permanentResidence"),
            gender=updated.get("gender"),
            bankAccount=updated.get("bankAccount"),
        )

        success = profile.update_student_profile(self.db)
        if not success:
            return False

        # ====== GHI LOG THEO TỪNG FIELD ======
        current_user = self.user_id

        for field in mapped_data:
            old_value = old_profile.get(field)
            new_value = updated.get(field)

            if old_value != new_value:
                log = Log(
                    LogID=None,
                    LogType="UPDATE",
                    LogObject="StudentProfile",
                    ChangeAt=datetime.now(),
                    userID=current_user,
                    OldValue=str(old_value)
                )
                log.add_log(self.db)

        return True


    def viewCurriculum(self):
        user_info = User.search_user_by_ID(self.db, self.user_id)
        if not user_info or not user_info.get("curriculumID"):
            return {}

        curriculum_id = user_info["curriculumID"]
        rows = Contain.get_all_curriculum_information(self.db)

        curriculum = {}

        for r in rows:
            if r["curriculumID"] != curriculum_id:
                continue

            semester = r["semester"]

            if semester not in curriculum:
                curriculum[semester] = []

            curriculum[semester].append(r["subject"])

        return curriculum

    def viewSchedule(self):
        all_courses = Course.get_all_information(self.db)
        result = []

        for c in all_courses:
            participants = [p["userID"] for p in c["participants"]]
            if self.user_id in participants:
                result.append(c)

        return result

    def viewGrade(self):
        all_grades = Grade.get_all_information(self.db)
        return [
            g for g in all_grades
            if g["student"]["userID"] == self.user_id
        ]
