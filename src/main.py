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
        title = ctk.CTkLabel(card, text="Healthcare Management\nSystem", font=("Segoe UI", 22, "bold"), text_color=TEXT_MAIN, justify="center")
        title.pack(pady=(0, 5))

        subtitle = ctk.CTkLabel(card, text="Sign in to continue", font=("Segoe UI", 14), text_color=TEXT_SUB)
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

        password_label = ctk.CTkLabel(card, text="Password", font=("Segoe UI", 12, "bold"), text_color=TEXT_MAIN)
        password_label.pack(anchor="w", padx=45)

        self.password_entry = ctk.CTkEntry(
            card, placeholder_text="Enter password", show="*", 
            width=330, height=45, font=("Segoe UI", 14), 
            border_color=BORDER_COLOR, border_width=1, fg_color="#f8fafc", corner_radius=8
        )
        self.password_entry.pack(pady=(5, 30), padx=45)

        # Login button
        login_btn = ctk.CTkButton(
            card, text="Sign In", width=330, height=45, 
            font=("Segoe UI", 15, "bold"), fg_color=PRIMARY_COLOR, 
            hover_color="#1d4ed8", corner_radius=8, command=self.handle_login
        )
        login_btn.pack(pady=(0, 40))

    def handle_login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        
        if database.authenticate(email, password):
            self.show_dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid email or password.\n\nHint: Use admin@healthcare.com / admin123")

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
        
        title = ctk.CTkLabel(title_frame, text="🏥 Healthcare System", font=("Segoe UI", 18, "bold"), text_color=TEXT_MAIN)
        title.pack(side="left")

        # Menu Items
        self.menu_buttons = []
        menu_items = [
            ("Dashboard", "📊", self.page_dashboard),
            ("Patients", "👥", self.page_patients),
            ("Doctors", "⚕️", self.page_doctors),
            ("Appointments", "📅", self.page_appointments),
            ("Services", "🏥", self.page_services),
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
            text="   🚪   Logout",
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
        self.set_header("Dashboard", "Overview of your healthcare system")

        self.content_area.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # Stats Cards
        db_stats = database.get_dashboard_stats()
        stats = [
            ("Total Patients", db_stats["total_patients"], "👥", "+12%", "#16a34a", "#dcfce7", "#16a34a"),
            ("Active Doctors", db_stats["active_doctors"], "⚕️", "+3%", "#16a34a", "#e0f2fe", "#0284c7"),
            ("Appointments Today", db_stats["appointments_today"], "📅", "-5%", "#dc2626", "#ffedd5", "#ea580c"),
            ("Revenue", db_stats["revenue"], "📈", "+18%", "#16a34a", "#f3e8ff", "#9333ea")
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
        
        recent_title = ctk.CTkLabel(recent_frame, text="Recent Appointments", font=("Segoe UI", 16, "bold"), text_color=TEXT_MAIN)
        recent_title.pack(anchor="w", padx=25, pady=20)

        columns = ["Patient", "Doctor", "Time", "Status"]
        data = database.get_recent_appointments()

        self.create_custom_table(recent_frame, columns, data)

    # ======================
    # CUSTOM TABLE TEMPLATE
    # ======================
    def create_custom_table(self, parent, columns, data):
        # Create a single grid frame for perfect column alignment
        table_frame = ctk.CTkFrame(parent, fg_color="transparent")
        table_frame.pack(fill="both", expand=True, padx=20, pady=15)

        col_widths = [2, 2, 1, 1] if len(columns) == 4 else [1] * len(columns)
        
        for i, width in enumerate(col_widths):
            table_frame.grid_columnconfigure(i, weight=width, uniform="colGroup")
            
        # Header
        for i, col in enumerate(columns):
            lbl = ctk.CTkLabel(table_frame, text=col, font=("Segoe UI", 13, "bold"), text_color=TEXT_SUB, anchor="w")
            lbl.grid(row=0, column=i, sticky="w", padx=10, pady=(0, 10))

        # Header bottom border
        header_border = ctk.CTkFrame(table_frame, fg_color=BORDER_COLOR, height=1)
        header_border.grid(row=1, column=0, columnspan=len(columns), sticky="ew", pady=(0, 10))

        # Rows
        current_row = 2
        for r_idx, row in enumerate(data):
            for i, val in enumerate(row):
                if columns[i] == "Status":
                    status_colors = {
                        "Completed": ("#dcfce7", "#16a34a"),
                        "In Progress": ("#dbeafe", "#2563eb"),
                        "Scheduled": ("#f3e8ff", "#9333ea")
                    }
                    bg, fg = status_colors.get(val, ("#f1f5f9", TEXT_SUB))
                    
                    status_frame = ctk.CTkFrame(table_frame, fg_color=bg, corner_radius=10)
                    status_frame.grid(row=current_row, column=i, sticky="w", padx=10, pady=8)
                    
                    lbl = ctk.CTkLabel(status_frame, text=val, font=("Segoe UI", 12, "bold"), text_color=fg)
                    lbl.pack(padx=12, pady=3)
                else:
                    lbl = ctk.CTkLabel(table_frame, text=val, font=("Segoe UI", 14), text_color=TEXT_MAIN, anchor="w")
                    lbl.grid(row=current_row, column=i, sticky="w", padx=10, pady=12)
            
            current_row += 1
            
            # Row border
            if r_idx < len(data) - 1:
                border = ctk.CTkFrame(table_frame, fg_color="#f1f5f9", height=1)
                border.grid(row=current_row, column=0, columnspan=len(columns), sticky="ew")
                current_row += 1

    # ======================
    # OTHER PAGES
    # ======================
    def page_patients(self):
        self.clear_content()
        self.set_header("Patients", "Manage patient records and details")

        # Action Bar
        action_frame = ctk.CTkFrame(self.content_area, fg_color="transparent")
        action_frame.pack(fill="x", pady=(0, 15))
        
        # Search Entry
        self.search_var = tk.StringVar()
        search_entry = ctk.CTkEntry(
            action_frame, placeholder_text="Search by name...", width=250, 
            textvariable=self.search_var, border_color=BORDER_COLOR
        )
        search_entry.pack(side="left", padx=(0, 10))
        
        search_btn = ctk.CTkButton(
            action_frame, text="🔍 Search", font=("Segoe UI", 13, "bold"), width=100,
            command=self.refresh_patients_table
        )
        search_btn.pack(side="left")
        
        add_btn = ctk.CTkButton(
            action_frame, text="➕ Add Patient", font=("Segoe UI", 14, "bold"),
            fg_color=PRIMARY_COLOR, hover_color="#1d4ed8", corner_radius=8,
            command=self.show_add_patient_dialog
        )
        add_btn.pack(side="right")
        
        export_btn = ctk.CTkButton(
            action_frame, text="📥 Export CSV", font=("Segoe UI", 14, "bold"),
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
        columns = ["Name", "Age", "Gender", "Contact", "Last Visit"]
        data = database.get_patients(query)
        self.create_custom_table(self.patients_table_frame, columns, data)

    def export_patients_csv(self):
        data = database.get_patients() # Get all without filter or use self.search_var.get() if you want filtered export
        if not data:
            messagebox.showinfo("Export", "No data to export.")
            return
            
        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")],
            title="Export Patients Data",
            initialfile="patients_data.csv"
        )
        if filepath:
            try:
                with open(filepath, mode='w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(["Name", "Age", "Gender", "Contact", "Last Visit"])
                    writer.writerows(data)
                messagebox.showinfo("Success", "Data exported successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export data: {e}")

    def show_add_patient_dialog(self):
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Add New Patient")
        dialog.geometry("420x550")
        dialog.configure(fg_color=BG_COLOR)
        dialog.grab_set() # Chặn click vào cửa sổ chính
        dialog.focus()
        
        title = ctk.CTkLabel(dialog, text="Patient Information", font=("Segoe UI", 20, "bold"), text_color=TEXT_MAIN)
        title.pack(pady=(25, 15))
        
        # Form Inputs
        entries = {}
        fields = [
            ("Name", "e.g. Alex Johnson"), 
            ("Age", "e.g. 35"), 
            ("Gender", "e.g. Male / Female"), 
            ("Contact", "e.g. 555-0199"), 
            ("Last Visit", "e.g. 2026-04-20")
        ]
        
        for field, placeholder in fields:
            frame = ctk.CTkFrame(dialog, fg_color="transparent")
            frame.pack(fill="x", padx=40, pady=8)
            
            lbl = ctk.CTkLabel(frame, text=field, font=("Segoe UI", 13, "bold"), text_color=TEXT_MAIN, width=80, anchor="w")
            lbl.pack(side="left")
            
            ent = ctk.CTkEntry(frame, width=220, border_color=BORDER_COLOR, placeholder_text=placeholder)
            ent.pack(side="right", fill="x", expand=True)
            entries[field] = ent
            
        def save_patient():
            name = entries["Name"].get()
            age = entries["Age"].get()
            gender = entries["Gender"].get()
            contact = entries["Contact"].get()
            last_visit = entries["Last Visit"].get()
            
            if not name or not age:
                messagebox.showerror("Error", "Name and Age are required fields!", parent=dialog)
                return
                
            # Lưu vào CSDL
            database.add_patient(name, age, gender, contact, last_visit)
            dialog.destroy()
            
            # Tải lại trang để hiện dữ liệu mới
            messagebox.showinfo("Success", "Patient added successfully!")
            self.page_patients()
            
        save_btn = ctk.CTkButton(
            dialog, text="Save Patient", fg_color="#16a34a", hover_color="#15803d", 
            font=("Segoe UI", 15, "bold"), height=40, command=save_patient
        )
        save_btn.pack(pady=35)

    def page_doctors(self):
        self.clear_content()
        self.set_header("Doctors", "View and manage doctor directory")

        # Action Bar
        action_frame = ctk.CTkFrame(self.content_area, fg_color="transparent")
        action_frame.pack(fill="x", pady=(0, 15))
        
        del_btn = ctk.CTkButton(
            action_frame, text="🗑️ Delete Doctor", font=("Segoe UI", 14, "bold"),
            fg_color="#ef4444", hover_color="#dc2626", corner_radius=8,
            command=self.show_delete_doctor_dialog
        )
        del_btn.pack(side="right", padx=(10, 0))

        add_btn = ctk.CTkButton(
            action_frame, text="➕ Add Doctor", font=("Segoe UI", 14, "bold"),
            fg_color=PRIMARY_COLOR, hover_color="#1d4ed8", corner_radius=8,
            command=self.show_add_doctor_dialog
        )
        add_btn.pack(side="right")

        frame = ctk.CTkFrame(self.content_area, fg_color=SURFACE_COLOR, corner_radius=12, border_width=1, border_color=BORDER_COLOR)
        frame.pack(fill="both", expand=True)

        columns = ["Name", "Specialty", "Experience", "Contact", "Status"]
        data = database.get_doctors()
        self.create_custom_table(frame, columns, data)

    def show_add_doctor_dialog(self):
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Add New Doctor")
        dialog.geometry("420x550")
        dialog.configure(fg_color=BG_COLOR)
        dialog.grab_set()
        dialog.focus()
        
        title = ctk.CTkLabel(dialog, text="Doctor Information", font=("Segoe UI", 20, "bold"), text_color=TEXT_MAIN)
        title.pack(pady=(25, 15))
        
        entries = {}
        fields = [
            ("Name", "e.g. Dr. John Doe"), 
            ("Specialty", "e.g. Cardiology"), 
            ("Experience", "e.g. 10 years"), 
            ("Contact", "e.g. 555-0199"), 
            ("Status", ["Available", "On Leave"])
        ]
        
        for field, config in fields:
            frame = ctk.CTkFrame(dialog, fg_color="transparent")
            frame.pack(fill="x", padx=40, pady=8)
            
            lbl = ctk.CTkLabel(frame, text=field, font=("Segoe UI", 13, "bold"), text_color=TEXT_MAIN, width=80, anchor="w")
            lbl.pack(side="left")
            
            if field == "Status":
                ent = ctk.CTkOptionMenu(frame, values=config, width=220, fg_color="#f8fafc", text_color=TEXT_MAIN, button_color=PRIMARY_COLOR)
                ent.set("Available")
            else:
                ent = ctk.CTkEntry(frame, width=220, border_color=BORDER_COLOR, placeholder_text=config)
            ent.pack(side="right", fill="x", expand=True)
            entries[field] = ent
            
        def save_doctor():
            name = entries["Name"].get()
            specialty = entries["Specialty"].get()
            experience = entries["Experience"].get()
            contact = entries["Contact"].get()
            status = entries["Status"].get()
            
            if not name or not specialty:
                messagebox.showerror("Error", "Name and Specialty are required!", parent=dialog)
                return
                
            database.add_doctor(name, specialty, experience, contact, status)
            dialog.destroy()
            messagebox.showinfo("Success", "Doctor added successfully!")
            self.page_doctors()
            
        save_btn = ctk.CTkButton(dialog, text="Save Doctor", fg_color="#16a34a", hover_color="#15803d", font=("Segoe UI", 15, "bold"), height=40, command=save_doctor)
        save_btn.pack(pady=35)

    def show_delete_doctor_dialog(self):
        doctors = database.get_doctor_names()
        if not doctors:
            messagebox.showinfo("Info", "No doctors found to delete.")
            return

        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Delete Doctor")
        dialog.geometry("350x250")
        dialog.configure(fg_color=BG_COLOR)
        dialog.grab_set()
        
        title = ctk.CTkLabel(dialog, text="Select Doctor to Delete", font=("Segoe UI", 16, "bold"), text_color=TEXT_MAIN)
        title.pack(pady=20)
        
        combo = ctk.CTkOptionMenu(dialog, values=doctors, width=250)
        combo.pack(pady=10)
        
        def confirm_delete():
            selected = combo.get()
            if selected:
                database.delete_doctor(selected)
                dialog.destroy()
                messagebox.showinfo("Success", f"Doctor '{selected}' deleted.")
                self.page_doctors()
                
        btn = ctk.CTkButton(dialog, text="Confirm Delete", fg_color="#ef4444", hover_color="#dc2626", font=("Segoe UI", 14, "bold"), command=confirm_delete)
        btn.pack(pady=20)

    def page_appointments(self):
        self.clear_content()
        self.set_header("Appointments", "Schedule and track appointments")

        # Action Bar
        action_frame = ctk.CTkFrame(self.content_area, fg_color="transparent")
        action_frame.pack(fill="x", pady=(0, 15))

        add_btn = ctk.CTkButton(
            action_frame, text="📅 Book Appointment", font=("Segoe UI", 14, "bold"),
            fg_color=PRIMARY_COLOR, hover_color="#1d4ed8", corner_radius=8,
            command=self.show_book_appointment_dialog
        )
        add_btn.pack(side="right")

        frame = ctk.CTkFrame(self.content_area, fg_color=SURFACE_COLOR, corner_radius=12, border_width=1, border_color=BORDER_COLOR)
        frame.pack(fill="both", expand=True)

        columns = ["Patient", "Doctor", "Date", "Type", "Status"]
        data = database.get_appointments()
        self.create_custom_table(frame, columns, data)

    def show_book_appointment_dialog(self):
        patients = database.get_patient_names()
        doctors = database.get_doctor_names()
        
        if not patients or not doctors:
            messagebox.showwarning("Warning", "You need at least one patient and one doctor to book an appointment.")
            return

        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Book Appointment")
        dialog.geometry("420x550")
        dialog.configure(fg_color=BG_COLOR)
        dialog.grab_set()
        dialog.focus()
        
        title = ctk.CTkLabel(dialog, text="Appointment Details", font=("Segoe UI", 20, "bold"), text_color=TEXT_MAIN)
        title.pack(pady=(25, 15))
        
        entries = {}
        fields = [
            ("Patient", patients), 
            ("Doctor", doctors), 
            ("Date", "e.g. 2026-04-20"), 
            ("Time", "e.g. 09:00 AM"),
            ("Type", "e.g. Checkup"),
            ("Status", ["Scheduled", "In Progress", "Completed"])
        ]
        
        for field, config in fields:
            frame = ctk.CTkFrame(dialog, fg_color="transparent")
            frame.pack(fill="x", padx=40, pady=8)
            
            lbl = ctk.CTkLabel(frame, text=field, font=("Segoe UI", 13, "bold"), text_color=TEXT_MAIN, width=80, anchor="w")
            lbl.pack(side="left")
            
            if isinstance(config, list):
                ent = ctk.CTkOptionMenu(frame, values=config, width=220, fg_color="#f8fafc", text_color=TEXT_MAIN, button_color=PRIMARY_COLOR)
                ent.set(config[0])
            else:
                ent = ctk.CTkEntry(frame, width=220, border_color=BORDER_COLOR, placeholder_text=config)
            ent.pack(side="right", fill="x", expand=True)
            entries[field] = ent
            
        def save_appointment():
            patient = entries["Patient"].get()
            doctor = entries["Doctor"].get()
            date = entries["Date"].get()
            time = entries["Time"].get()
            app_type = entries["Type"].get()
            status = entries["Status"].get()
            
            if not date or not time:
                messagebox.showerror("Error", "Date and Time are required!", parent=dialog)
                return
                
            database.add_appointment(patient, doctor, date, time, app_type, status)
            dialog.destroy()
            messagebox.showinfo("Success", "Appointment booked successfully!")
            self.page_appointments()
            
        save_btn = ctk.CTkButton(dialog, text="Confirm Booking", fg_color="#16a34a", hover_color="#15803d", font=("Segoe UI", 15, "bold"), height=40, command=save_appointment)
        save_btn.pack(pady=30)

    def page_services(self):
        self.clear_content()
        self.set_header("Services", "Manage healthcare services and pricing")

        frame = ctk.CTkFrame(self.content_area, fg_color=SURFACE_COLOR, corner_radius=12, border_width=1, border_color=BORDER_COLOR)
        frame.pack(fill="both", expand=True)

        columns = ["Service", "Category", "Price", "Duration"]
        data = database.get_services()
        self.create_custom_table(frame, columns, data)

if __name__ == "__main__":
    root = ctk.CTk()
    app = HealthcareApp(root)
    root.mainloop()