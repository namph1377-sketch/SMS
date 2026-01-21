class Contain:
    def __init__(self, curriculumID, subjectID):
        self.curriculumID = curriculumID
        self.subjectID = subjectID

    @staticmethod
    def get_all_curriculum_information(db):
        query = """
        SELECT
          c.curriculumID,
          cur.semester,
          s.subjectID,
          s.subjectName,
          s.Credits
        FROM Contain c
        JOIN Curriculum cur ON c.curriculumID = cur.curriculumID
        JOIN Subject s ON c.subjectID = s.subjectID
        """
        rows = db.fetch_all(query)

        result = []
        for r in rows:
            result.append({
                "curriculum": {
                    "curriculumID": r[0],
                    "semester": r[1],
                },
                "subject": {
                    "subjectID": r[2],
                    "subjectName": r[3],
                    "Credits": r[4],
                }
            })
        return result
