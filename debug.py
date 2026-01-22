import hashlib

class StudentManagementSystem:
    def hash_pw(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    # TC01, TC02: Login
    def login(self, username, password):
        user = self.users.get(username)
        if user and user["password"] == self.hash_pw(password):
            return f"Login successful! Hiển thị MENU {user['role']}."
        return "Incorrect login information, please try again!"

    # TC03, TC04: Forgot Password
    def forgot_password(self, username, email, otp, new_pw, confirm_pw):
        user = self.users.get(username)
        if not user or user.get("email") != email:
            return "Incorrect account or email!"
        if otp != "123456": # Giả lập OTP đúng là 123456
            return "Incorrect OTP code! / OTP code has expired!"
        if new_pw != confirm_pw:
            return "Mật khẩu không trùng khớp"
        user["password"] = self.hash_pw(new_pw)
        return "Password reset successful! Quay về trang đăng nhập"

    # TC05, TC07, TC08, TC09: View Info (SV)
    def view_student_info(self, sid, info_type):
        s = self.users.get(sid)
        if info_type == "profile": return s # Read-only
        if info_type == "academic": return {"class": s["class"], "dept": s["dept"]}
        if info_type == "curriculum": return self.curriculums.get(s["dept"])
        if info_type == "grades": return s["grades"]

    # TC10, TC11: Change Password
    def change_password(self, sid, old_pw, new_pw, confirm_pw):
        user = self.users.get(sid)
        if user["password"] != self.hash_pw(old_pw):
            return "Mật khẩu cũ không đúng"
        if new_pw != confirm_pw:
            return "Mật khẩu xác nhận mới không trùng khớp với mật khẩu mới, vui lòng nhập lại."
        user["password"] = self.hash_pw(new_pw)
        return "SUCCESSFUL!"

    # TC12, TC13, TC14: Lecturer (GV)
    def gv_update_grade(self, gv_id, course_id, student_id, new_ca, new_final):
        if student_id in self.users:
            self.users[student_id]["grades"][course_id] = {"CA": new_ca, "Final": new_final}
            return "UPDATE SUCCESSFUL! Điểm được cập nhật."
        return "Failed"

    # TC15, TC16, TC17, TC18, TC19: Admin
    def admin_action(self, action, data):
        if action == "create":
            sid = data["citizen_id"]
            if sid in self.users: return "Duplicated ID"
            self.users[sid] = {**data, "password": self.hash_pw(sid), "role": "SV"}
            return "SUCCESSFUL SAVE!"
        if action == "search":
            kw = data.lower()
            return [u for k, u in self.users.items() if kw in k or kw in u.get("name", "").lower()]
        if action == "filter":
            return [u for u in self.users.values() if u.get("dept") == data["dept"] and u.get("status") == data["status"]]
        if action == "delete":
            if data in self.users:
                self.users[data]["status"] = "Deactivated" # Soft delete
                return "SUCCESSFUL DELETE!"
        return "Error"

    # TC20: Logout
    def logout(self):
        return "Redirecting to login..."

