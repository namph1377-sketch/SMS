from Service.Teacher import Teacher
from getpass import getpass
from Database.Assignment import Assignment
from UI.Auth_UI import UIAuth


class Teacher_UI:
    def __init__(self):
        self.teacher = Teacher()

    def pause(self):
        input("\nPress [ENTER] to continue...")

    def show_menu(self):
        print("\n============= TEACHER MENU ===========")
        print("1. View teaching schedule")
        print("2. View student list by course")
        print("3. Change your password")
        print("4. Log out")

    # ====== FUNCTION 1 ======
    def view_schedule(self):
        print("\n------------- View teaching schedule -------------")
        self.teacher.ViewSchedule()
        self.pause()

    # ====== FUNCTION 2 ======
    def view_student_list_by_course(self):
        while True:
            print("\n------------- View student list by course-------------")
            print("List of course section")
            self.teacher.preView()

            print("\n[1] Enter Course ID")
            print("[2] Return to teacher menu")
            choice = input("-> ").strip()

            if choice == "2":
                return

            if choice != "1":
                print("Invalid choice")
                continue

            course_id = input("Enter Course ID: ").strip()
            assignments = Assignment.search_by_courseID(
                self.teacher.db, course_id
            )

            if not assignments:
                print("No student found for this course")
                self.pause()
                continue

            print(f"\n=> Course section CURRENTLY OPEN: {course_id}")
            print("\nStudent list")
            self.teacher.ViewStudentList(assignments)

            # chọn sinh viên
            student = self.teacher.choose_student_from_list(assignments)
            if not student:
                self.pause()
                continue

            print(f"\nUpdating for: {student.fullname} ({student.userID})")

            # cập nhật điểm
            self.teacher.addGrade(student.CourseID, student.userID)

            # confirm quay lại
            self.pause()
            return

    # ====== FUNCTION 3 ======
    def change_password(self):
        UIAuth.ui_change_password()

    # ====== FUNCTION 4 ======
    def logout(self):
        UIAuth.ui_logout()

    # ====== MAIN LOOP ======
    def run(self):
        while True:
            self.show_menu()
            choice = input("Select function: ").strip()

            if choice == "1":
                self.view_schedule()
            elif choice == "2":
                self.view_student_list_by_course()
            elif choice == "3":
                self.change_password()
            elif choice == "4":
                confirm = input(
                    "Are you sure you want to log out of the system? (y/n): "
                ).lower()
                if confirm == "y":
                    print("Logged out successfully")
                    return
            else:
                print("Invalid selection")
