import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk

from controllers import event_controller


class EventsView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=0)
        self.selected_event_id = None

        self.create_widgets()
        self.load_events()

    def create_widgets(self):
        title = ctk.CTkLabel(
            self,
            text="Quản lý sự kiện",
            font=ctk.CTkFont(size=30, weight="bold")
        )
        title.pack(anchor="w", padx=30, pady=(25, 5))

        subtitle = ctk.CTkLabel(
            self,
            text="Thêm, sửa, xóa và tìm kiếm sự kiện.",
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

        self.name_entry = self.create_input(form_frame, "Tên sự kiện")
        self.date_entry = self.create_input(form_frame, "Ngày (YYYY-MM-DD)")
        self.time_entry = self.create_input(form_frame, "Giờ (HH:MM)")
        self.location_entry = self.create_input(form_frame, "Địa điểm")
        self.capacity_entry = self.create_input(form_frame, "Sức chứa")

        description_label = ctk.CTkLabel(form_frame, text="Mô tả")
        description_label.pack(anchor="w", padx=15, pady=(8, 3))

        self.description_textbox = ctk.CTkTextbox(form_frame, height=80)
        self.description_textbox.pack(fill="x", padx=15, pady=(0, 10))

        button_row_1 = ctk.CTkFrame(form_frame, fg_color="transparent")
        button_row_1.pack(fill="x", padx=15, pady=(5, 5))

        add_button = ctk.CTkButton(button_row_1, text="Thêm", command=self.add_event)
        add_button.pack(side="left", expand=True, fill="x", padx=(0, 5))

        update_button = ctk.CTkButton(button_row_1, text="Cập nhật", command=self.update_event)
        update_button.pack(side="right", expand=True, fill="x", padx=(5, 0))

        button_row_2 = ctk.CTkFrame(form_frame, fg_color="transparent")
        button_row_2.pack(fill="x", padx=15, pady=(5, 5))

        delete_button = ctk.CTkButton(
            button_row_2,
            text="Xóa",
            fg_color="#c0392b",
            hover_color="#922b21",
            command=self.delete_event
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

        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="Tìm theo tên, ngày, địa điểm...")
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        search_button = ctk.CTkButton(search_frame, text="Tìm kiếm", width=100, command=self.search_events)
        search_button.pack(side="left")

        reset_button = ctk.CTkButton(search_frame, text="Tải lại", width=90, command=self.load_events)
        reset_button.pack(side="left", padx=(10, 0))

        columns = ("id", "name", "date", "time", "location", "capacity", "description")

        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=16)

        self.tree.heading("id", text="Mã")
        self.tree.heading("name", text="Tên sự kiện")
        self.tree.heading("date", text="Ngày")
        self.tree.heading("time", text="Giờ")
        self.tree.heading("location", text="Địa điểm")
        self.tree.heading("capacity", text="Sức chứa")
        self.tree.heading("description", text="Mô tả")

        self.tree.column("id", width=40, anchor="center")
        self.tree.column("name", width=160)
        self.tree.column("date", width=100, anchor="center")
        self.tree.column("time", width=80, anchor="center")
        self.tree.column("location", width=130)
        self.tree.column("capacity", width=80, anchor="center")
        self.tree.column("description", width=220)

        self.tree.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        self.tree.bind("<<TreeviewSelect>>", self.on_select_event)

    def create_input(self, parent, label_text):
        label = ctk.CTkLabel(parent, text=label_text)
        label.pack(anchor="w", padx=15, pady=(8, 3))

        entry = ctk.CTkEntry(parent)
        entry.pack(fill="x", padx=15, pady=(0, 5))

        return entry

    def load_events(self):
        self.clear_table()

        events = event_controller.get_events()

        for event in events:
            self.tree.insert(
                "",
                "end",
                values=(
                    event["id"],
                    event["name"],
                    event["date"],
                    event["time"],
                    event["location"],
                    event["capacity"],
                    event["description"] or ""
                )
            )

    def search_events(self):
        keyword = self.search_entry.get()
        events = event_controller.search_events(keyword)

        self.clear_table()

        for event in events:
            self.tree.insert(
                "",
                "end",
                values=(
                    event["id"],
                    event["name"],
                    event["date"],
                    event["time"],
                    event["location"],
                    event["capacity"],
                    event["description"] or ""
                )
            )

    def add_event(self):
        try:
            event_controller.create_event(
                self.name_entry.get(),
                self.date_entry.get(),
                self.time_entry.get(),
                self.location_entry.get(),
                self.capacity_entry.get(),
                self.description_textbox.get("1.0", "end").strip()
            )

            messagebox.showinfo("Thành công", "Thêm sự kiện thành công.")
            self.clear_form()
            self.load_events()

        except ValueError as error:
            messagebox.showerror("Dữ liệu không hợp lệ", str(error))

    def update_event(self):
        if self.selected_event_id is None:
            messagebox.showwarning("Chưa chọn dữ liệu", "Vui lòng chọn sự kiện cần cập nhật.")
            return

        try:
            event_controller.edit_event(
                self.selected_event_id,
                self.name_entry.get(),
                self.date_entry.get(),
                self.time_entry.get(),
                self.location_entry.get(),
                self.capacity_entry.get(),
                self.description_textbox.get("1.0", "end").strip()
            )

            messagebox.showinfo("Thành công", "Cập nhật sự kiện thành công.")
            self.clear_form()
            self.load_events()

        except ValueError as error:
            messagebox.showerror("Dữ liệu không hợp lệ", str(error))

    def delete_event(self):
        if self.selected_event_id is None:
            messagebox.showwarning("Chưa chọn dữ liệu", "Vui lòng chọn sự kiện cần xóa.")
            return

        confirm = messagebox.askyesno("Xác nhận xóa", "Bạn có chắc muốn xóa sự kiện này không?")

        if confirm:
            event_controller.remove_event(self.selected_event_id)
            messagebox.showinfo("Thành công", "Xóa sự kiện thành công.")
            self.clear_form()
            self.load_events()

    def on_select_event(self, event):
        selected_item = self.tree.selection()

        if not selected_item:
            return

        values = self.tree.item(selected_item[0], "values")

        self.selected_event_id = values[0]

        self.name_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.time_entry.delete(0, tk.END)
        self.location_entry.delete(0, tk.END)
        self.capacity_entry.delete(0, tk.END)
        self.description_textbox.delete("1.0", tk.END)

        self.name_entry.insert(0, values[1])
        self.date_entry.insert(0, values[2])
        self.time_entry.insert(0, values[3])
        self.location_entry.insert(0, values[4])
        self.capacity_entry.insert(0, values[5])
        self.description_textbox.insert("1.0", values[6])

    def clear_form(self):
        self.selected_event_id = None

        self.name_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.time_entry.delete(0, tk.END)
        self.location_entry.delete(0, tk.END)
        self.capacity_entry.delete(0, tk.END)
        self.description_textbox.delete("1.0", tk.END)

        for selected_item in self.tree.selection():
            self.tree.selection_remove(selected_item)

    def clear_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
