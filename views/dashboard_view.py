import customtkinter as ctk

from database.db import get_connection


class DashboardView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=0)
        self.create_widgets()

    def create_widgets(self):
        title = ctk.CTkLabel(
            self,
            text="Tổng quan",
            font=ctk.CTkFont(size=30, weight="bold")
        )
        title.pack(anchor="w", padx=30, pady=(25, 5))

        subtitle = ctk.CTkLabel(
            self,
            text="Theo dõi nhanh tình hình sự kiện, người tham dự và đăng ký.",
            text_color="gray",
            font=ctk.CTkFont(size=15)
        )
        subtitle.pack(anchor="w", padx=30, pady=(0, 20))

        stats = self.get_dashboard_stats()

        cards_frame = ctk.CTkFrame(self, fg_color="transparent")
        cards_frame.pack(fill="x", padx=30, pady=(0, 20))

        self.create_stat_card(cards_frame, "Sự kiện", stats["events"], "Tổng số sự kiện đã tạo", 0, 0)
        self.create_stat_card(cards_frame, "Người tham dự", stats["attendees"], "Tổng số người tham dự", 0, 1)
        self.create_stat_card(cards_frame, "Đăng ký", stats["registrations"], "Tổng lượt đăng ký", 0, 2)
        self.create_stat_card(cards_frame, "Đã check-in", stats["checked_in"], "Số người đã đến", 0, 3)

        for column in range(4):
            cards_frame.grid_columnconfigure(column, weight=1)

        content = ctk.CTkFrame(self, corner_radius=15)
        content.pack(fill="both", expand=True, padx=30, pady=(0, 30))

        content_title = ctk.CTkLabel(
            content,
            text="Sự kiện sắp diễn ra",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        content_title.pack(anchor="w", padx=20, pady=(18, 8))

        upcoming_events = self.get_upcoming_events()
        if not upcoming_events:
            empty_label = ctk.CTkLabel(content, text="Chưa có sự kiện nào trong hệ thống.", text_color="gray")
            empty_label.pack(anchor="w", padx=20, pady=10)
            return

        for event in upcoming_events:
            event_row = ctk.CTkFrame(content, corner_radius=10)
            event_row.pack(fill="x", padx=20, pady=6)

            event_name = ctk.CTkLabel(
                event_row,
                text=event["name"],
                font=ctk.CTkFont(size=16, weight="bold")
            )
            event_name.pack(anchor="w", padx=15, pady=(10, 2))

            details = f"Ngày: {event['date']} | Giờ: {event['time']} | Địa điểm: {event['location']} | Sức chứa: {event['capacity']}"
            event_details = ctk.CTkLabel(event_row, text=details, text_color="gray")
            event_details.pack(anchor="w", padx=15, pady=(0, 10))

    def create_stat_card(self, parent, title, value, subtitle, row, column):
        card = ctk.CTkFrame(parent, corner_radius=12)
        card.grid(row=row, column=column, sticky="ew", padx=6)

        value_label = ctk.CTkLabel(
            card,
            text=str(value),
            font=ctk.CTkFont(size=30, weight="bold")
        )
        value_label.pack(anchor="w", padx=18, pady=(14, 0))

        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(size=15, weight="bold")
        )
        title_label.pack(anchor="w", padx=18, pady=(2, 0))

        subtitle_label = ctk.CTkLabel(card, text=subtitle, text_color="gray")
        subtitle_label.pack(anchor="w", padx=18, pady=(0, 14))

    def get_dashboard_stats(self):
        conn = get_connection()
        cursor = conn.cursor()

        stats = {
            "events": cursor.execute("SELECT COUNT(*) AS total FROM events").fetchone()["total"],
            "attendees": cursor.execute("SELECT COUNT(*) AS total FROM attendees").fetchone()["total"],
            "registrations": cursor.execute("SELECT COUNT(*) AS total FROM registrations").fetchone()["total"],
            "checked_in": cursor.execute("SELECT COUNT(*) AS total FROM registrations WHERE check_in = 1").fetchone()["total"]
        }

        conn.close()
        return stats

    def get_upcoming_events(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM events
            ORDER BY date ASC, time ASC
            LIMIT 5
        """)

        events = cursor.fetchall()
        conn.close()
        return events
