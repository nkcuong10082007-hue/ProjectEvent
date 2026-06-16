import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk

from controllers import registration_controller, event_controller, attendee_controller


class RegistrationsView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=0)
        self.selected_registration_id = None
        self.event_options = {}
        self.attendee_options = {}

        self.create_widgets()
        self.load_combo_data()
        self.load_registrations()

    def create_widgets(self):
        title = ctk.CTkLabel(
            self,
            text="Quản lý đăng ký tham dự",
            font=ctk.CTkFont(size=30, weight="bold")
        )
        title.pack(anchor="w", padx=30, pady=(25, 5))

        subtitle = ctk.CTkLabel(
            self,
            text="Đăng ký người tham dự vào sự kiện, hủy đăng ký và check-in.",
            text_color="gray",
            font=ctk.CTkFont(size=15)
        )
        subtitle.pack(anchor="w", padx=30, pady=(0, 20))

        content = ctk.CTkFrame(self, corner_radius=15)
        content.pack(fill="both", expand=True, padx=30, pady=(0, 30))

        form_frame = ctk.CTkFrame(content, width=330, corner_radius=15)
        form_frame.pack(side="left", fill="y", padx=20, pady=20)
        form_frame.pack_propagate(False)

        table_frame = ctk.CTkFrame(content, corner_radius=15)
        table_frame.pack(side="right", fill="both", expand=True, padx=(0, 20), pady=20)

        event_label = ctk.CTkLabel(form_frame, text="Sự kiện")
        event_label.pack(anchor="w", padx=15, pady=(12, 3))

        self.event_menu = ctk.CTkOptionMenu(form_frame, values=["Chưa có sự kiện"])
        self.event_menu.pack(fill="x", padx=15, pady=(0, 8))

        attendee_label = ctk.CTkLabel(form_frame, text="Người tham dự")
        attendee_label.pack(anchor="w", padx=15, pady=(8, 3))

        self.attendee_menu = ctk.CTkOptionMenu(form_frame, values=["Chưa có người tham dự"])
        self.attendee_menu.pack(fill="x", padx=15, pady=(0, 12))

        add_button = ctk.CTkButton(form_frame, text="Đăng ký", command=self.add_registration)
        add_button.pack(fill="x", padx=15, pady=(5, 8))

        confirm_button = ctk.CTkButton(form_frame, text="Xác nhận lại", command=self.confirm_registration)
        confirm_button.pack(fill="x", padx=15, pady=4)

        cancel_button = ctk.CTkButton(
            form_frame,
            text="Hủy đăng ký",
            fg_color="#c0392b",
            hover_color="#922b21",
            command=self.cancel_registration
        )
        cancel_button.pack(fill="x", padx=15, pady=4)

        check_in_button = ctk.CTkButton(form_frame, text="Check-in", command=self.check_in_registration)
        check_in_button.pack(fill="x", padx=15, pady=(16, 4))

        undo_check_in_button = ctk.CTkButton(
            form_frame,
            text="Bỏ check-in",
            fg_color="#555555",
            hover_color="#444444",
            command=self.undo_check_in_registration
        )
        undo_check_in_button.pack(fill="x", padx=15, pady=4)

        delete_button = ctk.CTkButton(
            form_frame,
            text="Xóa khỏi danh sách",
            fg_color="#8e1b1b",
            hover_color="#641212",
            command=self.delete_registration
        )
        delete_button.pack(fill="x", padx=15, pady=(16, 4))

        clear_button = ctk.CTkButton(
            form_frame,
            text="Làm mới",
            fg_color="#555555",
            hover_color="#444444",
            command=self.clear_selection
        )
        clear_button.pack(fill="x", padx=15, pady=4)

        search_frame = ctk.CTkFrame(table_frame, fg_color="transparent")
        search_frame.pack(fill="x", padx=15, pady=(15, 10))

        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Tìm theo sự kiện, tên, email, số điện thoại..."
        )
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        search_button = ctk.CTkButton(search_frame, text="Tìm kiếm", width=100, command=self.search_registrations)
        search_button.pack(side="left")

        reset_button = ctk.CTkButton(search_frame, text="Tải lại", width=90, command=self.refresh_all)
        reset_button.pack(side="left", padx=(10, 0))

        columns = ("id", "event", "attendee", "email", "status", "check_in", "registered_at")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=16)

        self.tree.heading("id", text="Mã")
        self.tree.heading("event", text="Sự kiện")
        self.tree.heading("attendee", text="Người tham dự")
        self.tree.heading("email", text="Email")
        self.tree.heading("status", text="Trạng thái")
        self.tree.heading("check_in", text="Check-in")
        self.tree.heading("registered_at", text="Thời gian đăng ký")

        self.tree.column("id", width=45, anchor="center")
        self.tree.column("event", width=170)
        self.tree.column("attendee", width=150)
        self.tree.column("email", width=190)
        self.tree.column("status", width=100, anchor="center")
        self.tree.column("check_in", width=80, anchor="center")
        self.tree.column("registered_at", width=145, anchor="center")

        self.tree.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        self.tree.bind("<<TreeviewSelect>>", self.on_select_registration)

    def load_combo_data(self):
        events = event_controller.get_events()
        attendees = attendee_controller.get_attendees()

        self.event_options = {
            f"{event['id']} - {event['name']} ({event['date']})": event["id"]
            for event in events
        }
        self.attendee_options = {
            f"{attendee['id']} - {attendee['full_name']} ({attendee['email']})": attendee["id"]
            for attendee in attendees
        }

        event_values = list(self.event_options.keys()) or ["Chưa có sự kiện"]
        attendee_values = list(self.attendee_options.keys()) or ["Chưa có người tham dự"]

        self.event_menu.configure(values=event_values)
        self.attendee_menu.configure(values=attendee_values)
        self.event_menu.set(event_values[0])
        self.attendee_menu.set(attendee_values[0])

    def load_registrations(self):
        self.clear_table()
        registrations = registration_controller.get_registrations()
        self.insert_registrations(registrations)

    def search_registrations(self):
        self.clear_table()
        registrations = registration_controller.search_registrations(self.search_entry.get())
        self.insert_registrations(registrations)

    def insert_registrations(self, registrations):
        for registration in registrations:
            check_in_text = "Đã đến" if registration["check_in"] == 1 else "Chưa đến"
            status_text = "Đã hủy" if registration["status"] == "Cancelled" else "Đã đăng ký"

            self.tree.insert(
                "",
                "end",
                values=(
                    registration["id"],
                    registration["event_name"],
                    registration["attendee_name"],
                    registration["attendee_email"],
                    status_text,
                    check_in_text,
                    registration["registered_at"]
                )
            )

    def add_registration(self):
        event_id = self.event_options.get(self.event_menu.get())
        attendee_id = self.attendee_options.get(self.attendee_menu.get())

        try:
            registration_controller.create_registration(event_id, attendee_id)
            messagebox.showinfo("Thành công", "Đăng ký tham dự thành công.")
            self.refresh_all()
        except ValueError as error:
            messagebox.showerror("Dữ liệu không hợp lệ", str(error))

    def confirm_registration(self):
        try:
            registration_controller.confirm_registration(self.selected_registration_id)
            messagebox.showinfo("Thành công", "Đã xác nhận lại đăng ký.")
            self.refresh_all()
        except ValueError as error:
            messagebox.showwarning("Chưa chọn dữ liệu", str(error))

    def cancel_registration(self):
        try:
            registration_controller.cancel_registration(self.selected_registration_id)
            messagebox.showinfo("Thành công", "Đã hủy đăng ký.")
            self.refresh_all()
        except ValueError as error:
            messagebox.showwarning("Chưa chọn dữ liệu", str(error))

    def check_in_registration(self):
        try:
            registration_controller.check_in_registration(self.selected_registration_id)
            messagebox.showinfo("Thành công", "Check-in thành công.")
            self.refresh_all()
        except ValueError as error:
            messagebox.showwarning("Chưa chọn dữ liệu", str(error))

    def undo_check_in_registration(self):
        try:
            registration_controller.undo_check_in_registration(self.selected_registration_id)
            messagebox.showinfo("Thành công", "Đã bỏ check-in.")
            self.refresh_all()
        except ValueError as error:
            messagebox.showwarning("Chưa chọn dữ liệu", str(error))

    def delete_registration(self):
        if self.selected_registration_id is None:
            messagebox.showwarning("Chưa chọn dữ liệu", "Vui lòng chọn đăng ký cần xóa.")
            return

        confirm = messagebox.askyesno("Xác nhận xóa", "Bạn có chắc muốn xóa đăng ký này không?")
        if confirm:
            registration_controller.remove_registration(self.selected_registration_id)
            messagebox.showinfo("Thành công", "Xóa đăng ký thành công.")
            self.refresh_all()

    def on_select_registration(self, event):
        selected_item = self.tree.selection()
        if not selected_item:
            return

        values = self.tree.item(selected_item[0], "values")
        self.selected_registration_id = values[0]

    def clear_selection(self):
        self.selected_registration_id = None
        self.search_entry.delete(0, tk.END)
        for selected_item in self.tree.selection():
            self.tree.selection_remove(selected_item)

    def refresh_all(self):
        self.clear_selection()
        self.load_combo_data()
        self.load_registrations()

    def clear_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
