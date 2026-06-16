from database.db import get_connection


def get_all_attendees():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM attendees
        ORDER BY full_name ASC
    """)

    attendees = cursor.fetchall()
    conn.close()
    return attendees


def search_attendees(keyword):
    conn = get_connection()
    cursor = conn.cursor()

    search_value = f"%{keyword}%"

    cursor.execute("""
        SELECT * FROM attendees
        WHERE full_name LIKE ?
           OR email LIKE ?
           OR phone LIKE ?
        ORDER BY full_name ASC
    """, (search_value, search_value, search_value))

    attendees = cursor.fetchall()
    conn.close()
    return attendees


def add_attendee(full_name, email, phone):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO attendees (full_name, email, phone)
        VALUES (?, ?, ?)
    """, (full_name, email, phone))

    conn.commit()
    conn.close()


def update_attendee(attendee_id, full_name, email, phone):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE attendees
        SET full_name = ?, email = ?, phone = ?
        WHERE id = ?
    """, (full_name, email, phone, attendee_id))

    conn.commit()
    conn.close()


def delete_attendee(attendee_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM attendees WHERE id = ?", (attendee_id,))

    conn.commit()
    conn.close()