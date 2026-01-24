import re
from datetime import datetime

def debug_student_input():
    # ===== Kiem tra sdt =====
    while True:
        phone = input("Enter phone number: ").strip()

        if phone.startswith("+84"):
            phone = "0" + phone[3:]

        phone = re.sub(r"\D", "", phone)

        if len(phone) != 10:
            print(" Phone number must contain exactly 10 digits!")
            continue
        break

    # ===== kiem tra cac ngay =====
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
                print(" Invalid date format!")

    # ===== nay sinh va nhap hoc(>=18 YEARS OLD) =====
    dateOfBirth = input_date("Enter date of birth: ")
    enrollmentDate = input_date("Enter enrollment date: ")

    while True:
        if dateOfBirth > enrollmentDate:
            print(" Date of birth cannot be after enrollment date!")
        else:
            age = enrollmentDate.year - dateOfBirth.year
            if (enrollmentDate.month, enrollmentDate.day) < (dateOfBirth.month, dateOfBirth.day):
                age -= 1

            if age < 18:
                print(" Student must be at least 18 years old to enroll!")
            else:
                break

        dateOfBirth = input_date("Re-enter date of birth: ")
        enrollmentDate = input_date("Re-enter enrollment date: ")

    # ===== ngay gia nhap doan va dang =====
    joinUnionDate = input_date("Enter Union join date: ")
    joinPartyDate = input_date("Enter Party join date: ")

    while joinPartyDate < joinUnionDate:
        print(" Party join date cannot be earlier than Union join date!")
        joinUnionDate = input_date("Re-enter Union join date: ")
        joinPartyDate = input_date("Re-enter Party join date: ")

    # ===== diem =====
    def input_score(msg):
        while True:
            try:
                score = float(input(msg))
                if score < 0 or score > 10:
                    print(" Score must be between 0 and 10!")
                    continue
                return score
            except ValueError:
                print(" Score must be a number!")

    caScore = input_score("Enter CA score: ")
    finalScore = input_score("Enter Final score: ")

    return {
        "phone": phone,
        "dateOfBirth": dateOfBirth.strftime("%Y-%m-%d"),
        "enrollmentDate": enrollmentDate.strftime("%Y-%m-%d"),
        "joinUnionDate": joinUnionDate.strftime("%Y-%m-%d"),
        "joinPartyDate": joinPartyDate.strftime("%Y-%m-%d"),
        "caScore": caScore,
        "finalScore": finalScore
    }

