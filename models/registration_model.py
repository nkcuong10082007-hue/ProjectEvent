import sqlite3
from database.db import get_connection


def get_all_registrations():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            registrations.id,
            registrations.event_id,
            registrations.attendee_id,
            registrations.status,
            registrations.check_in,
            registrations.registered_at,
            events.name AS event_name,
            events.date AS event_date,
            events.time AS event_time,
            attendees.full_name AS attendee_name,
            attendees.email AS attendee_email,
            attendees.phone AS attendee_phone
        FROM registrations
        JOIN events ON registrations.event_id = events.id
        JOIN attendees ON registrations.attendee_id = attendees.id
        ORDER BY registrations.registered_at DESC
    """)

    registrations = cursor.fetchall()
    conn.close()
    return registrations


def search_registrations(keyword):
    conn = get_connection()
    cursor = conn.cursor()
    search_value = f"%{keyword}%"

    cursor.execute("""
        SELECT
            registrations.id,
            registrations.event_id,
            registrations.attendee_id,
            registrations.status,
            registrations.check_in,
            registrations.registered_at,
            events.name AS event_name,
            events.date AS event_date,
            events.time AS event_time,
            attendees.full_name AS attendee_name,
            attendees.email AS attendee_email,
            attendees.phone AS attendee_phone
        FROM registrations
        JOIN events ON registrations.event_id = events.id
        JOIN attendees ON registrations.attendee_id = attendees.id
        WHERE events.name LIKE ?
           OR attendees.full_name LIKE ?
           OR attendees.email LIKE ?
           OR attendees.phone LIKE ?
           OR registrations.status LIKE ?
        ORDER BY registrations.registered_at DESC
    """, (search_value, search_value, search_value, search_value, search_value))

    registrations = cursor.fetchall()
    conn.close()
    return registrations


def count_registrations_by_event(event_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM registrations
        WHERE event_id = ? AND status != 'Cancelled'
    """, (event_id,))

    total = cursor.fetchone()["total"]
    conn.close()
    return total


def get_event_capacity(event_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT capacity FROM events WHERE id = ?", (event_id,))
    event = cursor.fetchone()
    conn.close()

    if event is None:
        return None
    return event["capacity"]


def add_registration(event_id, attendee_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO registrations (event_id, attendee_id, status, check_in)
        VALUES (?, ?, 'Registered', 0)
    """, (event_id, attendee_id))

    conn.commit()
    conn.close()


def update_registration_status(registration_id, status):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE registrations
        SET status = ?
        WHERE id = ?
    """, (status, registration_id))

    conn.commit()
    conn.close()


def update_check_in(registration_id, check_in):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE registrations
        SET check_in = ?
        WHERE id = ?
    """, (check_in, registration_id))

    conn.commit()
    conn.close()


def delete_registration(registration_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM registrations WHERE id = ?", (registration_id,))

    conn.commit()
    conn.close()
