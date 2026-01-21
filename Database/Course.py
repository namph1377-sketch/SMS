class Course:
    def __init__(self, CourseID, CourseTime, Startdate, Enddate, subjectID):
        self.CourseID = CourseID
        self.CourseTime = CourseTime
        self.Startdate = Startdate
        self.Enddate = Enddate
        self.subjectID = subjectID

    @staticmethod
    def get_all_information(db):
        query = """
        SELECT
          co.CourseID,
          co.CourseTime,
          co.Startdate,
          co.Enddate,
          co.subjectID,
          s.subjectName,
          s.Credits,
          a.userID,
          u.username,
          u.fullName,
          u.email,
          u.Role,
          u.isActive
        FROM Course co
        LEFT JOIN Subject s ON co.subjectID = s.subjectID
        LEFT JOIN Assignment a ON co.CourseID = a.CourseID
        LEFT JOIN `User` u ON a.userID = u.userID
        ORDER BY co.CourseID
        """
        rows = db.fetch_all(query)

        # Group rows by CourseID
        courses = {}
        for r in rows:
            course_id = r[0]
            if course_id not in courses:
                courses[course_id] = {
                    "CourseID": r[0],
                    "CourseTime": r[1],
                    "Startdate": r[2],
                    "Enddate": r[3],
                    "subject": {
                        "subjectID": r[4],
                        "subjectName": r[5],
                        "Credits": r[6],
                    },
                    "participants": []
                }

            user_id = r[7]
            if user_id is not None:
                user_obj = {
                    "userID": r[7],
                    "username": r[8],
                    "fullName": r[9],
                    "email": r[10],
                    "role": r[11],
                    "is_active": r[12],
                }
                courses[course_id]["participants"].append(user_obj)

        return list(courses.values())
