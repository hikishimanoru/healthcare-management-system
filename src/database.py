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
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'patient'
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

    # 6. Bảng Medical Records (Hồ sơ Bệnh án)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS medical_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT,
            doctor_name TEXT,
            date TEXT,
            diagnosis TEXT,
            prescription TEXT
        )
    ''')

    # Thêm dữ liệu mẫu (Dummy Data) nếu bảng rỗng
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        # Tài khoản mặc định cho các role
        users_data = [
            ('admin@healthcare.com', 'admin123', 'admin'),
            ('doctor@healthcare.com', 'doctor123', 'doctor'),
            ('patient@healthcare.com', 'patient123', 'patient')
        ]
        cursor.executemany("INSERT INTO users (email, password, role) VALUES (?, ?, ?)", users_data)
        
        # Bệnh nhân mẫu
        patients = [
            ("Nguyễn Văn An", "45", "Nam", "0901234567", "2026-04-10"),
            ("Trần Thị Bình", "32", "Nữ", "0912345678", "2026-04-11"),
            ("Lê Hoàng Châu", "58", "Nam", "0923456789", "2026-04-13"),
            ("Phạm Minh Đức", "29", "Nam", "0934567890", "2026-04-14"),
            ("Hoàng Thị Én", "62", "Nữ", "0945678901", "2026-04-15"),
            ("Vũ Đức Phúc", "41", "Nam", "0981234567", "2026-04-16"),
            ("Đặng Thu Hà", "27", "Nữ", "0972345678", "2026-04-17"),
            ("Bùi Anh Tuấn", "50", "Nam", "0963456789", "2026-04-18"),
            ("Đỗ Mỹ Linh", "34", "Nữ", "0954567890", "2026-04-19"),
            ("Hồ Quang Hiếu", "48", "Nam", "0945678901", "2026-04-20"),
            ("Ngô Kiến Huy", "39", "Nam", "0936789012", "2026-04-21"),
            ("Dương Tú Anh", "25", "Nữ", "0927890123", "2026-04-22"),
            ("Lý Nhã Kỳ", "44", "Nữ", "0918901234", "2026-04-23"),
            ("Mai Phương Thúy", "36", "Nữ", "0909012345", "2026-04-24"),
            ("Đoàn Văn Hậu", "28", "Nam", "0890123456", "2026-04-25"),
            ("Trịnh Kim Chi", "55", "Nữ", "0881234567", "2026-04-26"),
            ("Tạ Quang Bửu", "70", "Nam", "0872345678", "2026-04-27"),
            ("Lâm Tâm Như", "42", "Nữ", "0863456789", "2026-04-28"),
            ("Đinh Ngọc Diệp", "33", "Nữ", "0854567890", "2026-04-29"),
            ("Trương Nam Thành", "31", "Nam", "0845678901", "2026-04-30")
        ]
        cursor.executemany("INSERT INTO patients (name, age, gender, contact, last_visit) VALUES (?, ?, ?, ?, ?)", patients)

        # Bác sĩ mẫu
        doctors = [
            ("BS. Trần Thanh Tâm", "Tim mạch", "12 năm", "0988111222", "Sẵn sàng"),
            ("BS. Nguyễn Văn Bảo", "Nhi khoa", "8 năm", "0977111333", "Sẵn sàng"),
            ("BS. Lê Hoàng Yến", "Chỉnh hình", "15 năm", "0966111444", "Nghỉ phép"),
            ("BS. Phạm Gia Khiêm", "Thần kinh", "10 năm", "0955111555", "Sẵn sàng"),
        ]
        cursor.executemany("INSERT INTO doctors (name, specialty, experience, contact, status) VALUES (?, ?, ?, ?, ?)", doctors)

        # Lịch hẹn mẫu
        appointments = [
            ("Nguyễn Văn An", "BS. Trần Thanh Tâm", "2026-04-13", "09:00 AM", "Khám định kỳ", "Hoàn thành"),
            ("Trần Thị Bình", "BS. Nguyễn Văn Bảo", "2026-04-13", "10:30 AM", "Tái khám", "Hoàn thành"),
            ("Lê Hoàng Châu", "BS. Trần Thanh Tâm", "2026-04-14", "02:00 PM", "Tư vấn", "Đang tiến hành"),
            ("Phạm Minh Đức", "BS. Lê Hoàng Yến", "2026-04-15", "03:30 PM", "Khám định kỳ", "Đã lên lịch"),
            ("Hoàng Thị Én", "BS. Phạm Gia Khiêm", "2026-04-15", "04:00 PM", "Khám định kỳ", "Đã lên lịch"),
        ]
        cursor.executemany("INSERT INTO appointments (patient_name, doctor_name, date, time, type, status) VALUES (?, ?, ?, ?, ?, ?)", appointments)

        # Dịch vụ mẫu
        services = [
            ("Khám tổng quát", "Cơ bản", "500,000đ", "30 phút"),
            ("Xét nghiệm máu", "Xét nghiệm", "300,000đ", "15 phút"),
            ("Chụp MRI", "Hình ảnh", "2,500,000đ", "60 phút"),
            ("Chụp X-Quang", "Hình ảnh", "1,000,000đ", "20 phút"),
            ("Vật lý trị liệu", "Điều trị", "800,000đ", "45 phút"),
        ]
        cursor.executemany("INSERT INTO services (name, category, price, duration) VALUES (?, ?, ?, ?)", services)

        # Hồ sơ Bệnh án mẫu (Dành cho các ca đã Hoàn thành)
        records = [
            ("Nguyễn Văn An", "BS. Trần Thanh Tâm", "2026-04-13", "Cao huyết áp nhẹ", "Amlodipine 5mg, Uống 1 viên/ngày"),
            ("Trần Thị Bình", "BS. Nguyễn Văn Bảo", "2026-04-13", "Viêm họng hạt", "Amoxicillin 500mg, Uống 2 viên/ngày"),
            ("Lê Hoàng Châu", "BS. Trần Thanh Tâm", "2026-04-14", "Rối loạn nhịp tim", "Concor 2.5mg, Uống 1 viên/sáng"),
            ("Phạm Minh Đức", "BS. Lê Hoàng Yến", "2026-04-14", "Thoái hóa đốt sống cổ", "Meloxicam 7.5mg, Nghỉ ngơi"),
            ("Hoàng Thị Én", "BS. Phạm Gia Khiêm", "2026-04-15", "Đau đầu vận mạch", "Paracetamol 500mg, Ngủ đủ giấc"),
            ("Vũ Đức Phúc", "BS. Nguyễn Văn Bảo", "2026-04-15", "Viêm mũi dị ứng", "Loratadine 10mg, Xịt mũi"),
            ("Đặng Thu Hà", "BS. Lê Hoàng Yến", "2026-04-16", "Trật khớp cổ chân", "Chườm đá, Băng gạc cố định"),
            ("Bùi Anh Tuấn", "BS. Phạm Gia Khiêm", "2026-04-16", "Rối loạn lo âu", "Diazepam 5mg, Trị liệu tâm lý"),
            ("Đỗ Mỹ Linh", "BS. Trần Thanh Tâm", "2026-04-17", "Thiếu máu cơ tim", "Aspirin 81mg, Hạn chế vận động mạnh"),
            ("Hồ Quang Hiếu", "BS. Nguyễn Văn Bảo", "2026-04-17", "Cảm cúm siêu vi", "Vitamin C, Oresol, Nghỉ ngơi 3 ngày"),
            ("Ngô Kiến Huy", "BS. Lê Hoàng Yến", "2026-04-18", "Viêm gân gót chân", "Ibuprofen 400mg, Vật lý trị liệu"),
            ("Dương Tú Anh", "BS. Phạm Gia Khiêm", "2026-04-18", "Chóng mặt tư thế", "Betahistine 16mg, Tránh thay đổi tư thế đột ngột"),
            ("Trịnh Thăng Bình", "BS. Trần Thanh Tâm", "2026-04-19", "Suy tĩnh mạch chi dưới", "Daflon 500mg, Mang vớ tĩnh mạch"),
            ("Phan Đình Tùng", "BS. Nguyễn Văn Bảo", "2026-04-19", "Viêm phế quản cấp", "Azithromycin 500mg, Siro ho"),
            ("Khởi My", "BS. Lê Hoàng Yến", "2026-04-20", "Gãy xương quai xanh", "Cố định xương, Canxi D3, Tái khám sau 2 tuần"),
            ("Đông Nhi", "BS. Phạm Gia Khiêm", "2026-04-20", "Suy nhược thần kinh", "Ginkgo Biloba 120mg, Magne B6"),
            ("Ông Cao Thắng", "BS. Trần Thanh Tâm", "2026-04-21", "Mỡ máu cao", "Atorvastatin 20mg, Tập thể dục, Ăn kiêng"),
            ("Bảo Thy", "BS. Nguyễn Văn Bảo", "2026-04-21", "Sốt xuất huyết Dengue", "Hạ sốt, Truyền dịch, Theo dõi tại bệnh viện"),
            ("Minh Hằng", "BS. Lê Hoàng Yến", "2026-04-22", "Giãn dây chằng gối", "Đeo nẹp, Glucosamine, Nghỉ ngơi"),
            ("Chi Pu", "BS. Phạm Gia Khiêm", "2026-04-22", "Động kinh vắng ý thức", "Valproate 500mg, Tránh lái xe, Không thức khuya"),
        ]
        cursor.executemany("INSERT INTO medical_records (patient_name, doctor_name, date, diagnosis, prescription) VALUES (?, ?, ?, ?, ?)", records)

    conn.commit()
    conn.close()

# ==========================================
# CÁC HÀM TRUY VẤN CHO GIAO DIỆN (UI)
# ==========================================

def authenticate(email, password):
    """Kiểm tra đăng nhập và trả về role"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT role FROM users WHERE email = ? AND password = ?", (email, password))
    user = cursor.fetchone()
    conn.close()
    if user:
        return user[0] # Trả về role ('admin', 'doctor', 'patient')
    return None

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

def get_doctor_names(only_available=False):
    conn = get_connection()
    cursor = conn.cursor()
    if only_available:
        cursor.execute("SELECT name FROM doctors WHERE status='Sẵn sàng'")
    else:
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
    cursor.execute("SELECT patient_name, doctor_name, date, time, type, status FROM appointments")
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

def get_appointment_options():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, patient_name, doctor_name, date, time FROM appointments")
    data = [f"[{row[0]}] {row[1]} gặp {row[2]} ({row[3]} {row[4]})" for row in cursor.fetchall()]
    conn.close()
    return data

def delete_appointment(app_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM appointments WHERE id = ?", (app_id,))
    conn.commit()
    conn.close()

def update_appointment_status(app_id, status):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE appointments SET status = ? WHERE id = ?", (status, app_id))
    conn.commit()
    conn.close()

def check_appointment_conflict(doctor_name, date, time):
    """Kiểm tra trùng lịch: Trả về True nếu bác sĩ đã có lịch khám vào giờ này"""
    conn = get_connection()
    cursor = conn.cursor()
    # Chỉ kiểm tra các lịch hẹn chưa hoàn thành/hủy
    cursor.execute('''
        SELECT COUNT(*) FROM appointments 
        WHERE doctor_name = ? AND date = ? AND time = ? AND status != 'Completed'
    ''', (doctor_name, date, time))
    count = cursor.fetchone()[0]
    conn.close()
    return count > 0

def get_recent_appointments():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT patient_name, doctor_name, time, status FROM appointments ORDER BY id DESC LIMIT 5")
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

def add_service(name, category, price, duration):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO services (name, category, price, duration) VALUES (?, ?, ?, ?)", (name, category, price, duration))
    conn.commit()
    conn.close()

def get_service_names():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM services")
    data = [row[0] for row in cursor.fetchall()]
    conn.close()
    return data

def delete_service(name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM services WHERE name = ?", (name,))
    conn.commit()
    conn.close()

def get_dashboard_stats():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM patients")
    total_patients = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM doctors WHERE status='Sẵn sàng'")
    active_doctors = cursor.fetchone()[0]
    
    # Đếm lịch hẹn ngày hôm nay (giả định dùng ngày 2026-04-15 hoặc đếm tổng tùy ý)
    cursor.execute("SELECT COUNT(*) FROM appointments WHERE date = date('now')")
    scheduled_appointments = cursor.fetchone()[0]
    
    conn.close()
    
    return {
        "total_patients": f"{total_patients:,}",
        "active_doctors": str(active_doctors),
        "appointments_today": str(scheduled_appointments),
        "revenue": "45,231,000đ" # Có thể tính tổng thực tế sau này
    }

def get_medical_records(search_query=""):
    conn = get_connection()
    cursor = conn.cursor()
    if search_query:
        cursor.execute("SELECT patient_name, doctor_name, date, diagnosis, prescription FROM medical_records WHERE patient_name LIKE ?", ('%' + search_query + '%',))
    else:
        cursor.execute("SELECT patient_name, doctor_name, date, diagnosis, prescription FROM medical_records")
    data = cursor.fetchall()
    conn.close()
    return data

def add_medical_record(patient_name, doctor_name, date, diagnosis, prescription):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO medical_records (patient_name, doctor_name, date, diagnosis, prescription) 
        VALUES (?, ?, ?, ?, ?)
    ''', (patient_name, doctor_name, date, diagnosis, prescription))
    conn.commit()
    conn.close()
