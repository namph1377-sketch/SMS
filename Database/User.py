class User:
    def __init__(
        self,
        userID,
        username,
        password,
        email,
        Role,
        isActive,
        fullName,
        dateofBirth,
        educationLevel=None,
        educationType=None,
        status=None,
        Admissiondate=None,
        Specialization=None,
        courseYear=None,
        ClassID=None,
        curriculumID=None,
        CourseID=None,
    ):
        # required fields
        self.userID = userID
        self.username = username
        self.password = password
        self.email = email
        self.Role = Role
        self.isActive = isActive
        self.fullName = fullName
        self.dateofBirth = dateofBirth

        # optional fields
        self.educationLevel = educationLevel
        self.educationType = educationType
        self.status = status
        self.Admissiondate = Admissiondate
        self.Specialization = Specialization
        self.courseYear = courseYear

        self.ClassID = ClassID
        self.curriculumID = curriculumID
        self.CourseID = CourseID


    def add_user(self, db):
        sql = """
        INSERT INTO `User`
        (userID, username, password, email, Role, isActive, fullName, dateofBirth,
         educationLevel, educationType, status, Admissiondate, Specialization, courseYear,
         ClassID, curriculumID, CourseID)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,
                %s,%s,%s,%s,%s,%s,
                %s,%s,%s)
        """
        params = (
            self.userID,
            self.username,
            self.password,
            self.email,
            self.Role,
            self.isActive,
            self.fullName,
            self.dateofBirth,
            self.educationLevel,
            self.educationType,
            self.status,
            self.Admissiondate,
            self.Specialization,
            self.courseYear,
            self.ClassID,
            self.curriculumID,
            self.CourseID,
        )
        return db.execute_query(sql, params)

    def update_user(self, db):
        sql = """
        UPDATE `User` SET
          username=%s,
          password=%s,
          email=%s,
          Role=%s,
          isActive=%s,
          fullName=%s,
          dateofBirth=%s,
          educationLevel=%s,
          educationType=%s,
          status=%s,
          Admissiondate=%s,
          Specialization=%s,
          courseYear=%s,
          ClassID=%s,
          curriculumID=%s,
          CourseID=%s
        WHERE userID=%s
        """
        params = (
            self.username,
            self.password,
            self.email,
            self.Role,
            self.isActive,
            self.fullName,
            self.dateofBirth,
            self.educationLevel,
            self.educationType,
            self.status,
            self.Admissiondate,
            self.Specialization,
            self.courseYear,
            self.ClassID,
            self.curriculumID,
            self.CourseID,
            self.userID,
        )
        return db.execute_query(sql, params)

    @staticmethod
    def delete_user(db, userID):
        sql = "DELETE FROM `User` WHERE userID=%s"
        return db.execute_query(sql, (userID,))

    # ------------- AUTH / ACCOUNT -------------
    @staticmethod
    def find_by_email(db, email):
        """
        Lấy thông tin user theo email (email là UNIQUE trong DB)
        Trả về dict hoặc None
        """
        sql = """
        SELECT
          userID, username, password, email, Role, isActive, fullName, dateofBirth,
          educationLevel, educationType, status, Admissiondate, Specialization, courseYear,
          ClassID, curriculumID, CourseID
        FROM `User`
        WHERE email=%s
        """
        row = db.fetch_one(sql, (email,))
        if not row:
            return None

        return {
            "userID": row[0],
            "username": row[1],
            "password": row[2],  # password đã hash trong DB
            "email": row[3],
            "Role": row[4],
            "isActive": row[5],
            "fullName": row[6],
            "dateofBirth": row[7],
            "educationLevel": row[8],
            "educationType": row[9],
            "status": row[10],
            "Admissiondate": row[11],
            "Specialization": row[12],
            "courseYear": row[13],
            "ClassID": row[14],
            "curriculumID": row[15],
            "CourseID": row[16],
        }

    @staticmethod
    def update_password(db, email, new_hashed_password):
        """
        Cập nhật password theo email
        new_hashed_password: mật khẩu đã được hash ở tầng service/controller
        """
        sql = "UPDATE `User` SET password=%s WHERE email=%s"
        return db.execute_query(sql, (new_hashed_password, email))

    # ------------- Searches & joins -------------
    @staticmethod
    def search_user_by_ID(db, userID):
        """
        Ngoài những thông tin cơ bản cần Select,
        Hãy lấy thêm những thông tin sau: role, is_active
        """
        sql = """
        SELECT userID, username, fullName, email, Role, isActive, dateofBirth, ClassID, curriculumID, CourseID
        FROM `User`
        WHERE userID = %s
        """
        r = db.fetch_one(sql, (userID,))
        if not r:
            return None

        return {
            "userID": r[0],
            "username": r[1],
            "fullName": r[2],
            "email": r[3],
            "role": r[4],
            "is_active": r[5],
            "dateofBirth": r[6],
            "ClassID": r[7],
            "curriculumID": r[8],
            "CourseID": r[9],
        }

    @staticmethod
    def search_user_by_Name(db, fullName):
        sql = """
        SELECT userID, username, fullName, email, Role, isActive, dateofBirth, ClassID, curriculumID, CourseID
        FROM `User`
        WHERE fullName LIKE %s
        """
        rows = db.fetch_all(sql, (f"%{fullName}%",))
        result = []
        for r in rows:
            result.append({
                "userID": r[0],
                "username": r[1],
                "fullName": r[2],
                "email": r[3],
                "role": r[4],
                "is_active": r[5],
                "dateofBirth": r[6],
                "ClassID": r[7],
                "curriculumID": r[8],
                "CourseID": r[9],
            })
        return result

    @staticmethod
    def search_user_by_filler(db, DepartmentID=None, ClassID=None, status=None):
        """
        Dùng lệnh "join" giữa các bảng
        + Có thể để trống điều kiện xét
        """
        base_sql = """
        SELECT
          u.userID, u.username, u.fullName, u.email, u.Role, u.isActive,
          c.ClassID, c.ClassName,
          m.MajorID, m.MajorName,
          d.departmentID, d.DepartmentName,
          u.status
        FROM `User` u
        LEFT JOIN AcademicClass c ON u.ClassID = c.ClassID
        LEFT JOIN Major m ON c.MajorID = m.MajorID
        LEFT JOIN Department d ON m.departmentID = d.departmentID
        """
        where_clauses = []
        params = []

        if DepartmentID:
            where_clauses.append("d.departmentID = %s")
            params.append(DepartmentID)
        if ClassID:
            where_clauses.append("c.ClassID = %s")
            params.append(ClassID)
        if status:
            where_clauses.append("u.status = %s")
            params.append(status)

        if where_clauses:
            base_sql += " WHERE " + " AND ".join(where_clauses)

        rows = db.fetch_all(base_sql, tuple(params))
        out = []
        for r in rows:
            out.append({
                "userID": r[0],
                "username": r[1],
                "fullName": r[2],
                "email": r[3],
                "role": r[4],
                "is_active": r[5],
                "class": {"ClassID": r[6], "ClassName": r[7]},
                "major": {"MajorID": r[8], "MajorName": r[9]},
                "department": {"departmentID": r[10], "DepartmentName": r[11]},
                "status": r[12],
            })
        return out

    @staticmethod
    def get_all_academic_and_personal_information(db):
        """
        Dùng lệnh "join" giữa các bảng
        """
        sql = """
        SELECT
          u.userID, u.username, u.fullName, u.email, u.Role, u.isActive,
          c.ClassID, c.ClassName,
          m.MajorID, m.MajorName,
          d.departmentID, d.DepartmentName,
          sp.phone, sp.personalEmail, sp.gender, sp.Nationality, sp.hometown
        FROM `User` u
        LEFT JOIN AcademicClass c ON u.ClassID = c.ClassID
        LEFT JOIN Major m ON c.MajorID = m.MajorID
        LEFT JOIN Department d ON m.departmentID = d.departmentID
        LEFT JOIN StudentProfile sp ON u.userID = sp.userID
        """
        rows = db.fetch_all(sql)
        result = []
        for r in rows:
            result.append({
                "userID": r[0],
                "username": r[1],
                "fullName": r[2],
                "email": r[3],
                "role": r[4],
                "is_active": r[5],
                "class": {"ClassID": r[6], "ClassName": r[7]},
                "major": {"MajorID": r[8], "MajorName": r[9]},
                "department": {"departmentID": r[10], "DepartmentName": r[11]},
                "profile": {
                    "phone": r[12],
                    "personalEmail": r[13],
                    "gender": r[14],
                    "Nationality": r[15],
                    "hometown": r[16],
                },
            })
        return result
