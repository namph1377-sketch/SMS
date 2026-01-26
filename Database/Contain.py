class Contain:
    def __init__(self, curriculumID, subjectID, semester):
        self.curriculumID = curriculumID
        self.subjectID = subjectID
        self.semester = semester

    @staticmethod
    def get_all_curriculum_information(db):
        query = """
        SELECT
            c.curriculumID,
            c.semester,
            s.subjectID,
            s.subjectName,
            s.Credits
        FROM Contain c
        JOIN Subject s ON c.subjectID = s.subjectID
        ORDER BY c.curriculumID, c.semester
        """
        rows = db.fetch_all(query)

        result = []
        for r in rows:
            result.append({
                "curriculumID": r[0],
                "semester": r[1],
                "subject": {
                    "subjectID": r[2],
                    "subjectName": r[3],
                    "Credits": r[4]
                }
            })
        return result
