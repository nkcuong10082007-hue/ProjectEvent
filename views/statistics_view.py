from tkinter import ttk
import customtkinter as ctk

from database.db import get_connection


class StatisticsView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=0)
        self.create_widgets()

    def create_widgets(self):
        title = ctk.CTkLabel(
            self,
            text="Thống kê",
            font=ctk.CTkFont(size=30, weight="bold")
        )
        title.pack(anchor="w", padx=30, pady=(25, 5))

        subtitle = ctk.CTkLabel(
            self,
            text="Xem số lượng đăng ký và check-in theo từng sự kiện.",
            text_color="gray",
            font=ctk.CTkFont(size=15)
        )
        subtitle.pack(anchor="w", padx=30, pady=(0, 20))

        content = ctk.CTkFrame(self, corner_radius=15)
        content.pack(fill="both", expand=True, padx=30, pady=(0, 30))

        chart_frame = ctk.CTkFrame(content, corner_radius=12)
        chart_frame.pack(fill="both", expand=True, padx=20, pady=(20, 10))

        table_frame = ctk.CTkFrame(content, corner_radius=12)
        table_frame.pack(fill="x", padx=20, pady=(0, 20))

        data = self.get_event_statistics()
        self.create_chart(chart_frame, data)
        self.create_table(table_frame, data)

    def create_chart(self, parent, data):
        if not data:
            empty_label = ctk.CTkLabel(parent, text="Chưa có dữ liệu để thống kê.", text_color="gray")
            empty_label.pack(expand=True)
            return

        try:
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
            from matplotlib.figure import Figure
        except ImportError:
            error_label = ctk.CTkLabel(parent, text="Chưa cài matplotlib nên không thể hiển thị biểu đồ.")
            error_label.pack(expand=True)
            return

        event_names = [row["event_name"] for row in data]
        registration_counts = [row["total_registrations"] for row in data]
        check_in_counts = [row["total_check_in"] for row in data]

        figure = Figure(figsize=(8, 3.2), dpi=100)
        axis = figure.add_subplot(111)

        positions = range(len(event_names))
        axis.bar(positions, registration_counts, label="Đăng ký", color="#3b82f6")
        axis.bar(positions, check_in_counts, label="Check-in", color="#22c55e")

        axis.set_title("Số lượng đăng ký theo sự kiện")
        axis.set_ylabel("Số lượng")
        axis.set_xticks(list(positions))
        axis.set_xticklabels(event_names, rotation=20, ha="right")
        axis.legend()
        figure.tight_layout()

        canvas = FigureCanvasTkAgg(figure, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=15, pady=15)

    def create_table(self, parent, data):
        columns = ("event", "registrations", "checked_in", "capacity")
        tree = ttk.Treeview(parent, columns=columns, show="headings", height=6)

        tree.heading("event", text="Sự kiện")
        tree.heading("registrations", text="Số đăng ký")
        tree.heading("checked_in", text="Đã check-in")
        tree.heading("capacity", text="Sức chứa")

        tree.column("event", width=320)
        tree.column("registrations", width=120, anchor="center")
        tree.column("checked_in", width=120, anchor="center")
        tree.column("capacity", width=120, anchor="center")

        tree.pack(fill="x", padx=15, pady=15)

        for row in data:
            tree.insert(
                "",
                "end",
                values=(
                    row["event_name"],
                    row["total_registrations"],
                    row["total_check_in"],
                    row["capacity"]
                )
            )

    def get_event_statistics(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                events.name AS event_name,
                events.capacity,
                COUNT(registrations.id) AS total_registrations,
                SUM(CASE WHEN registrations.check_in = 1 THEN 1 ELSE 0 END) AS total_check_in
            FROM events
            LEFT JOIN registrations ON events.id = registrations.event_id
            GROUP BY events.id
            ORDER BY total_registrations DESC, events.date ASC
        """)

        rows = cursor.fetchall()
        conn.close()
        return rows
