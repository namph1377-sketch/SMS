from Database.Connect import Database


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

    def add_user(self, db):
        query = """
                INSERT INTO `User`
                (userID, username, password, email, Role, isActive, fullName, dateofBirth,
                 educationLevel, educationType, status, Admissiondate, Specialization, courseYear,
                 ClassID, curriculumID)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s,
                        %s, %s) 
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
        )
        return db.execute(query, params)

    @staticmethod
    def update_student_profile(db, user_id, data: dict):
        ALLOWED_COLUMNS = {
            "email",
            "fullName",
            "dateofBirth",
            "educationLevel",
            "educationType",
            "status",
            "Admissiondate",
            "Specialization",
            "courseYear",
            "ClassID",
            "curriculumID"
        }

        set_clauses = []
        values = []

        for column, value in data.items():
            if column in ALLOWED_COLUMNS and value is not None:
                set_clauses.append(f"{column} = %s")
                values.append(value)

        if not set_clauses:
            return False

        sql = f"""
            UPDATE `User`
            SET {', '.join(set_clauses)}
            WHERE userID = %s
        """

        values.append(user_id)
        return db.execute(sql, tuple(values))

    @staticmethod
    def delete_user(db, userID):
        query = "DELETE FROM `User` WHERE userID=%s"
        return db.execute(query, (userID,))
    
    @staticmethod
    def deactivate_account(db, user_id):
        sql = "UPDATE `User` SET isActive = 0 WHERE userID = %s"
        return db.execute(sql, (user_id,))

    # ------------- AUTH / ACCOUNT -------------
    @staticmethod
    def find_by_username(db, username):
        """
        Lấy thông tin user theo username (username là UNIQUE trong DB)
        Trả về dict hoặc None
        """
        query = """
                SELECT userID, 
                       username, 
                       password, 
                       email, 
                       Role, 
                       isActive, 
                       fullName, 
                       dateofBirth, 
                       educationLevel, 
                       educationType, 
                       status, 
                       Admissiondate, 
                       Specialization, 
                       courseYear, 
                       ClassID, 
                       curriculumID
                FROM `User`
                WHERE username = %s 
                """

        row = db.fetch_one(query, (username,))
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
        }

    @staticmethod
    def update_password(db, user_id, new_hashed_password):
        """
        Cập nhật password theo email
        new_hashed_password: mật khẩu đã được hash ở tầng service/controller
        """
        query = "UPDATE `User` SET password=%s WHERE userID=%s"
        return db.execute(query, (new_hashed_password, user_id))

    # ------------- Searches & joins -------------
    @staticmethod
    def _map_user_row(r):
        return {
            "userID": r[0],
            "fullName": r[1],
            "username": r[2],
            "email": r[3],
            "Role": r[4],
            "isActive": r[5],
            "dateofBirth": r[6],
            "educationLevel": r[7],
            "educationType": r[8],
            "status": r[9],
            "Admissiondate": r[10],
            "Specialization": r[11],
            "courseYear": r[12],
            "curriculumID": r[13],
            "class": {"ClassID": r[14], "ClassName": r[15]},
            "major": {"MajorID": r[16], "MajorName": r[17]},
            "department": {"departmentID": r[18], "DepartmentName": r[19]},
            "profile": {
                "phone": r[20],
                "emergencyPhone": r[21],
                "personalEmail": r[22],
                "ethnicity": r[23],
                "religion": r[24],
                "Nationality": r[25],
                "joinUnionDate": r[26],
                "joinPartyDate": r[27],
                "nationalID": r[28],
                "insuranceCode": r[29],
                "initialHospital": r[30],
                "placeOfBirth": r[31],
                "hometown": r[32],
                "permanentResidence": r[33],
                "gender": r[34],
                "bankAccount": r[35],
            },
        }

    @staticmethod
    def search_user_by_ID(db, userID):
        """
        JOIN: User + AcademicClass + Major + Department + StudentProfile
        Ngoài thông tin cơ bản, lấy thêm: Role, isActive
        """
        query = """
                SELECT u.userID,
                       u.fullName,
                       u.username,
                       u.email,
                       u.Role,
                       u.isActive,
                       u.dateofBirth,
                       u.educationLevel,
                       u.educationType,
                       u.status,
                       u.Admissiondate,
                       u.Specialization,
                       u.courseYear,
                       u.curriculumID,
                       u.ClassID,
                       c.ClassName,
                       m.MajorID,
                       m.MajorName,
                       d.departmentID,
                       d.DepartmentName,
                       sp.phone,
                       sp.emergencyPhone,
                       sp.personalEmail,
                       sp.ethnicity,
                       sp.religion,
                       sp.Nationality,
                       sp.joinUnionDate,
                       sp.joinPartyDate,
                       sp.nationalID,
                       sp.insuranceCode,
                       sp.initialHospital,
                       sp.placeOfBirth,
                       sp.hometown,
                       sp.permanentResidence,
                       sp.gender,
                       sp.bankAccount
                FROM `User` u
                         LEFT JOIN AcademicClass c ON u.ClassID = c.ClassID
                         LEFT JOIN Major m ON c.MajorID = m.MajorID
                         LEFT JOIN Department d ON m.departmentID = d.departmentID
                         LEFT JOIN StudentProfile sp ON u.userID = sp.userID
                WHERE u.userID = %s 
                """
        r = db.fetch_one(query, (userID,))
        if not r:
            return None

        return User._map_user_row(r)


    @staticmethod
    def search_user_by_Name(db, fullName):
        """
        JOIN: User + AcademicClass + Major + Department + StudentProfile
        Tìm theo LIKE %fullName%
        Trả về list dict
        """
        query = """
                SELECT u.userID,
                       u.fullName,
                       u.username,
                       u.email,
                       u.Role,
                       u.isActive,
                       u.dateofBirth,
                       u.educationLevel,
                       u.educationType,
                       u.status,
                       u.Admissiondate,
                       u.Specialization,
                       u.courseYear,
                       u.curriculumID,
                       u.ClassID,
                       c.ClassName,
                       m.MajorID,
                       m.MajorName,
                       d.departmentID,
                       d.DepartmentName,
                       sp.phone,
                       sp.emergencyPhone,
                       sp.personalEmail,
                       sp.ethnicity,
                       sp.religion,
                       sp.Nationality,
                       sp.joinUnionDate,
                       sp.joinPartyDate,
                       sp.nationalID,
                       sp.insuranceCode,
                       sp.initialHospital,
                       sp.placeOfBirth,
                       sp.hometown,
                       sp.permanentResidence,
                       sp.gender,
                       sp.bankAccount
                FROM `User` u
                         LEFT JOIN AcademicClass c ON u.ClassID = c.ClassID
                         LEFT JOIN Major m ON c.MajorID = m.MajorID
                         LEFT JOIN Department d ON m.departmentID = d.departmentID
                         LEFT JOIN StudentProfile sp ON u.userID = sp.userID
                WHERE u.fullName LIKE %s 
                """

        rows = db.fetch_all(query, (f"%{fullName}%",))
        return [User._map_user_row(r) for r in rows]

    @staticmethod
    def search_user_by_filter(db, DepartmentName=None, ClassName=None, status=None):
        """
        Dùng lệnh "join" giữa các bảng
        + Có thể để trống điều kiện xét
        """
        base_sql = """
                SELECT u.userID,
                       u.fullName,
                       u.username,
                       u.email,
                       u.Role,
                       u.isActive,
                       u.dateofBirth,
                       u.educationLevel,
                       u.educationType,
                       u.status,
                       u.Admissiondate,
                       u.Specialization,
                       u.courseYear,
                       u.curriculumID,
                       u.ClassID,
                       c.ClassName,
                       m.MajorID,
                       m.MajorName,
                       d.departmentID,
                       d.DepartmentName,
                       sp.phone,
                       sp.emergencyPhone,
                       sp.personalEmail,
                       sp.ethnicity,
                       sp.religion,
                       sp.Nationality,
                       sp.joinUnionDate,
                       sp.joinPartyDate,
                       sp.nationalID,
                       sp.insuranceCode,
                       sp.initialHospital,
                       sp.placeOfBirth,
                       sp.hometown,
                       sp.permanentResidence,
                       sp.gender,
                       sp.bankAccount
                FROM `User` u
                         LEFT JOIN AcademicClass c ON u.ClassID = c.ClassID
                         LEFT JOIN Major m ON c.MajorID = m.MajorID
                         LEFT JOIN Department d ON m.departmentID = d.departmentID
                         LEFT JOIN StudentProfile sp ON u.userID = sp.userID
                """
        where_clauses = []
        params = []

        if DepartmentName:
            where_clauses.append("d.DepartmentName LIKE %s")
            params.append(f"%{DepartmentName}%")
        if ClassName:
            where_clauses.append("c.ClassName LIKE %s")
            params.append(f"%{ClassName}%")
        if status:
            where_clauses.append("u.status = %s")
            params.append(status)

        if where_clauses:
            base_sql += " WHERE " + " AND ".join(where_clauses)

        rows = db.fetch_all(base_sql, tuple(params))
        return [User._map_user_row(r) for r in rows]


    @staticmethod
    def get_all_academic_and_personal_information(db):
        """
        Dùng lệnh "join" giữa các bảng
        """
        query = """
                SELECT u.userID,
                       u.fullName,
                       u.username,
                       u.email,
                       u.Role,
                       u.isActive,
                       u.dateofBirth,
                       u.educationLevel,
                       u.educationType,
                       u.status,
                       u.Admissiondate,
                       u.Specialization,
                       u.courseYear,
                       u.curriculumID,
                       u.ClassID,
                       c.ClassName,
                       m.MajorID,
                       m.MajorName,
                       d.departmentID,
                       d.DepartmentName,
                       sp.phone,
                       sp.emergencyPhone,
                       sp.personalEmail,
                       sp.ethnicity,
                       sp.religion,
                       sp.Nationality,
                       sp.joinUnionDate,
                       sp.joinPartyDate,
                       sp.nationalID,
                       sp.insuranceCode,
                       sp.initialHospital,
                       sp.placeOfBirth,
                       sp.hometown,
                       sp.permanentResidence,
                       sp.gender,
                       sp.bankAccount
                FROM `User` u
                         LEFT JOIN AcademicClass c ON u.ClassID = c.ClassID
                         LEFT JOIN Major m ON c.MajorID = m.MajorID
                         LEFT JOIN Department d ON m.departmentID = d.departmentID
                         LEFT JOIN StudentProfile sp ON u.userID = sp.userID
                """

        rows = db.fetch_all(query)
        return [User._map_user_row(r) for r in rows]

    @staticmethod
    def search_user_by_personal_email(db, email):
        query = """
            SELECT sp.userID
            FROM StudentProfile sp
            WHERE sp.personalEmail = %s
        """
        return db.fetch_one(query, (email,))

    @staticmethod
    def find_by_email(db, username):
        query = """
            SELECT u.email
            FROM User u
            WHERE u.username = %s
        """
        return db.fetch_one(query, (username,))

