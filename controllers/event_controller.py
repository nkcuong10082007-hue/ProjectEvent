from datetime import datetime
from models import event_model


def get_events():
    return event_model.get_all_events()


def search_events(keyword):
    if keyword.strip() == "":
        return event_model.get_all_events()

    return event_model.search_events(keyword.strip())


def create_event(name, date, time, location, capacity, description):
    validate_event_data(name, date, time, location, capacity)
    event_model.add_event(
        name.strip(),
        date.strip(),
        time.strip(),
        location.strip(),
        int(capacity),
        description.strip()
    )


def edit_event(event_id, name, date, time, location, capacity, description):
    validate_event_data(name, date, time, location, capacity)
    event_model.update_event(
        event_id,
        name.strip(),
        date.strip(),
        time.strip(),
        location.strip(),
        int(capacity),
        description.strip()
    )


def remove_event(event_id):
    event_model.delete_event(event_id)


def validate_event_data(name, date, time, location, capacity):
    if name.strip() == "":
        raise ValueError("Tên sự kiện không được để trống.")

    if date.strip() == "":
        raise ValueError("Ngày diễn ra sự kiện không được để trống.")

    try:
        datetime.strptime(date.strip(), "%Y-%m-%d")
    except ValueError:
        raise ValueError("Ngày phải đúng định dạng YYYY-MM-DD. Ví dụ: 2026-06-17.")

    if time.strip() == "":
        raise ValueError("Giờ diễn ra sự kiện không được để trống.")

    try:
        datetime.strptime(time.strip(), "%H:%M")
    except ValueError:
        raise ValueError("Giờ phải đúng định dạng HH:MM. Ví dụ: 08:30 hoặc 19:00.")

    if location.strip() == "":
        raise ValueError("Địa điểm tổ chức không được để trống.")

    if capacity.strip() == "":
        raise ValueError("Sức chứa không được để trống.")

    if not capacity.isdigit():
        raise ValueError("Sức chứa phải là số nguyên dương.")

    if int(capacity) <= 0:
        raise ValueError("Sức chứa phải lớn hơn 0.")
