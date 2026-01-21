# Grade.py
class Grade:
    def __init__(
        self,
        CourseID,
        userID,
        CAscore=None,
        Finalscore=None,
        FinalGrade=None,
        GPA=None,
        LetterGrade=None,
        classification=None,
        Pass=None,
        Notes=None
    ):
        self.CourseID = CourseID
        self.userID = userID
        self.CAscore = CAscore
        self.Finalscore = Finalscore
        self.FinalGrade = FinalGrade
        self.GPA = GPA
        self.LetterGrade = LetterGrade
        self.classification = classification
        self.Pass = Pass
        self.Notes = Notes

    def add_grade(self, db):
        sql = """
        INSERT INTO Grade
        (CourseID, userID, CAscore, Finalscore, FinalGrade, GPA, LetterGrade, classification, Pass, Notes)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        params = (
            self.CourseID,
            self.userID,
            self.CAscore,
            self.Finalscore,
            self.FinalGrade,
            self.GPA,
            self.LetterGrade,
            self.classification,
            self.Pass,
            self.Notes,
        )
        return db.execute_query(sql, params)

    def update_grade(self, db):
        sql = """
        UPDATE Grade SET
          CAscore=%s,
          Finalscore=%s,
          FinalGrade=%s,
          GPA=%s,
          LetterGrade=%s,
          classification=%s,
          Pass=%s,
          Notes=%s
        WHERE CourseID=%s AND userID=%s
        """
        params = (
            self.CAscore,
            self.Finalscore,
            self.FinalGrade,
            self.GPA,
            self.LetterGrade,
            self.classification,
            self.Pass,
            self.Notes,
            self.CourseID,
            self.userID,
        )
        return db.execute_query(sql, params)

    @staticmethod
    def get_all_information(db):
        """
        Dùng lệnh JOIN giữa các bảng:
        Grade + Course + Subject + User
        """
        sql = """
        SELECT
          g.CourseID,
          c.CourseTime,
          c.Startdate,
          c.Enddate,
          s.subjectID,
          s.subjectName,
          s.Credits,
          u.userID,
          u.username,
          u.fullName,
          g.CAscore,
          g.Finalscore,
          g.FinalGrade,
          g.GPA,
          g.LetterGrade,
          g.classification,
          g.Pass,
          g.Notes
        FROM Grade g
        JOIN Course c ON g.CourseID = c.CourseID
        JOIN Subject s ON c.subjectID = s.subjectID
        JOIN `User` u ON g.userID = u.userID
        """
        rows = db.fetch_all(sql)

        result = []
        for r in rows:
            result.append({
                "course": {
                    "CourseID": r[0],
                    "CourseTime": r[1],
                    "Startdate": r[2],
                    "Enddate": r[3],
                    "subject": {
                        "subjectID": r[4],
                        "subjectName": r[5],
                        "Credits": r[6],
                    }
                },
                "student": {
                    "userID": r[7],
                    "username": r[8],
                    "fullName": r[9],
                },
                "grade": {
                    "CAscore": r[10],
                    "Finalscore": r[11],
                    "FinalGrade": r[12],
                    "GPA": r[13],
                    "LetterGrade": r[14],
                    "classification": r[15],
                    "Pass": r[16],
                    "Notes": r[17],
                }
            })
        return result
