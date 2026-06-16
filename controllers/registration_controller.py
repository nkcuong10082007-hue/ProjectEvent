import sqlite3
from models import registration_model


def get_registrations():
    return registration_model.get_all_registrations()


def search_registrations(keyword):
    if keyword.strip() == "":
        return registration_model.get_all_registrations()

    return registration_model.search_registrations(keyword)


def create_registration(event_id, attendee_id):
    if event_id is None:
        raise ValueError("Vui lòng chọn sự kiện.")

    if attendee_id is None:
        raise ValueError("Vui lòng chọn người tham dự.")

    capacity = registration_model.get_event_capacity(event_id)
    if capacity is None:
        raise ValueError("Sự kiện không tồn tại.")

    current_total = registration_model.count_registrations_by_event(event_id)
    if current_total >= capacity:
        raise ValueError("Sự kiện này đã đủ số lượng người tham dự.")

    try:
        registration_model.add_registration(event_id, attendee_id)
    except sqlite3.IntegrityError:
        raise ValueError("Người này đã đăng ký sự kiện này rồi.")


def cancel_registration(registration_id):
    if registration_id is None:
        raise ValueError("Vui lòng chọn đăng ký cần hủy.")

    registration_model.update_registration_status(registration_id, "Cancelled")


def confirm_registration(registration_id):
    if registration_id is None:
        raise ValueError("Vui lòng chọn đăng ký cần xác nhận.")

    registration_model.update_registration_status(registration_id, "Registered")


def check_in_registration(registration_id):
    if registration_id is None:
        raise ValueError("Vui lòng chọn đăng ký cần check-in.")

    registration_model.update_check_in(registration_id, 1)


def undo_check_in_registration(registration_id):
    if registration_id is None:
        raise ValueError("Vui lòng chọn đăng ký cần bỏ check-in.")

    registration_model.update_check_in(registration_id, 0)


def remove_registration(registration_id):
    if registration_id is None:
        raise ValueError("Vui lòng chọn đăng ký cần xóa.")

    registration_model.delete_registration(registration_id)
