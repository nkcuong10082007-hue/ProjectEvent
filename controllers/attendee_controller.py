import re
import sqlite3
from models import attendee_model

EMAIL_PATTERN = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"


def get_attendees():
    return attendee_model.get_all_attendees()


def search_attendees(keyword):
    if keyword.strip() == "":
        return attendee_model.get_all_attendees()

    return attendee_model.search_attendees(keyword.strip())


def create_attendee(full_name, email, phone):
    validate_attendee_data(full_name, email, phone)

    try:
        attendee_model.add_attendee(full_name.strip(), email.strip().lower(), phone.strip())
    except sqlite3.IntegrityError:
        raise ValueError("Email này đã tồn tại.")


def edit_attendee(attendee_id, full_name, email, phone):
    validate_attendee_data(full_name, email, phone)

    try:
        attendee_model.update_attendee(attendee_id, full_name.strip(), email.strip().lower(), phone.strip())
    except sqlite3.IntegrityError:
        raise ValueError("Email này đã tồn tại.")


def remove_attendee(attendee_id):
    attendee_model.delete_attendee(attendee_id)


def validate_attendee_data(full_name, email, phone):
    if full_name.strip() == "":
        raise ValueError("Họ và tên không được để trống.")

    if len(full_name.strip()) < 2:
        raise ValueError("Họ và tên phải có ít nhất 2 ký tự.")

    if email.strip() == "":
        raise ValueError("Email không được để trống.")

    if re.match(EMAIL_PATTERN, email.strip()) is None:
        raise ValueError("Email không hợp lệ. Ví dụ: nguyenvana@gmail.com.")

    if phone.strip() == "":
        raise ValueError("Số điện thoại không được để trống.")

    if not phone.strip().isdigit():
        raise ValueError("Số điện thoại chỉ được chứa chữ số.")

    if len(phone.strip()) < 9 or len(phone.strip()) > 11:
        raise ValueError("Số điện thoại phải có từ 9 đến 11 chữ số.")
