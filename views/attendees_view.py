import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk

from controllers import attendee_controller


class AttendeesView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=0)
        self.selected_attendee_id = None

        self.create_widgets()
        self.load_attendees()

    def create_widgets(self):
        title = ctk.CTkLabel(
            self,
            text="Quản lý người tham dự",
            font=ctk.CTkFont(size=30, weight="bold")
        )
        title.pack(anchor="w", padx=30, pady=(25, 5))

        subtitle = ctk.CTkLabel(
            self,
            text="Thêm, sửa, xóa và tìm kiếm người tham dự.",
            text_color="gray",
            font=ctk.CTkFont(size=15)
        )
        subtitle.pack(anchor="w", padx=30, pady=(0, 20))

        content = ctk.CTkFrame(self, corner_radius=15)
        content.pack(fill="both", expand=True, padx=30, pady=(0, 30))

        form_frame = ctk.CTkFrame(content, width=310, corner_radius=15)
        form_frame.pack(side="left", fill="y", padx=20, pady=20)
        form_frame.pack_propagate(False)

        table_frame = ctk.CTkFrame(content, corner_radius=15)
        table_frame.pack(side="right", fill="both", expand=True, padx=(0, 20), pady=20)

        self.full_name_entry = self.create_input(form_frame, "Họ và tên")
        self.email_entry = self.create_input(form_frame, "Email")
        self.phone_entry = self.create_input(form_frame, "Số điện thoại")

        button_row_1 = ctk.CTkFrame(form_frame, fg_color="transparent")
        button_row_1.pack(fill="x", padx=15, pady=(15, 5))

        add_button = ctk.CTkButton(button_row_1, text="Thêm", command=self.add_attendee)
        add_button.pack(side="left", expand=True, fill="x", padx=(0, 5))

        update_button = ctk.CTkButton(button_row_1, text="Cập nhật", command=self.update_attendee)
        update_button.pack(side="right", expand=True, fill="x", padx=(5, 0))

        button_row_2 = ctk.CTkFrame(form_frame, fg_color="transparent")
        button_row_2.pack(fill="x", padx=15, pady=(5, 5))

        delete_button = ctk.CTkButton(
            button_row_2,
            text="Xóa",
            fg_color="#c0392b",
            hover_color="#922b21",
            command=self.delete_attendee
        )
        delete_button.pack(side="left", expand=True, fill="x", padx=(0, 5))

        clear_button = ctk.CTkButton(
            button_row_2,
            text="Làm mới",
            fg_color="#555555",
            hover_color="#444444",
            command=self.clear_form
        )
        clear_button.pack(side="right", expand=True, fill="x", padx=(5, 0))

        search_frame = ctk.CTkFrame(table_frame, fg_color="transparent")
        search_frame.pack(fill="x", padx=15, pady=(15, 10))

        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Tìm theo tên, email hoặc số điện thoại..."
        )
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        search_button = ctk.CTkButton(search_frame, text="Tìm kiếm", width=100, command=self.search_attendees)
        search_button.pack(side="left")

        reset_button = ctk.CTkButton(search_frame, text="Tải lại", width=90, command=self.load_attendees)
        reset_button.pack(side="left", padx=(10, 0))

        columns = ("id", "full_name", "email", "phone")

        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=16)

        self.tree.heading("id", text="Mã")
        self.tree.heading("full_name", text="Họ và tên")
        self.tree.heading("email", text="Email")
        self.tree.heading("phone", text="Số điện thoại")

        self.tree.column("id", width=50, anchor="center")
        self.tree.column("full_name", width=220)
        self.tree.column("email", width=240)
        self.tree.column("phone", width=140, anchor="center")

        self.tree.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        self.tree.bind("<<TreeviewSelect>>", self.on_select_attendee)

    def create_input(self, parent, label_text):
        label = ctk.CTkLabel(parent, text=label_text)
        label.pack(anchor="w", padx=15, pady=(8, 3))

        entry = ctk.CTkEntry(parent)
        entry.pack(fill="x", padx=15, pady=(0, 5))

        return entry

    def load_attendees(self):
        self.clear_table()

        attendees = attendee_controller.get_attendees()

        for attendee in attendees:
            self.tree.insert(
                "",
                "end",
                values=(
                    attendee["id"],
                    attendee["full_name"],
                    attendee["email"],
                    attendee["phone"]
                )
            )

    def search_attendees(self):
        keyword = self.search_entry.get()
        attendees = attendee_controller.search_attendees(keyword)

        self.clear_table()

        for attendee in attendees:
            self.tree.insert(
                "",
                "end",
                values=(
                    attendee["id"],
                    attendee["full_name"],
                    attendee["email"],
                    attendee["phone"]
                )
            )

    def add_attendee(self):
        try:
            attendee_controller.create_attendee(
                self.full_name_entry.get(),
                self.email_entry.get(),
                self.phone_entry.get()
            )

            messagebox.showinfo("Thành công", "Thêm người tham dự thành công.")
            self.clear_form()
            self.load_attendees()

        except ValueError as error:
            messagebox.showerror("Dữ liệu không hợp lệ", str(error))

    def update_attendee(self):
        if self.selected_attendee_id is None:
            messagebox.showwarning("Chưa chọn dữ liệu", "Vui lòng chọn người tham dự cần cập nhật.")
            return

        try:
            attendee_controller.edit_attendee(
                self.selected_attendee_id,
                self.full_name_entry.get(),
                self.email_entry.get(),
                self.phone_entry.get()
            )

            messagebox.showinfo("Thành công", "Cập nhật người tham dự thành công.")
            self.clear_form()
            self.load_attendees()

        except ValueError as error:
            messagebox.showerror("Dữ liệu không hợp lệ", str(error))

    def delete_attendee(self):
        if self.selected_attendee_id is None:
            messagebox.showwarning("Chưa chọn dữ liệu", "Vui lòng chọn người tham dự cần xóa.")
            return

        confirm = messagebox.askyesno(
            "Xác nhận xóa",
            "Bạn có chắc muốn xóa người tham dự này không?"
        )

        if confirm:
            attendee_controller.remove_attendee(self.selected_attendee_id)
            messagebox.showinfo("Thành công", "Xóa người tham dự thành công.")
            self.clear_form()
            self.load_attendees()

    def on_select_attendee(self, event):
        selected_item = self.tree.selection()

        if not selected_item:
            return

        values = self.tree.item(selected_item[0], "values")

        self.selected_attendee_id = values[0]

        self.full_name_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)

        self.full_name_entry.insert(0, values[1])
        self.email_entry.insert(0, values[2])
        self.phone_entry.insert(0, values[3])

    def clear_form(self):
        self.selected_attendee_id = None

        self.full_name_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)

        for selected_item in self.tree.selection():
            self.tree.selection_remove(selected_item)

    def clear_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
