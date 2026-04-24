import sqlite3
import os

# Đường dẫn tới file database
# File này sẽ được tự động tạo trong thư mục "database" của project
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'healthcare.db')

def get_connection():
    """Tạo kết nối tới database SQLite"""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return sqlite3.connect(DB_PATH)

def initialize_database():
    """Khởi tạo các bảng và dữ liệu mẫu nếu chưa có"""
    conn = get_connection()
    cursor = conn.cursor()

    # 1. Bảng Users (Quản trị viên/Bác sĩ đăng nhập)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # 2. Bảng Patients (Bệnh nhân)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age TEXT,
            gender TEXT,
            contact TEXT,
            last_visit TEXT
        )
    ''')

    # 3. Bảng Doctors (Bác sĩ)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS doctors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            specialty TEXT,
            experience TEXT,
            contact TEXT,
            status TEXT
        )
    ''')

    # 4. Bảng Appointments (Lịch hẹn)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT,
            doctor_name TEXT,
            date TEXT,
            time TEXT,
            type TEXT,
            status TEXT
        )
    ''')

    # 5. Bảng Services (Dịch vụ)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS services (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            category TEXT,
            price TEXT,
            duration TEXT
        )
    ''')

    # Thêm dữ liệu mẫu (Dummy Data) nếu bảng rỗng
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        # Tài khoản mặc định
        cursor.execute("INSERT INTO users (email, password) VALUES ('admin@healthcare.com', 'admin123')")
        
        # Bệnh nhân mẫu
        patients = [
            ("John Smith", "45", "Male", "555-0101", "2026-04-10"),
            ("Emma Johnson", "32", "Female", "555-0102", "2026-04-11"),
            ("Robert Brown", "58", "Male", "555-0103", "2026-04-13"),
            ("Sarah Williams", "29", "Female", "555-0104", "2026-04-14"),
            ("Michael Davis", "62", "Male", "555-0105", "2026-04-15"),
        ]
        cursor.executemany("INSERT INTO patients (name, age, gender, contact, last_visit) VALUES (?, ?, ?, ?, ?)", patients)

        # Bác sĩ mẫu
        doctors = [
            ("Dr. Sarah Wilson", "Cardiology", "12 years", "555-1001", "Available"),
            ("Dr. Michael Chen", "Pediatrics", "8 years", "555-1002", "Available"),
            ("Dr. James Lee", "Orthopedics", "15 years", "555-1003", "On Leave"),
            ("Dr. Emily Davis", "Neurology", "10 years", "555-1004", "Available"),
        ]
        cursor.executemany("INSERT INTO doctors (name, specialty, experience, contact, status) VALUES (?, ?, ?, ?, ?)", doctors)

        # Lịch hẹn mẫu
        appointments = [
            ("John Smith", "Dr. Sarah Wilson", "2026-04-13", "09:00 AM", "Checkup", "Completed"),
            ("Emma Johnson", "Dr. Michael Chen", "2026-04-13", "10:30 AM", "Follow-up", "Completed"),
            ("Robert Brown", "Dr. Sarah Wilson", "2026-04-14", "02:00 PM", "Consultation", "In Progress"),
            ("Lisa Anderson", "Dr. James Lee", "2026-04-15", "03:30 PM", "Checkup", "Scheduled"),
            ("David Martinez", "Dr. Emily Davis", "2026-04-15", "04:00 PM", "Checkup", "Scheduled"),
        ]
        cursor.executemany("INSERT INTO appointments (patient_name, doctor_name, date, time, type, status) VALUES (?, ?, ?, ?, ?, ?)", appointments)

        # Dịch vụ mẫu
        services = [
            ("General Checkup", "Basic", "$50", "30 mins"),
            ("Blood Test", "Lab", "$30", "15 mins"),
            ("MRI Scan", "Imaging", "$250", "60 mins"),
            ("X-Ray", "Imaging", "$100", "20 mins"),
            ("Physical Therapy", "Therapy", "$80", "45 mins"),
        ]
        cursor.executemany("INSERT INTO services (name, category, price, duration) VALUES (?, ?, ?, ?)", services)

    conn.commit()
    conn.close()

# ==========================================
# CÁC HÀM TRUY VẤN CHO GIAO DIỆN (UI)
# ==========================================

def authenticate(email, password):
    """Kiểm tra đăng nhập"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
    user = cursor.fetchone()
    conn.close()
    return user is not None

def get_patients(search_query=""):
    conn = get_connection()
    cursor = conn.cursor()
    if search_query:
        cursor.execute("SELECT name, age, gender, contact, last_visit FROM patients WHERE name LIKE ? COLLATE NOCASE", ('%' + search_query + '%',))
    else:
        cursor.execute("SELECT name, age, gender, contact, last_visit FROM patients")
    data = cursor.fetchall()
    conn.close()
    return data

def add_patient(name, age, gender, contact, last_visit):
    """Thêm một bệnh nhân mới vào database"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO patients (name, age, gender, contact, last_visit) 
        VALUES (?, ?, ?, ?, ?)
    ''', (name, age, gender, contact, last_visit))
    conn.commit()
    conn.close()


def get_doctors():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, specialty, experience, contact, status FROM doctors")
    data = cursor.fetchall()
    conn.close()
    return data

def add_doctor(name, specialty, experience, contact, status):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO doctors (name, specialty, experience, contact, status) 
        VALUES (?, ?, ?, ?, ?)
    ''', (name, specialty, experience, contact, status))
    conn.commit()
    conn.close()

def delete_doctor(name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM doctors WHERE name = ?", (name,))
    conn.commit()
    conn.close()

def get_doctor_names():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM doctors")
    data = [row[0] for row in cursor.fetchall()]
    conn.close()
    return data

def get_patient_names():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM patients")
    data = [row[0] for row in cursor.fetchall()]
    conn.close()
    return data

def get_appointments():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT patient_name, doctor_name, date, type, status FROM appointments")
    data = cursor.fetchall()
    conn.close()
    return data

def add_appointment(patient_name, doctor_name, date, time, app_type, status):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO appointments (patient_name, doctor_name, date, time, type, status) 
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (patient_name, doctor_name, date, time, app_type, status))
    conn.commit()
    conn.close()

def get_recent_appointments():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT patient_name, doctor_name, time, status FROM appointments LIMIT 5")
    data = cursor.fetchall()
    conn.close()
    return data

def get_services():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, category, price, duration FROM services")
    data = cursor.fetchall()
    conn.close()
    return data

def get_dashboard_stats():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM patients")
    total_patients = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM doctors WHERE status='Available'")
    active_doctors = cursor.fetchone()[0]
    
    # Đếm lịch hẹn ngày hôm nay (giả định dùng ngày 2026-04-15 hoặc đếm tổng tùy ý)
    cursor.execute("SELECT COUNT(*) FROM appointments WHERE status='Scheduled'")
    scheduled_appointments = cursor.fetchone()[0]
    
    conn.close()
    
    return {
        "total_patients": f"{total_patients:,}",
        "active_doctors": str(active_doctors),
        "appointments_today": str(scheduled_appointments),
        "revenue": "$45,231" # Có thể tính tổng thực tế sau này
    }
