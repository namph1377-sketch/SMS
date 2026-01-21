
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
