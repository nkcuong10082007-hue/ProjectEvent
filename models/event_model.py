from database.db import get_connection


def get_all_events():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM events
        ORDER BY date ASC, time ASC
    """)

    events = cursor.fetchall()
    conn.close()
    return events


def search_events(keyword):
    conn = get_connection()
    cursor = conn.cursor()

    search_value = f"%{keyword}%"

    cursor.execute("""
        SELECT * FROM events
        WHERE name LIKE ?
           OR date LIKE ?
           OR time LIKE ?
           OR location LIKE ?
           OR description LIKE ?
        ORDER BY date ASC, time ASC
    """, (search_value, search_value, search_value, search_value, search_value))

    events = cursor.fetchall()
    conn.close()
    return events


def add_event(name, date, time, location, capacity, description):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO events (name, date, time, location, capacity, description)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (name, date, time, location, capacity, description))

    conn.commit()
    conn.close()


def update_event(event_id, name, date, time, location, capacity, description):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE events
        SET name = ?, date = ?, time = ?, location = ?, capacity = ?, description = ?
        WHERE id = ?
    """, (name, date, time, location, capacity, description, event_id))

    conn.commit()
    conn.close()


def delete_event(event_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM events WHERE id = ?", (event_id,))

    conn.commit()
    conn.close()