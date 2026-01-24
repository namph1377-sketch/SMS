import re

def validate_phone(phone: str):
    if not phone:
        return None, "Phone number is required"

    phone = phone.strip()

    if phone.startswith("+84"):
        phone = "0" + phone[3:]

    phone = re.sub(r"\D", "", phone)

    if len(phone) != 10:
        return None, "Phone number must contain exactly 10 digits"

    return phone, None
    ######## Kiêm tra ngay#####
from datetime import datetime
import re
def debug_date(date_str):
    if date_str is None or date_str.strip() == "":
        return None, "Date is required"

    d = date_str.strip().replace("/", "-").replace(".", "-")

    try:
        if re.match(r"\d{2}-\d{2}-\d{4}", d):
            return datetime.strptime(d, "%d-%m-%Y"), None
        elif re.match(r"\d{4}-\d{2}-\d{2}", d):
            return datetime.strptime(d, "%Y-%m-%d"), None
        else:
            return None, "Invalid date format"
    except ValueError:
        return None, "Invalid date value"
#########kiem tra ngay sinh ngay nhap hc ####
def debug_age(dateOfBirth, enrollmentDate):
    if dateOfBirth > enrollmentDate:
        return False, "Date of birth cannot be after enrollment date"

    age = enrollmentDate.year - dateOfBirth.year
    if (enrollmentDate.month, enrollmentDate.day) < (dateOfBirth.month, dateOfBirth.day):
        age -= 1

    if age < 18:
        return False, "Student must be at least 18 years old"

    return True, None
###### kiem tra ngay nhap doan, dang
def debug_join_dates(joinUnionDate, joinPartyDate):
    if joinPartyDate < joinUnionDate:
        return False, "Party join date cannot be earlier than Union join date"
    return True, None
####### kiem tra dim Ca score va final score chung
def debug_score(score):
    if score is None or str(score).strip() == "":
        return None, "Score is required"
    try:
        score = float(score)
    except ValueError:
        return None, "Score must be a number"

    if score < 0 or score > 10:
        return None, "Score must be between 0 and 10"

    return score, None
