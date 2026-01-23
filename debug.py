import re
from datetime import datetime

def debug_student_input():
    # ===== SỐ ĐIỆN THOẠI =====
    while True:
        phone = input("Nhập số điện thoại: ").strip()

        if phone.startswith("+84"):
            phone = "0" + phone[3:]

        phone = re.sub(r"\D", "", phone)

        if len(phone) != 10:
            print(" SĐT phải đúng 10 chữ số!")
            continue
        break

    # ===== HÀM NHẬP NGÀY (NGÀY-THÁNG-NĂM) =====
    def input_date(msg):
        while True:
            d = input(msg).strip().replace("/", "-").replace(".", "-")
            try:
                if re.match(r"\d{2}-\d{2}-\d{4}", d):
                    return datetime.strptime(d, "%d-%m-%Y")
                elif re.match(r"\d{4}-\d{2}-\d{2}", d):
                    return datetime.strptime(d, "%Y-%m-%d")
                else:
                    raise ValueError
            except ValueError:
                print(" Ngày không đúng định dạng (DD-MM-YYYY hoặc YYYY-MM-DD)!")

    # ===== NGÀY SINH & NGÀY NHẬP HỌC (>=18 TUỔI) =====
    ngay_sinh = input_date("Nhập ngày sinh: ")
    ngay_nhap_hoc = input_date("Nhập ngày nhập học: ")

    while True:
        if ngay_sinh > ngay_nhap_hoc:
            print(" Ngày sinh không được sau ngày nhập học!")
        else:
            age = ngay_nhap_hoc.year - ngay_sinh.year
            if (ngay_nhap_hoc.month, ngay_nhap_hoc.day) < (ngay_sinh.month, ngay_sinh.day):
                age -= 1

            if age < 18:
                print(" Sinh viên phải đủ 18 tuổi mới được nhập học!")
            else:
                break

        ngay_sinh = input_date("Nhập lại ngày sinh: ")
        ngay_nhap_hoc = input_date("Nhập lại ngày nhập học: ")

    # ===== NGÀY VÀO ĐỘI / ĐOÀN =====
    ngay_vao_doi = input_date("Nhập ngày vào Đội: ")
    ngay_vao_doan = input_date("Nhập ngày vào Đoàn: ")

    while ngay_vao_doan < ngay_vao_doi:
        print(" Ngày vào Đoàn không được trước ngày vào Đội!")
        ngay_vao_doi = input_date("Nhập lại ngày vào Đội: ")
        ngay_vao_doan = input_date("Nhập lại ngày vào Đoàn: ")

    # ===== ĐIỂM CA & FINAL =====
    def input_score(msg):
        while True:
            try:
                score = float(input(msg))
                if score < 0 or score > 10:
                    print(" Điểm phải nằm trong khoảng 0 – 10!")
                    continue
                return score
            except ValueError:
                print(" Điểm phải là số!")

    ca_score = input_score("Nhập điểm CA: ")
    final_score = input_score("Nhập điểm Final: ")

    return {
        "phone": phone,
        "ngay_sinh": ngay_sinh.strftime("%Y-%m-%d"),
        "ngay_nhap_hoc": ngay_nhap_hoc.strftime("%Y-%m-%d"),
        "ngay_vao_doi": ngay_vao_doi.strftime("%Y-%m-%d"),
        "ngay_vao_doan": ngay_vao_doan.strftime("%Y-%m-%d"),
        "ca_score": ca_score,
        "final_score": final_score
    }
