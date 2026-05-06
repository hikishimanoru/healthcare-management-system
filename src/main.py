import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog
import database
import csv

# Setup global theme
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Color palette based on design
BG_COLOR = "#f4f7fe" # Very light gray/blue background
SURFACE_COLOR = "#ffffff" # White for cards/sidebar
PRIMARY_COLOR = "#2563eb" # Bright blue
TEXT_MAIN = "#1e293b" # Dark slate text
TEXT_SUB = "#64748b" # Gray text
BORDER_COLOR = "#e2e8f0"

class HealthcareApp:

    def __init__(self, root):
        # Initialize database
        database.initialize_database()
        
        self.root = root
        self.root.title("Healthcare Management System")
        self.root.geometry("1200x750")
        self.root.configure(fg_color=BG_COLOR)
        
        # Configure grid weight for main window
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.current_frame = None
        self.show_login()

    def clear_window(self):
        if self.current_frame is not None:
            self.current_frame.destroy()

    # ======================
    # LOGIN
    # ======================
    def show_login(self):
        self.clear_window()

        self.current_frame = ctk.CTkFrame(self.root, fg_color=BG_COLOR)
        self.current_frame.grid(row=0, column=0, sticky="nsew")

        # Main login card
        card = ctk.CTkFrame(
            self.current_frame,
            width=420,
            height=520,
            corner_radius=20,
            fg_color=SURFACE_COLOR,
            border_width=1,
            border_color=BORDER_COLOR
        )
        card.place(relx=0.5, rely=0.5, anchor="center")

        # Icon placeholder (blue circle)
        icon_frame = ctk.CTkFrame(card, width=64, height=64, corner_radius=32, fg_color=PRIMARY_COLOR)
        icon_frame.pack(pady=(45, 20))
        
        icon_label = ctk.CTkLabel(icon_frame, text="🔒", font=("Segoe UI", 26), text_color="white")
        icon_label.place(relx=0.5, rely=0.5, anchor="center")

        # Titles
        title = ctk.CTkLabel(card, text="Hệ Thống Quản Lý\nPhòng Khám", font=("Segoe UI", 22, "bold"), text_color=TEXT_MAIN, justify="center")
        title.pack(pady=(0, 5))

        subtitle = ctk.CTkLabel(card, text="Đăng nhập để tiếp tục", font=("Segoe UI", 14), text_color=TEXT_SUB)
        subtitle.pack(pady=(0, 35))

        # Inputs
        email_label = ctk.CTkLabel(card, text="Email", font=("Segoe UI", 12, "bold"), text_color=TEXT_MAIN)
        email_label.pack(anchor="w", padx=45)
        
        self.email_entry = ctk.CTkEntry(
            card, placeholder_text="admin@healthcare.com", 
            width=330, height=45, font=("Segoe UI", 14), 
            border_color=BORDER_COLOR, border_width=1, fg_color="#f8fafc", corner_radius=8
        )
        self.email_entry.pack(pady=(5, 15), padx=45)

        password_label = ctk.CTkLabel(card, text="Mật khẩu", font=("Segoe UI", 12, "bold"), text_color=TEXT_MAIN)
        password_label.pack(anchor="w", padx=45)

        self.password_entry = ctk.CTkEntry(
            card, placeholder_text="Nhập mật khẩu", show="*", 
            width=330, height=45, font=("Segoe UI", 14), 
            border_color=BORDER_COLOR, border_width=1, fg_color="#f8fafc", corner_radius=8
        )
        self.password_entry.pack(pady=(5, 30), padx=45)

        # Login button
        login_btn = ctk.CTkButton(
            card, text="Đăng nhập", width=330, height=45, 
            font=("Segoe UI", 15, "bold"), fg_color=PRIMARY_COLOR, 
            hover_color="#1d4ed8", corner_radius=8, command=self.handle_login
        )
        login_btn.pack(pady=(0, 40))

    def handle_login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        
        role = database.authenticate(email, password)
        if role:
            self.current_role = role
            self.show_dashboard()
        else:
            messagebox.showerror("Đăng nhập thất bại", "Email hoặc mật khẩu không đúng.\n\nGợi ý:\nQuản trị: admin@healthcare.com / admin123\nBác sĩ: doctor@healthcare.com / doctor123\nBệnh nhân: patient@healthcare.com / patient123")

    # ======================
    # DASHBOARD LAYOUT
    # ======================
    def show_dashboard(self):
        self.clear_window()

        self.current_frame = ctk.CTkFrame(self.root, fg_color=BG_COLOR)
        self.current_frame.grid(row=0, column=0, sticky="nsew")
        
        self.current_frame.grid_rowconfigure(0, weight=1)
        self.current_frame.grid_columnconfigure(1, weight=1)

        # Sidebar
        sidebar = ctk.CTkFrame(
            self.current_frame, width=260, corner_radius=0, 
            fg_color=SURFACE_COLOR, border_width=1, border_color=BORDER_COLOR
        )
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_rowconfigure(6, weight=1)

        # Sidebar Title
        title_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        title_frame.pack(fill="x", pady=25, padx=25)
        
        title = ctk.CTkLabel(title_frame, text="🏥 Quản Lý Phòng Khám", font=("Segoe UI", 18, "bold"), text_color=TEXT_MAIN)
        title.pack(side="left")

        # Menu Items
        self.menu_buttons = []
        role = getattr(self, 'current_role', 'patient')
        
        if role == 'admin':
            menu_items = [
                ("Tổng quan", "📊", self.page_dashboard),
                ("Bệnh nhân", "👥", self.page_patients),
                ("Bác sĩ", "⚕️", self.page_doctors),
                ("Lịch hẹn", "📅", self.page_appointments),
                ("Bệnh án", "📋", self.page_medical_records),
                ("Dịch vụ", "🏥", self.page_services),
            ]
        elif role == 'doctor':
            menu_items = [
                ("Tổng quan", "📊", self.page_dashboard),
                ("Bệnh nhân", "👥", self.page_patients),
                ("Lịch hẹn", "📅", self.page_appointments),
                ("Bệnh án", "📋", self.page_medical_records),
            ]
        else: # patient
            menu_items = [
                ("Lịch hẹn", "📅", self.page_appointments),
                ("Bệnh án", "📋", self.page_medical_records),
                ("Dịch vụ", "🏥", self.page_services),
            ]

        for i, (name, icon, cmd) in enumerate(menu_items):
            btn = ctk.CTkButton(
                sidebar,
                text=f"   {icon}   {name}",
                anchor="w",
                width=220,
                height=45,
                fg_color="transparent",
                text_color=TEXT_SUB,
                hover_color="#f1f5f9",
                font=("Segoe UI", 15),
                corner_radius=8,
                command=lambda c=cmd, idx=i: self.nav_click(c, idx)
            )
            btn.pack(pady=4, padx=20)
            self.menu_buttons.append(btn)

        # Logout
        logout_btn = ctk.CTkButton(
            sidebar,
            text="   🚪   Đăng xuất",
            anchor="w",
            width=220,
            height=45,
            fg_color="transparent",
            text_color="#ef4444",
            hover_color="#fee2e2",
            font=("Segoe UI", 15, "bold"),
            corner_radius=8,
            command=self.show_login
        )
        logout_btn.pack(side="bottom", pady=25, padx=20)

        # Main Content Area
        self.main_content = ctk.CTkFrame(self.current_frame, fg_color=BG_COLOR, corner_radius=0)
        self.main_content.grid(row=0, column=1, sticky="nsew", padx=35, pady=35)
        
        self.main_content.grid_rowconfigure(1, weight=1)
        self.main_content.grid_columnconfigure(0, weight=1)

        # Header Frame
        self.header_frame = ctk.CTkFrame(self.main_content, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew")

        self.page_title = ctk.CTkLabel(self.header_frame, text="", font=("Segoe UI", 26, "bold"), text_color=TEXT_MAIN)
        self.page_title.pack(anchor="w")

        self.page_subtitle = ctk.CTkLabel(self.header_frame, text="", font=("Segoe UI", 15), text_color=TEXT_SUB)
        self.page_subtitle.pack(anchor="w", pady=(5, 25))

        # Content Frame
        self.content_area = ctk.CTkFrame(self.main_content, fg_color="transparent")
        self.content_area.grid(row=1, column=0, sticky="nsew")

        # Initial page
        if getattr(self, 'current_role', 'patient') == 'patient':
            self.nav_click(self.page_appointments, 0)
        else:
            self.nav_click(self.page_dashboard, 0)

    def nav_click(self, cmd, idx):
        # Update button styles
        for i, btn in enumerate(self.menu_buttons):
            if i == idx:
                btn.configure(fg_color="#eff6ff", text_color=PRIMARY_COLOR, font=("Segoe UI", 15, "bold"))
            else:
                btn.configure(fg_color="transparent", text_color=TEXT_SUB, font=("Segoe UI", 15))
        # Execute command
        cmd()

    def clear_content(self):
        for widget in self.content_area.winfo_children():
            widget.destroy()

    def set_header(self, title, subtitle):
        self.page_title.configure(text=title)
        self.page_subtitle.configure(text=subtitle)

    # ======================
    # DASHBOARD PAGE
    # ======================
    def page_dashboard(self):
        self.clear_content()
        self.set_header("Tổng quan", "Toàn cảnh hoạt động của phòng khám")

        self.content_area.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # Stats Cards
        db_stats = database.get_dashboard_stats()
        stats = [
            ("Tổng Bệnh nhân", db_stats["total_patients"], "👥", "+12%", "#16a34a", "#dcfce7", "#16a34a"),
            ("Bác sĩ hoạt động", db_stats["active_doctors"], "⚕️", "+3%", "#16a34a", "#e0f2fe", "#0284c7"),
            ("Lịch hẹn hôm nay", db_stats["appointments_today"], "📅", "-5%", "#dc2626", "#ffedd5", "#ea580c"),
            ("Doanh thu", db_stats["revenue"], "📈", "+18%", "#16a34a", "#f3e8ff", "#9333ea")
        ]

        for i, (title, value, icon, change, change_color, icon_bg, icon_color) in enumerate(stats):
            card = ctk.CTkFrame(
                self.content_area, fg_color=SURFACE_COLOR, 
                corner_radius=12, border_width=1, border_color=BORDER_COLOR
            )
            card.grid(row=0, column=i, sticky="ew", padx=(0, 20) if i < 3 else 0)
            
            # Icon and Change
            top_frame = ctk.CTkFrame(card, fg_color="transparent")
            top_frame.pack(fill="x", padx=20, pady=(20, 15))
            
            # Icon background wrapper
            icon_wrapper = ctk.CTkFrame(top_frame, fg_color=icon_bg, corner_radius=8, width=40, height=40)
            icon_wrapper.pack(side="left")
            icon_wrapper.pack_propagate(False)
            
            icon_lbl = ctk.CTkLabel(icon_wrapper, text=icon, font=("Segoe UI", 18))
            icon_lbl.place(relx=0.5, rely=0.5, anchor="center")
            
            change_lbl = ctk.CTkLabel(top_frame, text=change, font=("Segoe UI", 13, "bold"), text_color=change_color)
            change_lbl.pack(side="right")

            # Title and Value
            title_lbl = ctk.CTkLabel(card, text=title, font=("Segoe UI", 13), text_color=TEXT_SUB)
            title_lbl.pack(anchor="w", padx=20)

            val_lbl = ctk.CTkLabel(card, text=value, font=("Segoe UI", 26, "bold"), text_color=TEXT_MAIN)
            val_lbl.pack(anchor="w", padx=20, pady=(0, 20))

        # Recent Appointments Section (Custom Table)
        recent_frame = ctk.CTkFrame(
            self.content_area, fg_color=SURFACE_COLOR, 
            corner_radius=12, border_width=1, border_color=BORDER_COLOR
        )
        recent_frame.grid(row=1, column=0, columnspan=4, sticky="nsew", pady=30)
        
        recent_title = ctk.CTkLabel(recent_frame, text="Lịch hẹn gần đây", font=("Segoe UI", 16, "bold"), text_color=TEXT_MAIN)
        recent_title.pack(anchor="w", padx=25, pady=20)

        columns = ["Bệnh nhân", "Bác sĩ", "Giờ khám", "Trạng thái"]
        data = database.get_recent_appointments()

        self.create_custom_table(recent_frame, columns, data)

    # ======================
    # CUSTOM TABLE TEMPLATE
    # ======================
    def create_custom_table(self, parent, columns, data, items_per_page=8):
        # Create a single grid frame for perfect column alignment
        main_frame = ctk.CTkFrame(parent, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=15)
        
        pagination_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        pagination_frame.pack(side="bottom", fill="x", pady=(10, 0))

        table_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        table_frame.pack(side="top", fill="both", expand=True)

        col_widths = [2, 2, 1, 1] if len(columns) == 4 else [1] * len(columns)
        
        total_pages = max(1, (len(data) + items_per_page - 1) // items_per_page)
        state = {"page": 0}
        
        def render_page():
            for widget in table_frame.winfo_children():
                widget.destroy()
                
            for i, width in enumerate(col_widths):
                table_frame.grid_columnconfigure(i, weight=width, uniform="colGroup")
                
            # Header
            for i, col in enumerate(columns):
                lbl = ctk.CTkLabel(table_frame, text=col, font=("Segoe UI", 13, "bold"), text_color=TEXT_SUB, anchor="w")
                lbl.grid(row=0, column=i, sticky="w", padx=10, pady=(0, 10))

            # Header bottom border
            header_border = ctk.CTkFrame(table_frame, fg_color=BORDER_COLOR, height=1)
            header_border.grid(row=1, column=0, columnspan=len(columns), sticky="ew", pady=(0, 10))

            start_idx = state["page"] * items_per_page
            end_idx = start_idx + items_per_page
            page_data = data[start_idx:end_idx]

            # Rows
            current_row = 2
            for r_idx, row in enumerate(page_data):
                for i, val in enumerate(row):
                    if columns[i] in ["Status", "Trạng thái"]:
                        status_colors = {
                            "Hoàn thành": ("#dcfce7", "#16a34a"),
                            "Đang tiến hành": ("#dbeafe", "#2563eb"),
                            "Đã lên lịch": ("#f3e8ff", "#9333ea"),
                            "Sẵn sàng": ("#dcfce7", "#16a34a"),
                            "Nghỉ phép": ("#fee2e2", "#ef4444"),
                            "Đã hủy": ("#fee2e2", "#ef4444")
                        }
                        bg, fg = status_colors.get(val, ("#f1f5f9", TEXT_SUB))
                        
                        status_frame = ctk.CTkFrame(table_frame, fg_color=bg, corner_radius=10)
                        status_frame.grid(row=current_row, column=i, sticky="w", padx=10, pady=8)
                        
                        lbl = ctk.CTkLabel(status_frame, text=val, font=("Segoe UI", 12, "bold"), text_color=fg)
                        lbl.pack(padx=12, pady=3)
                    else:
                        lbl = ctk.CTkLabel(table_frame, text=str(val), font=("Segoe UI", 14), text_color=TEXT_MAIN, anchor="w")
                        lbl.grid(row=current_row, column=i, sticky="w", padx=10, pady=12)
                
                current_row += 1
                
                # Row border
                if r_idx < len(page_data) - 1:
                    border = ctk.CTkFrame(table_frame, fg_color="#f1f5f9", height=1)
                    border.grid(row=current_row, column=0, columnspan=len(columns), sticky="ew")
                    current_row += 1
            
            # Update Pagination controls
            for widget in pagination_frame.winfo_children():
                widget.destroy()
                
            if total_pages > 1:
                prev_btn = ctk.CTkButton(
                    pagination_frame, text="◀ Trước", width=80, 
                    fg_color=PRIMARY_COLOR if state["page"] > 0 else "#cbd5e1",
                    hover_color="#1d4ed8" if state["page"] > 0 else "#cbd5e1",
                    command=go_prev
                )
                prev_btn.pack(side="left", padx=10)
                
                info_lbl = ctk.CTkLabel(pagination_frame, text=f"Trang {state['page'] + 1} / {total_pages}", font=("Segoe UI", 13, "bold"), text_color=TEXT_MAIN)
                info_lbl.pack(side="left", expand=True)
                
                next_btn = ctk.CTkButton(
                    pagination_frame, text="Sau ▶", width=80,
                    fg_color=PRIMARY_COLOR if state["page"] < total_pages - 1 else "#cbd5e1",
                    hover_color="#1d4ed8" if state["page"] < total_pages - 1 else "#cbd5e1",
                    command=go_next
                )
                next_btn.pack(side="right", padx=10)

        def go_prev():
            if state["page"] > 0:
                state["page"] -= 1
                render_page()

        def go_next():
            if state["page"] < total_pages - 1:
                state["page"] += 1
                render_page()

        render_page()

    # ======================
    # OTHER PAGES
    # ======================
    def page_patients(self):
        self.clear_content()
        self.set_header("Bệnh nhân", "Quản lý hồ sơ và chi tiết bệnh nhân")

        # Action Bar
        action_frame = ctk.CTkFrame(self.content_area, fg_color="transparent")
        action_frame.pack(fill="x", pady=(0, 15))
        
        # Search Entry
        self.search_var = tk.StringVar()
        search_entry = ctk.CTkEntry(
            action_frame, placeholder_text="Tìm theo tên...", width=250, 
            textvariable=self.search_var, border_color=BORDER_COLOR
        )
        search_entry.pack(side="left", padx=(0, 10))
        
        search_btn = ctk.CTkButton(
            action_frame, text="🔍 Tìm kiếm", font=("Segoe UI", 13, "bold"), width=100,
            command=self.refresh_patients_table
        )
        search_btn.pack(side="left")
        
        add_btn = ctk.CTkButton(
            action_frame, text="➕ Thêm Bệnh nhân", font=("Segoe UI", 14, "bold"),
            fg_color=PRIMARY_COLOR, hover_color="#1d4ed8", corner_radius=8,
            command=self.show_add_patient_dialog
        )
        add_btn.pack(side="right")
        
        if getattr(self, 'current_role', 'patient') == 'admin':
            export_btn = ctk.CTkButton(
                action_frame, text="📥 Xuất CSV", font=("Segoe UI", 14, "bold"),
                fg_color="#10b981", hover_color="#059669", corner_radius=8,
                command=self.export_patients_csv
            )
            export_btn.pack(side="right", padx=(0, 10))

        self.patients_table_frame = ctk.CTkFrame(self.content_area, fg_color=SURFACE_COLOR, corner_radius=12, border_width=1, border_color=BORDER_COLOR)
        self.patients_table_frame.pack(fill="both", expand=True)

        self.refresh_patients_table()

    def refresh_patients_table(self):
        for widget in self.patients_table_frame.winfo_children():
            widget.destroy()
            
        query = self.search_var.get()
        columns = ["Họ tên", "Tuổi", "Giới tính", "Liên hệ", "Khám lần cuối"]
        data = database.get_patients(query)
        self.create_custom_table(self.patients_table_frame, columns, data)

    def export_patients_csv(self):
        data = database.get_patients() # Get all without filter or use self.search_var.get() if you want filtered export
        if not data:
            messagebox.showinfo("Export", "Không có dữ liệu để xuất.")
            return
            
        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")],
            title="Xuất Dữ liệu Bệnh nhân",
            initialfile="du_lieu_benh_nhan.csv"
        )
        if filepath:
            try:
                with open(filepath, mode='w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(["Họ tên", "Tuổi", "Giới tính", "Liên hệ", "Khám lần cuối"])
                    writer.writerows(data)
                messagebox.showinfo("Thành công", "Đã xuất dữ liệu thành công!")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể xuất dữ liệu: {e}")

    def show_add_patient_dialog(self):
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Thêm Bệnh nhân mới")
        dialog.geometry("420x550")
        dialog.configure(fg_color=BG_COLOR)
        dialog.grab_set() # Chặn click vào cửa sổ chính
        dialog.focus()
        
        title = ctk.CTkLabel(dialog, text="Thông tin Bệnh nhân", font=("Segoe UI", 20, "bold"), text_color=TEXT_MAIN)
        title.pack(pady=(25, 15))
        
        # Form Inputs
        entries = {}
        fields = [
            ("Họ tên", "Ví dụ: Nguyễn Văn A"), 
            ("Tuổi", "Ví dụ: 35"), 
            ("Giới tính", "Ví dụ: Nam / Nữ"), 
            ("Liên hệ", "Ví dụ: 0912345678"), 
            ("Khám lần cuối", "Ví dụ: 2026-04-20")
        ]
        
        for field, placeholder in fields:
            frame = ctk.CTkFrame(dialog, fg_color="transparent")
            frame.pack(fill="x", padx=40, pady=8)
            
            lbl = ctk.CTkLabel(frame, text=field, font=("Segoe UI", 13, "bold"), text_color=TEXT_MAIN, width=90, anchor="w")
            lbl.pack(side="left")
            
            ent = ctk.CTkEntry(frame, width=220, border_color=BORDER_COLOR, placeholder_text=placeholder)
            ent.pack(side="right", fill="x", expand=True)
            entries[field] = ent
            
        def save_patient():
            name = entries["Họ tên"].get().strip()
            age = entries["Tuổi"].get().strip()
            gender = entries["Giới tính"].get().strip()
            contact = entries["Liên hệ"].get().strip()
            last_visit = entries["Khám lần cuối"].get().strip()
            
            if not name or not age:
                messagebox.showerror("Lỗi", "Họ tên và Tuổi là bắt buộc!", parent=dialog)
                return
                
            if not age.isdigit():
                messagebox.showerror("Lỗi", "Tuổi phải là một số!", parent=dialog)
                return
                
            # Lưu vào CSDL
            database.add_patient(name, age, gender, contact, last_visit)
            dialog.destroy()
            
            # Tải lại trang để hiện dữ liệu mới
            messagebox.showinfo("Thành công", "Đã thêm bệnh nhân thành công!")
            self.page_patients()
            
        save_btn = ctk.CTkButton(
            dialog, text="Lưu Bệnh nhân", fg_color="#16a34a", hover_color="#15803d", 
            font=("Segoe UI", 15, "bold"), height=40, command=save_patient
        )
        save_btn.pack(pady=35)

    def page_doctors(self):
        self.clear_content()
        self.set_header("Bác sĩ", "Danh sách và quản lý bác sĩ")

        # Action Bar
        action_frame = ctk.CTkFrame(self.content_area, fg_color="transparent")
        action_frame.pack(fill="x", pady=(0, 15))
        
        if getattr(self, 'current_role', 'patient') == 'admin':
            del_btn = ctk.CTkButton(
                action_frame, text="🗑️ Xóa Bác sĩ", font=("Segoe UI", 14, "bold"),
                fg_color="#ef4444", hover_color="#dc2626", corner_radius=8,
                command=self.show_delete_doctor_dialog
            )
            del_btn.pack(side="right", padx=(10, 0))

            add_btn = ctk.CTkButton(
                action_frame, text="➕ Thêm Bác sĩ", font=("Segoe UI", 14, "bold"),
                fg_color=PRIMARY_COLOR, hover_color="#1d4ed8", corner_radius=8,
                command=self.show_add_doctor_dialog
            )
            add_btn.pack(side="right")

        frame = ctk.CTkFrame(self.content_area, fg_color=SURFACE_COLOR, corner_radius=12, border_width=1, border_color=BORDER_COLOR)
        frame.pack(fill="both", expand=True)

        columns = ["Họ tên", "Chuyên khoa", "Kinh nghiệm", "Liên hệ", "Trạng thái"]
        data = database.get_doctors()
        self.create_custom_table(frame, columns, data)

    def show_add_doctor_dialog(self):
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Thêm Bác sĩ mới")
        dialog.geometry("420x550")
        dialog.configure(fg_color=BG_COLOR)
        dialog.grab_set()
        dialog.focus()
        
        title = ctk.CTkLabel(dialog, text="Thông tin Bác sĩ", font=("Segoe UI", 20, "bold"), text_color=TEXT_MAIN)
        title.pack(pady=(25, 15))
        
        entries = {}
        fields = [
            ("Họ tên", "Ví dụ: BS. Trần Thanh Tâm"), 
            ("Chuyên khoa", "Ví dụ: Tim mạch"), 
            ("Kinh nghiệm", "Ví dụ: 10 năm"), 
            ("Liên hệ", "Ví dụ: 0988111222"), 
            ("Trạng thái", ["Sẵn sàng", "Nghỉ phép"])
        ]
        
        for field, config in fields:
            frame = ctk.CTkFrame(dialog, fg_color="transparent")
            frame.pack(fill="x", padx=40, pady=8)
            
            lbl = ctk.CTkLabel(frame, text=field, font=("Segoe UI", 13, "bold"), text_color=TEXT_MAIN, width=90, anchor="w")
            lbl.pack(side="left")
            
            if field == "Trạng thái":
                ent = ctk.CTkOptionMenu(frame, values=config, width=220, fg_color="#f8fafc", text_color=TEXT_MAIN, button_color=PRIMARY_COLOR)
                ent.set("Sẵn sàng")
            else:
                ent = ctk.CTkEntry(frame, width=220, border_color=BORDER_COLOR, placeholder_text=config)
            ent.pack(side="right", fill="x", expand=True)
            entries[field] = ent
            
        def save_doctor():
            name = entries["Họ tên"].get().strip()
            specialty = entries["Chuyên khoa"].get().strip()
            experience = entries["Kinh nghiệm"].get().strip()
            contact = entries["Liên hệ"].get().strip()
            status = entries["Trạng thái"].get()
            
            if not name or not specialty:
                messagebox.showerror("Lỗi", "Tên và Chuyên khoa là bắt buộc!", parent=dialog)
                return
                
            database.add_doctor(name, specialty, experience, contact, status)
            dialog.destroy()
            messagebox.showinfo("Thành công", "Đã thêm bác sĩ thành công!")
            self.page_doctors()
            
        save_btn = ctk.CTkButton(dialog, text="Lưu Bác sĩ", fg_color="#16a34a", hover_color="#15803d", font=("Segoe UI", 15, "bold"), height=40, command=save_doctor)
        save_btn.pack(pady=35)

    def show_delete_doctor_dialog(self):
        doctors = database.get_doctor_names()
        if not doctors:
            messagebox.showinfo("Thông báo", "Không có bác sĩ nào để xóa.")
            return

        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Xóa Bác sĩ")
        dialog.geometry("350x250")
        dialog.configure(fg_color=BG_COLOR)
        dialog.grab_set()
        
        title = ctk.CTkLabel(dialog, text="Chọn Bác sĩ cần xóa", font=("Segoe UI", 16, "bold"), text_color=TEXT_MAIN)
        title.pack(pady=20)
        
        combo = ctk.CTkOptionMenu(dialog, values=doctors, width=250)
        combo.pack(pady=10)
        
        def confirm_delete():
            selected = combo.get()
            if selected:
                database.delete_doctor(selected)
                dialog.destroy()
                messagebox.showinfo("Thành công", f"Đã xóa bác sĩ '{selected}'.")
                self.page_doctors()
                
        btn = ctk.CTkButton(dialog, text="Xác nhận xóa", fg_color="#ef4444", hover_color="#dc2626", font=("Segoe UI", 14, "bold"), command=confirm_delete)
        btn.pack(pady=20)

    def page_appointments(self):
        self.clear_content()
        self.set_header("Lịch hẹn", "Quản lý và đặt lịch hẹn khám")

        # Action Bar
        action_frame = ctk.CTkFrame(self.content_area, fg_color="transparent")
        action_frame.pack(fill="x", pady=(0, 15))

        add_btn = ctk.CTkButton(
            action_frame, text="📅 Đặt lịch khám", font=("Segoe UI", 14, "bold"),
            fg_color=PRIMARY_COLOR, hover_color="#1d4ed8", corner_radius=8,
            command=self.show_book_appointment_dialog
        )
        add_btn.pack(side="right")
        
        if getattr(self, 'current_role', 'patient') in ['admin', 'doctor']:
            del_btn = ctk.CTkButton(
                action_frame, text="🗑️ Xóa Lịch hẹn", font=("Segoe UI", 14, "bold"),
                fg_color="#ef4444", hover_color="#dc2626", corner_radius=8,
                command=self.show_delete_appointment_dialog
            )
            del_btn.pack(side="right", padx=(10, 10))

            upd_btn = ctk.CTkButton(
                action_frame, text="✏️ Cập nhật/Hủy", font=("Segoe UI", 14, "bold"),
                fg_color="#f59e0b", hover_color="#d97706", corner_radius=8,
                command=self.show_update_appointment_dialog
            )
            upd_btn.pack(side="right")

        frame = ctk.CTkFrame(self.content_area, fg_color=SURFACE_COLOR, corner_radius=12, border_width=1, border_color=BORDER_COLOR)
        frame.pack(fill="both", expand=True)

        columns = ["Bệnh nhân", "Bác sĩ", "Ngày", "Giờ", "Loại khám", "Trạng thái"]
        data = database.get_appointments()
        self.create_custom_table(frame, columns, data)

    def show_book_appointment_dialog(self):
        patients = database.get_patient_names()
        doctors = database.get_doctor_names(only_available=True)
        
        if not patients or not doctors:
            messagebox.showwarning("Cảnh báo", "Cần có ít nhất một bệnh nhân và một bác sĩ Sẵn sàng để đặt lịch.")
            return

        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Đặt lịch khám")
        dialog.geometry("420x550")
        dialog.configure(fg_color=BG_COLOR)
        dialog.grab_set()
        dialog.focus()
        
        title = ctk.CTkLabel(dialog, text="Chi tiết lịch hẹn", font=("Segoe UI", 20, "bold"), text_color=TEXT_MAIN)
        title.pack(pady=(25, 15))
        
        import datetime
        today = datetime.date.today()
        dates = [(today + datetime.timedelta(days=i)).strftime("%Y-%m-%d") for i in range(14)]
        times = ["08:00 AM", "09:00 AM", "10:00 AM", "11:00 AM", "01:00 PM", "02:00 PM", "03:00 PM", "04:00 PM", "05:00 PM"]
        
        entries = {}
        fields = [
            ("Bệnh nhân", patients), 
            ("Bác sĩ", doctors), 
            ("Ngày", dates), 
            ("Giờ", times),
            ("Loại khám", ["Khám định kỳ", "Tư vấn", "Tái khám", "Điều trị", "Cấp cứu"]),
            ("Trạng thái", ["Đã lên lịch", "Đang tiến hành", "Hoàn thành"])
        ]
        
        for field, config in fields:
            frame = ctk.CTkFrame(dialog, fg_color="transparent")
            frame.pack(fill="x", padx=40, pady=8)
            
            lbl = ctk.CTkLabel(frame, text=field, font=("Segoe UI", 13, "bold"), text_color=TEXT_MAIN, width=90, anchor="w")
            lbl.pack(side="left")
            
            if isinstance(config, list):
                ent = ctk.CTkOptionMenu(frame, values=config, width=220, fg_color="#f8fafc", text_color=TEXT_MAIN, button_color=PRIMARY_COLOR)
                ent.set(config[0])
            else:
                ent = ctk.CTkEntry(frame, width=220, border_color=BORDER_COLOR, placeholder_text=config)
            ent.pack(side="right", fill="x", expand=True)
            entries[field] = ent
            
        def save_appointment():
            patient = entries["Bệnh nhân"].get()
            doctor = entries["Bác sĩ"].get()
            date = entries["Ngày"].get().strip()
            time = entries["Giờ"].get().strip()
            app_type = entries["Loại khám"].get().strip()
            status = entries["Trạng thái"].get()
            
            if not date or not time:
                messagebox.showerror("Lỗi", "Ngày và Giờ là bắt buộc!", parent=dialog)
                return
                
            import re
            if not re.match(r"^\d{4}-\d{2}-\d{2}$", date):
                messagebox.showerror("Lỗi", "Ngày phải đúng định dạng YYYY-MM-DD!", parent=dialog)
                return
                
            if database.check_appointment_conflict(doctor, date, time):
                messagebox.showerror(
                    "Trùng lịch", 
                    f"Trùng lịch! {doctor} đã có lịch hẹn khác vào lúc {time} ngày {date}.", 
                    parent=dialog
                )
                return
                
            database.add_appointment(patient, doctor, date, time, app_type, status)
            dialog.destroy()
            messagebox.showinfo("Thành công", "Đã đặt lịch thành công!")
            self.page_appointments()
            
        save_btn = ctk.CTkButton(dialog, text="Xác nhận đặt lịch", fg_color="#16a34a", hover_color="#15803d", font=("Segoe UI", 15, "bold"), height=40, command=save_appointment)
        save_btn.pack(pady=30)

    def show_update_appointment_dialog(self):
        apps = database.get_appointment_options()
        if not apps:
            messagebox.showinfo("Thông báo", "Không có lịch hẹn nào.")
            return

        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Cập nhật / Hủy Lịch hẹn")
        dialog.geometry("400x350")
        dialog.configure(fg_color=BG_COLOR)
        dialog.grab_set()
        
        title = ctk.CTkLabel(dialog, text="Chọn Lịch hẹn", font=("Segoe UI", 16, "bold"), text_color=TEXT_MAIN)
        title.pack(pady=20)
        
        combo = ctk.CTkOptionMenu(dialog, values=apps, width=350)
        combo.pack(pady=10)
        
        status_label = ctk.CTkLabel(dialog, text="Trạng thái mới:", font=("Segoe UI", 14, "bold"), text_color=TEXT_MAIN)
        status_label.pack(pady=(15, 5))
        
        status_combo = ctk.CTkOptionMenu(dialog, values=["Đã lên lịch", "Đang tiến hành", "Hoàn thành", "Đã hủy"], width=200, fg_color="#f8fafc", text_color=TEXT_MAIN, button_color=PRIMARY_COLOR)
        status_combo.pack(pady=5)
        
        def confirm_update():
            selected = combo.get()
            new_status = status_combo.get()
            if selected:
                try:
                    app_id = int(selected.split("]")[0].replace("[", ""))
                    database.update_appointment_status(app_id, new_status)
                    dialog.destroy()
                    messagebox.showinfo("Thành công", "Đã cập nhật trạng thái lịch hẹn.")
                    self.page_appointments()
                except:
                    messagebox.showerror("Lỗi", "Không thể cập nhật.")
                
        btn = ctk.CTkButton(dialog, text="Xác nhận", fg_color="#16a34a", hover_color="#15803d", font=("Segoe UI", 14, "bold"), command=confirm_update)
        btn.pack(pady=20)

    def show_delete_appointment_dialog(self):
        apps = database.get_appointment_options()
        if not apps:
            messagebox.showinfo("Thông báo", "Không có lịch hẹn nào.")
            return

        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Xóa Lịch hẹn")
        dialog.geometry("400x250")
        dialog.configure(fg_color=BG_COLOR)
        dialog.grab_set()
        
        title = ctk.CTkLabel(dialog, text="Chọn Lịch hẹn cần xóa", font=("Segoe UI", 16, "bold"), text_color=TEXT_MAIN)
        title.pack(pady=20)
        
        combo = ctk.CTkOptionMenu(dialog, values=apps, width=350)
        combo.pack(pady=10)
        
        def confirm_delete():
            selected = combo.get()
            if selected:
                try:
                    app_id = int(selected.split("]")[0].replace("[", ""))
                    database.delete_appointment(app_id)
                    dialog.destroy()
                    messagebox.showinfo("Thành công", "Đã xóa lịch hẹn.")
                    self.page_appointments()
                except:
                    messagebox.showerror("Lỗi", "Không thể xóa.")
                
        btn = ctk.CTkButton(dialog, text="Xác nhận xóa", fg_color="#ef4444", hover_color="#dc2626", font=("Segoe UI", 14, "bold"), command=confirm_delete)
        btn.pack(pady=20)

    def page_medical_records(self):
        self.clear_content()
        self.set_header("Hồ sơ bệnh án", "Tra cứu và quản lý hồ sơ y tế")

        action_frame = ctk.CTkFrame(self.content_area, fg_color="transparent")
        action_frame.pack(fill="x", pady=(0, 15))
        
        self.record_search_var = tk.StringVar()
        search_entry = ctk.CTkEntry(
            action_frame, placeholder_text="Tìm theo tên bệnh nhân...", width=250, 
            textvariable=self.record_search_var, border_color=BORDER_COLOR
        )
        search_entry.pack(side="left", padx=(0, 10))
        
        search_btn = ctk.CTkButton(
            action_frame, text="🔍 Tìm kiếm", font=("Segoe UI", 13, "bold"), width=100,
            command=self.refresh_records_table
        )
        search_btn.pack(side="left")

        if getattr(self, 'current_role', 'patient') in ['admin', 'doctor']:
            add_btn = ctk.CTkButton(
                action_frame, text="➕ Thêm Bệnh án", font=("Segoe UI", 14, "bold"),
                fg_color=PRIMARY_COLOR, hover_color="#1d4ed8", corner_radius=8,
                command=self.show_add_record_dialog
            )
            add_btn.pack(side="right")
            
            export_btn = ctk.CTkButton(
                action_frame, text="📥 Xuất CSV", font=("Segoe UI", 14, "bold"),
                fg_color="#10b981", hover_color="#059669", corner_radius=8,
                command=self.export_records_csv
            )
            export_btn.pack(side="right", padx=(0, 10))

        self.records_table_frame = ctk.CTkFrame(self.content_area, fg_color=SURFACE_COLOR, corner_radius=12, border_width=1, border_color=BORDER_COLOR)
        self.records_table_frame.pack(fill="both", expand=True)

        self.refresh_records_table()

    def refresh_records_table(self):
        for widget in self.records_table_frame.winfo_children():
            widget.destroy()
            
        query = self.record_search_var.get()
        columns = ["Bệnh nhân", "Bác sĩ", "Ngày khám", "Chẩn đoán", "Đơn thuốc"]
        data = database.get_medical_records(query)
        self.create_custom_table(self.records_table_frame, columns, data)

    def export_records_csv(self):
        data = database.get_medical_records() 
        if not data:
            messagebox.showinfo("Export", "Không có dữ liệu để xuất.")
            return
            
        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")],
            title="Xuất Dữ liệu Bệnh án",
            initialfile="du_lieu_benh_an.csv"
        )
        if filepath:
            try:
                with open(filepath, mode='w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(["Bệnh nhân", "Bác sĩ", "Ngày khám", "Chẩn đoán", "Đơn thuốc"])
                    writer.writerows(data)
                messagebox.showinfo("Thành công", "Đã xuất dữ liệu thành công!")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể xuất dữ liệu: {e}")

    def show_add_record_dialog(self):
        patients = database.get_patient_names()
        doctors = database.get_doctor_names()
        
        if not patients or not doctors:
            messagebox.showwarning("Cảnh báo", "Cần có ít nhất một bệnh nhân và một bác sĩ.")
            return

        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Thêm Hồ sơ Bệnh án")
        dialog.geometry("450x550")
        dialog.configure(fg_color=BG_COLOR)
        dialog.grab_set()
        dialog.focus()
        
        title = ctk.CTkLabel(dialog, text="Chi tiết Bệnh án", font=("Segoe UI", 20, "bold"), text_color=TEXT_MAIN)
        title.pack(pady=(25, 15))
        
        import datetime
        today = datetime.date.today().strftime("%Y-%m-%d")
        
        entries = {}
        fields = [
            ("Bệnh nhân", patients), 
            ("Bác sĩ", doctors), 
            ("Ngày khám", today), 
            ("Chẩn đoán", "Ví dụ: Viêm họng hạt"),
            ("Đơn thuốc", "Ví dụ: Amoxicillin 500mg, 2 viên/ngày")
        ]
        
        for field, config in fields:
            frame = ctk.CTkFrame(dialog, fg_color="transparent")
            frame.pack(fill="x", padx=40, pady=8)
            
            lbl = ctk.CTkLabel(frame, text=field, font=("Segoe UI", 13, "bold"), text_color=TEXT_MAIN, width=90, anchor="w")
            lbl.pack(side="left")
            
            if isinstance(config, list):
                ent = ctk.CTkOptionMenu(frame, values=config, width=220, fg_color="#f8fafc", text_color=TEXT_MAIN, button_color=PRIMARY_COLOR)
                ent.set(config[0])
            else:
                ent = ctk.CTkEntry(frame, width=220, border_color=BORDER_COLOR, placeholder_text=config if isinstance(config, str) else "")
                if field == "Ngày khám":
                    ent.insert(0, config)
            ent.pack(side="right", fill="x", expand=True)
            entries[field] = ent
            
        def save_record():
            patient = entries["Bệnh nhân"].get()
            doctor = entries["Bác sĩ"].get()
            date = entries["Ngày khám"].get().strip()
            diagnosis = entries["Chẩn đoán"].get().strip()
            prescription = entries["Đơn thuốc"].get().strip()
            
            if not date or not diagnosis:
                messagebox.showerror("Lỗi", "Ngày khám và Chẩn đoán là bắt buộc!", parent=dialog)
                return
                
            database.add_medical_record(patient, doctor, date, diagnosis, prescription)
            dialog.destroy()
            messagebox.showinfo("Thành công", "Đã thêm bệnh án thành công!")
            self.page_medical_records()
            
        save_btn = ctk.CTkButton(dialog, text="Lưu Bệnh án", fg_color="#16a34a", hover_color="#15803d", font=("Segoe UI", 15, "bold"), height=40, command=save_record)
        save_btn.pack(pady=30)

    def page_services(self):
        self.clear_content()
        self.set_header("Dịch vụ", "Bảng giá và dịch vụ y tế")

        action_frame = ctk.CTkFrame(self.content_area, fg_color="transparent")
        action_frame.pack(fill="x", pady=(0, 15))
        
        if getattr(self, 'current_role', 'patient') in ['admin', 'doctor']:
            del_btn = ctk.CTkButton(
                action_frame, text="🗑️ Xóa Dịch vụ", font=("Segoe UI", 14, "bold"),
                fg_color="#ef4444", hover_color="#dc2626", corner_radius=8,
                command=self.show_delete_service_dialog
            )
            del_btn.pack(side="right", padx=(10, 0))

            add_btn = ctk.CTkButton(
                action_frame, text="➕ Thêm Dịch vụ", font=("Segoe UI", 14, "bold"),
                fg_color=PRIMARY_COLOR, hover_color="#1d4ed8", corner_radius=8,
                command=self.show_add_service_dialog
            )
            add_btn.pack(side="right")

        frame = ctk.CTkFrame(self.content_area, fg_color=SURFACE_COLOR, corner_radius=12, border_width=1, border_color=BORDER_COLOR)
        frame.pack(fill="both", expand=True)

        columns = ["Tên dịch vụ", "Danh mục", "Giá", "Thời lượng"]
        data = database.get_services()
        self.create_custom_table(frame, columns, data)

    def show_add_service_dialog(self):
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Thêm Dịch vụ mới")
        dialog.geometry("400x500")
        dialog.configure(fg_color=BG_COLOR)
        dialog.grab_set()
        
        title = ctk.CTkLabel(dialog, text="Thông tin Dịch vụ", font=("Segoe UI", 20, "bold"), text_color=TEXT_MAIN)
        title.pack(pady=(25, 15))
        
        entries = {}
        fields = [
            ("Tên dịch vụ", "Ví dụ: Xét nghiệm máu"), 
            ("Danh mục", ["Cơ bản", "Xét nghiệm", "Hình ảnh", "Điều trị"]),
            ("Giá", "Ví dụ: 300,000đ"), 
            ("Thời lượng", "Ví dụ: 15 phút")
        ]
        
        for field, config in fields:
            frame = ctk.CTkFrame(dialog, fg_color="transparent")
            frame.pack(fill="x", padx=40, pady=8)
            
            lbl = ctk.CTkLabel(frame, text=field, font=("Segoe UI", 13, "bold"), text_color=TEXT_MAIN, width=90, anchor="w")
            lbl.pack(side="left")
            
            if isinstance(config, list):
                ent = ctk.CTkOptionMenu(frame, values=config, width=200, fg_color="#f8fafc", text_color=TEXT_MAIN, button_color=PRIMARY_COLOR)
                ent.set(config[0])
            else:
                ent = ctk.CTkEntry(frame, width=200, border_color=BORDER_COLOR, placeholder_text=config)
            ent.pack(side="right", fill="x", expand=True)
            entries[field] = ent
            
        def save_service():
            name = entries["Tên dịch vụ"].get().strip()
            category = entries["Danh mục"].get()
            price = entries["Giá"].get().strip()
            duration = entries["Thời lượng"].get().strip()
            
            if not name or not price:
                messagebox.showerror("Lỗi", "Tên dịch vụ và Giá là bắt buộc!", parent=dialog)
                return
                
            database.add_service(name, category, price, duration)
            dialog.destroy()
            messagebox.showinfo("Thành công", "Đã thêm dịch vụ thành công!")
            self.page_services()
            
        save_btn = ctk.CTkButton(dialog, text="Lưu Dịch vụ", fg_color="#16a34a", hover_color="#15803d", font=("Segoe UI", 15, "bold"), height=40, command=save_service)
        save_btn.pack(pady=30)

    def show_delete_service_dialog(self):
        services = database.get_service_names()
        if not services:
            messagebox.showinfo("Thông báo", "Không có dịch vụ nào.")
            return

        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Xóa Dịch vụ")
        dialog.geometry("350x250")
        dialog.configure(fg_color=BG_COLOR)
        dialog.grab_set()
        
        title = ctk.CTkLabel(dialog, text="Chọn Dịch vụ cần xóa", font=("Segoe UI", 16, "bold"), text_color=TEXT_MAIN)
        title.pack(pady=20)
        
        combo = ctk.CTkOptionMenu(dialog, values=services, width=250)
        combo.pack(pady=10)
        
        def confirm_delete():
            selected = combo.get()
            if selected:
                database.delete_service(selected)
                dialog.destroy()
                messagebox.showinfo("Thành công", f"Đã xóa dịch vụ '{selected}'.")
                self.page_services()
                
        btn = ctk.CTkButton(dialog, text="Xác nhận xóa", fg_color="#ef4444", hover_color="#dc2626", font=("Segoe UI", 14, "bold"), command=confirm_delete)
        btn.pack(pady=20)

if __name__ == "__main__":
    root = ctk.CTk()
    app = HealthcareApp(root)
    root.mainloop()