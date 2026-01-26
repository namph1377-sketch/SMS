class AcademicClass:
    def __init__(self, ClassID, ClassName, MajorID):
        self.ClassID = ClassID
        self.ClassName = ClassName
        self.MajorID = MajorID

    @staticmethod
    def validate_structure(db, class_id, major_name, department_name, curriculum_id=None):
        sql = """
            SELECT 1
            FROM AcademicClass c
            JOIN Major m ON c.MajorID = m.MajorID
            JOIN Department d ON m.departmentID = d.departmentID
            WHERE c.ClassID = %s
              AND m.MajorName = %s
              AND d.DepartmentName = %s
        """
        params = [class_id, major_name, department_name]

        # 👇 chỉ check curriculum nếu có truyền vào
        if curriculum_id is not None:
            sql += " AND m.curriculumID = %s"
            params.append(curriculum_id)

        return db.fetch_one(sql, tuple(params)) is not None



