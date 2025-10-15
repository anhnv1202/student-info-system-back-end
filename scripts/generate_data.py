from faker import Faker
import random
import pandas as pd
from datetime import datetime
import unicodedata
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CSV_DIR = os.path.join(BASE_DIR, 'csvdata')

fake = Faker(['vi_VN'])

HOMETOWNS = [
    "Hà Nội", "Hồ Chí Minh", "Đà Nẵng", "Cần Thơ", "Thanh Hóa",
    "Thái Bình", "Nam Định", "Quảng Ninh", "Thái Nguyên", "Lào Cai"
]

LASTNAME = ["Nguyễn", "Trần", "Lê", "Phạm", "Hoàng", "Huỳnh", "Phan", "Vũ", "Võ", "Đặng"]
MIDDLENAME = ["Văn", "Thị", "Hữu", "Đức", "Minh", "Ngọc", "Anh", "Gia", "Bảo", "Quốc"]
FIRSTNAME = ["Nam", "Linh", "Huy", "Trang", "Mai", "Tuấn", "Lan", "Phương", "Hà", "Long", "Ngân", "Nhung", "Hải", "Duy", "Cường"]

def normalize_diacritics_for_email(text):
    if not text:
        return None
    
    text = text.replace('đ', 'd').replace('Đ', 'D')
    normalized = unicodedata.normalize('NFD', text)
    return ''.join([c for c in normalized if unicodedata.category(c) != 'Mn'])

def generate_vn_name():
    """Generate realistic Vietnamese name and split it"""
    lastname = random.choice(LASTNAME)
    middlename = random.choice(MIDDLENAME)
    firstname = random.choice(FIRSTNAME)
    full = f"{lastname} {middlename} {firstname}"
    return full, lastname + " " + middlename, firstname

def random_dirty_score():
    """Generate clean + dirty scores"""
    p = random.random()
    if p < 0.05:
        return "NaN"
    elif p < 0.1:
        return -random.randint(1, 10)
    elif p < 0.15:
        return random.choice(["ten", "eight", "fail"])
    elif p < 0.25:
        return None
    else:
        return round(random.uniform(0, 10), 2)

def random_dirty_dob():
    """Generate dirty or inconsistent date_of_birth"""
    p = random.random()
    if p < 0.05:
        return "not a date"
    elif p < 0.1:
        return None
    else:
        year = random.randint(2000, 2007)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        formats = [
            f"{year}-{month:02d}-{day:02d}",
            f"{day}/{month}/{year}",
            f"{month}-{day}-{year}",
            f"{year}/{month}/{day}",
            f"{day}-{month}-{year}",
        ]
        return random.choice(formats)

def generate_students(count=100):
    students = []
    for i in range(1, count + 1):
        full, last_name, first_name = generate_vn_name() if random.random() > 0.05 else (None, None, None)
        if first_name and last_name:
            email_first = normalize_diacritics_for_email(first_name).lower()
            email_last = normalize_diacritics_for_email(f"{last_name}").lower().replace(" ", "")
            email_suffix = random.randint(1, 999)
            email = (
                f"{email_first}{email_last}{email_suffix}@edu.vn"
                if first_name and last_name and random.random() > 0.1
                else None
            )
        else:
            email = None

        hometown = random.choice(HOMETOWNS) if random.random() > 0.1 else None

        students.append({
            "student_code": f"SV2025{str(i).zfill(4)}",
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "date_of_birth": random_dirty_dob(),
            "hometown": hometown,
            "math_score": random_dirty_score(),
            "literature_score": random_dirty_score(),
            "english_score": random_dirty_score(),
        })
    return students

if __name__ == "__main__":
    sample_data = os.path.join(CSV_DIR, "sample_data.csv")
    df = pd.DataFrame(generate_students(100))
    df.to_csv(sample_data, index=False, encoding="utf-8-sig")
    print(f"Sample data has been generated and saved in the {CSV_DIR} folder")
