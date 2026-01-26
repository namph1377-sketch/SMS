from Database.Connect import Database
from Database.Grade import Grade
from Database.Course import Course
from Database.Assignment import Assignment
from Database.Log import Log
#from debug import debug
from datetime import datetime

class Teacher:
    def __init__(self, userID):
        self.db = Database()
        self.userID = userID
    # Hàm ánh xạ giờ với ca
    def get_shift(self, hour, minute):
        time_in_minutes = hour * 60 + minute

        SHIFT_TABLE = {
            1: range(6*60+45, 9*60+15+1),
            2: range(9*60+25, 11*60+55+1),
            3: range(12*60+10, 14*60+40+1),
            4: range(14*60+50, 17*60+20+1),
            5: range(17*60+30, 20*60+1+1),
        }

        for shift, minutes in SHIFT_TABLE.items():
            if time_in_minutes in minutes:
                return shift
        return None  
    def ViewSchedule(self):
        schedules = Course.get_all_information(self.db)

        if not schedules:
            print("No schedule found")
            return

        day_order = {
            "Monday": 1,
            "Tuesday": 2,
            "Wednesday": 3,
            "Thursday": 4,
            "Friday": 5,
            "Saturday": 6,
            "Sunday": 7
        }

        schedule_sorted = sorted(
            schedules,
            key=lambda s: (
                day_order.get(s["CourseTime"].strftime("%A"), 99),
                self.get_shift(
                    s["CourseTime"].hour,
                    s["CourseTime"].minute
                ) or 99
            )
        )

        # header
        print(f"{'Weekday':<10} | {'Shift':^12} | {'Subject':<35} | CourseID")
        print("-" * 70)

        for s in schedule_sorted:
            dt = s["CourseTime"]

            weekday = dt.strftime("%A")
            shift = self.get_shift(dt.hour, dt.minute)
            shift = shift if shift is not None else "N/A"

            subject_name = s["subject"]["subjectName"]

            print(
                f"{weekday:<10} | {shift:^12} | "
                f"{subject_name:<35} | {s['CourseID']}"
            )


    def searchbyCourseID(self):
        CourseID = input("Enter Course ID: ").strip()
        data = Assignment.search_by_courseID(self.db, CourseID)
        return data
    
    def choose_student_from_list(self, assignments: list[Assignment]):
        if not assignments:
            return None

        try:
            choice = int(input("Enter student number to update grades: "))
            if 1 <= choice <= len(assignments):
                return assignments[choice - 1]
        except ValueError:
            pass

        print("Invalid choice")
        return None

    def preView(self):
        sche = Course.get_all_information(self.db)

        print(f"{'Course ID':<20} | {'Subject Name'}")
        print("-" * 45)

        for s in sche:
            subject_name = s["subject"]["subjectName"]
            print(f"{s['CourseID']:<20} | {subject_name}")


    def ViewStudentList(self, info: list[dict]):
        print(
            f"{'No':<3} | {'Student ID':<12} | {'Fullname':<25} | "
            f"{'CA Score':<10} | {'Final Score':<10} | {'Final grade':<10} | {'Notes'}"
        )

        for idx, g in enumerate(info, start=1):
            user = g["user"]
            grade = g["grade"] or {}

            print(
                f"{idx:<3} | "
                f"{user['userID']:<12} | "
                f"{user['fullName']:<25} | "
                f"{grade.get('CAscore', ''):<10} | "
                f"{grade.get('Finalscore', ''):<10} | "
                f"{grade.get('FinalGrade', ''):<10} | "
                f"{grade.get('Notes', '')}"
            )


    def calculate_grade(self, ca_score, final_score):
        final_grade = round(ca_score * 0.4 + final_score * 0.6, 2)

        if final_grade >= 8.5:
            letter = "A"
            gpa = 4.0
            classification = "Excellent"
        elif final_grade >= 7.0:
            letter = "B"
            gpa = 3.0
            classification = "Good"
        elif final_grade >= 5.5:
            letter = "C"
            gpa = 2.0
            classification = "Average"
        elif final_grade >= 4.0:
            letter = "D"
            gpa = 1.0
            classification = "Weak"
        else:
            letter = "F"
            gpa = 0.0
            classification = "Poor"

        passed = final_grade >= 4.0

        return final_grade, gpa, letter, classification, passed


    # Ngoài hàm cập nhật điểm thì cần hàm xem danh sách sinh viên + hàm để lưu thay đổi vào Log
    def addGrade(self, CourseID, userID):
        # Lấy điểm cũ (nếu có)
        old_grade = Grade.get_grade(self.db, CourseID, userID)

        old_ca = old_grade["CAscore"] if old_grade else None
        old_final = old_grade["Finalscore"] if old_grade else None
        print("\n--- Update Grade ---")

        print("(Press ENTER to keep current value, type 'q' to cancel)")

        # ===== nhập CA score =====
        while True:
            raw = input("Enter CA score: ").strip()

            if raw.lower() == "q":
                print("Grade update cancelled")
                return

            if raw == "":
                CAScore = old_ca
                break

            try:
                CAScore = float(raw)
                if 0 <= CAScore <= 10:
                    break
                print("Score must be between 0 and 10")
            except ValueError:
                print("Invalid score")

        # ===== nhập Final score =====
        while True:
            raw = input("Enter Final score: ").strip()

            if raw.lower() == "q":
                print("Grade update cancelled")
                return

            if raw == "":
                Finalscore = old_final
                break

            try:
                Finalscore = float(raw)
                if 0 <= Finalscore <= 10:
                    break
                print("Score must be between 0 and 10")
            except ValueError:
                print("Invalid score")

        Notes = input("Enter note (Press ENTER to keep current value): ").strip()
        if Notes == "" and old_grade:
            Notes = old_grade.get("Notes", "")

        # Nếu vẫn chưa có đủ điểm thì không cho lưu
        if CAScore is None or Finalscore is None:
            print("Not enough scores to calculate the result")
            return

        FinalGrade, GPA, LetterGrade, classification, Pass = \
            self.calculate_grade(CAScore, Finalscore)

        grade = Grade(
            CourseID,
            userID,
            CAScore,
            Finalscore,
            FinalGrade,
            GPA,
            LetterGrade,
            classification,
            Pass,
            Notes
        )

        success = grade.update_grade(self.db)

        if success:
            print("Grade updated successfully")
            self.log(
                "UPDATE",
                "FinalGrade",
                f"Updated FinalGrade to {FinalGrade}"
            )

        else:
            print("Failed to update grade")


    def log(self, LogType, LogObject, OldValue=None):
        log = Log(
            LogID=None,
            LogType=LogType,
            LogObject=LogObject,
            OldValue=OldValue,
            ChangeAt=datetime.now(),
            userID=self.userID
        )
        log.add_log(self.db)
