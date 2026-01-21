class StudentProfile:
    def __init__(
        self,
        userID,
        phone,
        personalEmail,
        Nationality,
        placeOfBirth,
        hometown,
        permanentResidence,
        gender,
        emergencyPhone=None,
        ethnicity=None,
        religion=None,
        joinUnionDate=None,
        joinPartyDate=None,
        nationalId=None,
        insuranceCode=None,
        initialHospital=None,
        bankAccount=None,
    ):
        # NOT NULL theo schema
        self.userID = userID
        self.phone = phone
        self.personalEmail = personalEmail
        self.Nationality = Nationality
        self.placeOfBirth = placeOfBirth
        self.hometown = hometown
        self.permanentResidence = permanentResidence
        self.gender = gender

        # Nullable theo schema
        self.emergencyPhone = emergencyPhone
        self.ethnicity = ethnicity
        self.religion = religion
        self.joinUnionDate = joinUnionDate
        self.joinPartyDate = joinPartyDate
        self.nationalId = nationalId
        self.insuranceCode = insuranceCode
        self.initialHospital = initialHospital
        self.bankAccount = bankAccount

    def add_student_profile(self, db):
        query = """
        INSERT INTO StudentProfile
        (userID, phone, emergencyPhone, personalEmail, ethnicity, religion, Nationality,
         joinUnionDate, joinPartyDate, nationalId, insuranceCode, initialHospital,
         placeOfBirth, hometown, permanentResidence, gender, bankAccount)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        params = (
            self.userID,
            self.phone,
            self.emergencyPhone,
            self.personalEmail,
            self.ethnicity,
            self.religion,
            self.Nationality,
            self.joinUnionDate,
            self.joinPartyDate,
            self.nationalId,
            self.insuranceCode,
            self.initialHospital,
            self.placeOfBirth,
            self.hometown,
            self.permanentResidence,
            self.gender,
            self.bankAccount,
        )
        return db.execute_query(query, params)

    def update_student_profile(self, db):
        query = """
        UPDATE StudentProfile SET
          phone=%s,
          emergencyPhone=%s,
          personalEmail=%s,
          ethnicity=%s,
          religion=%s,
          Nationality=%s,
          joinUnionDate=%s,
          joinPartyDate=%s,
          nationalId=%s,
          insuranceCode=%s,
          initialHospital=%s,
          placeOfBirth=%s,
          hometown=%s,
          permanentResidence=%s,
          gender=%s,
          bankAccount=%s
        WHERE userID=%s
        """
        params = (
            self.phone,
            self.emergencyPhone,
            self.personalEmail,
            self.ethnicity,
            self.religion,
            self.Nationality,
            self.joinUnionDate,
            self.joinPartyDate,
            self.nationalId,
            self.insuranceCode,
            self.initialHospital,
            self.placeOfBirth,
            self.hometown,
            self.permanentResidence,
            self.gender,
            self.bankAccount,
            self.userID,
        )
        return db.execute_query(query, params)

    @staticmethod
    def delete_student_profile(db, userID):
        query = "DELETE FROM StudentProfile WHERE userID=%s"
        return db.execute_query(query, (userID,))
