class Log:
    def __init__(self, LogID, LogType, LogObject, ChangeAt, userID, OldValue=None):
        self.LogID = LogID
        self.LogType = LogType
        self.LogObject = LogObject
        self.OldValue = OldValue
        self.ChangeAt = ChangeAt
        self.userID = userID

    def add_log(self, db):
        query = "INSERT INTO `Log` (LogID, LogType, LogObject, OldValue, ChangeAt, userID) VALUES (%s,%s,%s,%s,%s,%s)"
        return db.execute_query(query, (self.LogID, self.LogType, self.LogObject, self.OldValue, self.ChangeAt, self.userID))
        
