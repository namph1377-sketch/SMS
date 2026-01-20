class User:
    # Ở hàm __init__: Nhập vào các thuộc tính của bảng User trong data model
    def __init__(self, userID, ):
        pass

    def add_user(self, db):
        pass
    def update_user(self, db):
        pass

    @staticmethod
    def delete_user(db, userID):
        pass
    @staticmethod
    def search_user_by_ID(db, userID):
        """
        Ngoài những thông tin cơ bản cần Select,
        Hãy lấy thêm những thông tin sau: role, is_active
        """
        pass
    @staticmethod
    def search_user_by_Name(db, fullName):
        pass
    @staticmethod
    def search_user_by_filler(db, DepartmentID, ClassID, status):
        """
        Dùng lệnh "join" giữa các bảng
        + Có thể để trống điều kiện xét
        """
        pass

    @staticmethod
    def get_all_academic_and_personal_information(db):
        """
        Dùng lệnh "join" giữa các bảng
        """
        pass