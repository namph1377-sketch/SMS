# Assignment.py
class Assignment:
    def __init__(self, CourseID, userID):
        self.CourseID = CourseID
        self.userID = userID

    def add_assignment_for_student(self, db):
        query = "INSERT INTO Assignment (CourseID, userID) VALUES (%s, %s)"
        return db.execute_query(query, (self.CourseID, self.userID))

    @staticmethod
    def get_all_information(db):
        query = """
        SELECT
          a.CourseID,
          u.userID,
          u.username,
          u.fullName,
          u.email,
          u.Role,
          u.isActive
        FROM Assignment a
        JOIN `User` u ON a.userID = u.userID
        """
        rows = db.fetch_all(query)

        result = []
        for r in rows:
            result.append({
                "CourseID": r[0],
                "user": {
                    "userID": r[1],
                    "username": r[2],
                    "fullName": r[3],
                    "email": r[4],
                    "role": r[5],
                    "is_active": r[6],
                }
            })
        return result

    @staticmethod
    def search_by_courseID(db, CourseID):
        """
        Lấy tất cả assignment cho CourseID:
        JOIN Assignment a
             LEFT JOIN `User` u ON a.userID = u.userID
             LEFT JOIN Grade g ON a.CourseID = g.CourseID AND a.userID = g.userID
        Trả về list các record gồm thông tin user + (nếu có) grade.
        """
        query = """
        SELECT
          a.CourseID,
          u.userID,
          u.username,
          u.fullName,
          u.email,
          u.Role,
          u.isActive,
          g.CAscore,
          g.Finalscore,
          g.FinalGrade,
          g.GPA,
          g.LetterGrade,
          g.classification,
          g.Pass,
          g.Notes
        FROM Assignment a
        LEFT JOIN `User` u ON a.userID = u.userID
        LEFT JOIN Grade g ON a.CourseID = g.CourseID AND a.userID = g.userID
        WHERE a.CourseID = %s
        ORDER BY u.userID
        """
        rows = db.fetch_all(query, (CourseID,))

        result = []
        for r in rows:
            user_obj = {
                "userID": r[1],
                "username": r[2],
                "fullName": r[3],
                "email": r[4],
                "role": r[5],
                "is_active": r[6],
            }

            grade = None
            # if no grade row, g.CAscore (r[7]) will be None
            if r[7] is not None or r[8] is not None or r[9] is not None or r[10] is not None or r[11] is not None or r[12] is not None or r[13] is not None or r[14] is not None:
                grade = {
                    "CAscore": r[7],
                    "Finalscore": r[8],
                    "FinalGrade": r[9],
                    "GPA": r[10],
                    "LetterGrade": r[11],
                    "classification": r[12],
                    "Pass": r[13],
                    "Notes": r[14],
                }

            result.append({
                "CourseID": r[0],
                "user": user_obj,
                "grade": grade,
            })

        return result
