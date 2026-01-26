from datetime import datetime
import re

def debug_phone(phone: str):
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
###### kiem tra ngay nhap doan, dang
def debug_citizen_id(citizen_id: str):
    """
    Citizen identification number:
    - Chỉ cho phép đúng 12 chữ số
    """
    if not citizen_id:
        print("ERROR: Citizen identification number cannot be empty")
        return None

    citizen_id = citizen_id.strip()

    if not citizen_id.isdigit():
        print("ERROR: Citizen identification number must contain only digits")
        return None

    if len(citizen_id) != 12:
        print("ERROR: Citizen identification number must contain exactly 12 digits")
        return None

    return citizen_id
from datetime import datetime

from datetime import datetime

def validate_entry_date(team_date: str, union_date: str):
    """
    Kiểm tra thứ tự ngày:
    - Ngày vào Đội < Ngày vào Đoàn
    """
    # cho phép bỏ trống
    if not team_date or not union_date:
        return True, None, None

    team_dt, team_err = debug_date(team_date)
    if team_err:
        print("ERROR: Team date -", team_err)
        return False, None, None

    union_dt, union_err = debug_date(union_date)
    if union_err:
        print("ERROR: Union date -", union_err)
        return False, None, None

    if union_dt < team_dt:
        print("ERROR: Youth Union entry date must be later than Team entry date")
        return False, None, None

    return True, team_dt, union_dt


