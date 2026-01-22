from Database.Connect import Database
from Database.Grade import Grade
from Database.Course import Course
from Database.Assignment import Assignment
from Database.Log import Log
from debug import debug
from datetime import datetime

class Teacher:
    def __init__(self):
        self.db = Database()

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
        
        # Thứ tự ngày trong tuần
        day_order = {
            "Monday": 1,
            "Tuesday": 2,
            "Wednesday": 3,
            "Thursday": 4,
            "Friday": 5,
            "Saturday": 6,
            "Sunday": 7
        }

        # Sắp xếp: theo ngày → theo ca
        schedule_sorted = sorted(
            schedules,
            key=lambda s: (
                day_order.get(s.CourseTime.strftime("%A"), 99),
                self.get_shift(s.CourseTime.hour, s.CourseTime.minute)
            )
        )

        print(f"{'Day':<10} | {'Course Time':<12} | {'Subject':<20} | {'Course ID'}")

        for s in schedule_sorted:
            dt = s.CourseTime
            weekday = dt.strftime("%A")
            shift = self.get_shift(dt.hour, dt.minute)
            print(f"{weekday:<10} | {shift:^12} | {s.subjectName:<20} | {s.CourseID}")

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

        print("Lựa chọn không hợp lệ")
        return None

    def preView(self):
        sche = Course.get_all_information(self.db)
        print(f"{'Course ID':<20} | {'SubjectName'}")
        for s in sche:
            print(f"{s.CourseID:<20} | {s.subjectName}")

    def ViewStudentList(self, info: list[Assignment]):
        print(
            f"{'No':<3} | {'Student ID':<12} | {'Fullname':<25} | {'CA Score':<10} | "
            f"{'Final Score':<10} | {'Final grade':<10} | {'Notes'}"
        )
        for idx, g in enumerate(info, start=1):
            print(
            f"{idx:<3} | {g.userID:<12} | {g.fullname:<25} | {g.CAscore:<10} | "
            f"{g.Finalscore:<10} | {g.FinalGrade:<10} | {g.Notes}"
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
        try:
            CAScore = float(input("Enter CA score: "))
            Finalscore = float(input("Enter Final score: "))
            if not (0 <= CAScore <= 10 and 0 <= Finalscore <= 10):
                print("Điểm phải nằm trong khoảng 0–10")
                return
        except ValueError:
            print("Điểm không hợp lệ")
            return

        Notes = input("Enter a note: ").strip()

        FinalGrade, GPA, LetterGrade, classification, Pass = \
            self.calculate_grade(CAScore, Finalscore)

        # Lưu DB
        grade = Grade(CourseID, userID, CAScore, Finalscore, FinalGrade,
                      GPA, LetterGrade, classification, Pass, Notes)
        success = grade.update_grade(self.db)

        if success:
            print("Cập nhật điểm thành công")

            # Ghi log
            self.log(
                "UPDATE",
                "Student.Grade",
                f"Updated FinalGrade to {grade.FinalGrade}",
                "TEACHER"
            )
        else:
            print("Cập nhật điểm thất bại")

    def log(self, log_type, log_object, old_value, user_id):
        LogType = log_type
        LogObject = log_object
        OldValue = old_value
        ChangeAt = datetime.now()
        userID = user_id

        log = Log(None, LogType, LogObject, OldValue, ChangeAt, userID)
        log.add_log(self.db)

