import customtkinter as ctk

from database.db import initialize_database
from views.events_view import EventsView
from views.attendees_view import AttendeesView
from views.registrations_view import RegistrationsView
from views.dashboard_view import DashboardView
from views.statistics_view import StatisticsView


class EventManagementApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Hệ thống quản lý sự kiện và người tham dự")
        self.geometry("1100x650")
        self.resizable(False, False)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.create_layout()

    def create_layout(self):
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.main_area = ctk.CTkFrame(self, corner_radius=0)
        self.main_area.pack(side="right", fill="both", expand=True)

        title = ctk.CTkLabel(
            self.sidebar,
            text="HỆ THỐNG SỰ KIỆN",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        title.pack(pady=(30, 20))

        menu_items = {
            "Dashboard": "Tổng quan",
            "Events": "Sự kiện",
            "Attendees": "Người tham dự",
            "Registrations": "Đăng ký",
            "Statistics": "Thống kê"
        }

        for page_key, page_label in menu_items.items():
            button = ctk.CTkButton(
                self.sidebar,
                text=page_label,
                height=42,
                corner_radius=10,
                command=lambda page=page_key: self.show_page(page)
            )
            button.pack(fill="x", padx=20, pady=8)

        self.show_page("Dashboard")

    def clear_main_area(self):
        for widget in self.main_area.winfo_children():
            widget.destroy()

    def show_page(self, page_name):
        self.clear_main_area()

        if page_name == "Dashboard":
            page = DashboardView(self.main_area)
            page.pack(fill="both", expand=True)
            return
        if page_name == "Events":
            page = EventsView(self.main_area)
            page.pack(fill="both", expand=True)
            return
        if page_name == "Attendees":
            page = AttendeesView(self.main_area)
            page.pack(fill="both", expand=True)
            return
        if page_name == "Registrations":
            page = RegistrationsView(self.main_area)
            page.pack(fill="both", expand=True)
            return
        if page_name == "Statistics":
            page = StatisticsView(self.main_area)
            page.pack(fill="both", expand=True)
            return
        page_titles = {
            "Dashboard": "Tổng quan",
            "Registrations": "Đăng ký tham dự",
            "Statistics": "Thống kê"
        }

        heading = ctk.CTkLabel(
            self.main_area,
            text=page_titles.get(page_name, page_name),
            font=ctk.CTkFont(size=30, weight="bold")
        )
        heading.pack(anchor="w", padx=30, pady=(30, 10))

        subtitle = ctk.CTkLabel(
            self.main_area,
            text="Trang này sẽ được hoàn thiện ở các bước tiếp theo.",
            font=ctk.CTkFont(size=16),
            text_color="gray"
        )
        subtitle.pack(anchor="w", padx=30, pady=(0, 20))

        card = ctk.CTkFrame(self.main_area, corner_radius=15)
        card.pack(fill="both", expand=True, padx=30, pady=20)

        message = ctk.CTkLabel(
            card,
            text="Chức năng này đang được xây dựng.",
            font=ctk.CTkFont(size=18)
        )
        message.pack(expand=True)


if __name__ == "__main__":
    initialize_database()
    app = EventManagementApp()
    app.mainloop()





