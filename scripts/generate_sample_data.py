import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from faker import Faker
import random
import pandas as pd
from datetime import datetime, timedelta
from app.database import SessionLocal, engine, Base
from app.models import Student

# Create tables
Base.metadata.create_all(bind=engine)

fake = Faker(['vi_VN'])  # Vietnamese locale

# Vietnamese hometown list
HOMETOWNS = [
    "Hà Nội", "Hồ Chí Minh", "Đà Nẵng", "Hải Phòng", "Cần Thơ",
    "Nghệ An", "Thanh Hóa", "Thái Bình", "Nam Định", "Hải Dương",
    "Quảng Ninh", "Bắc Ninh", "Bắc Giang", "Vĩnh Phúc", "Phú Thọ",
    "Hưng Yên", "Hà Nam", "Ninh Bình", "Thái Nguyên", "Lào Cai",
    "Yên Bái", "Tuyên Quang", "Hà Giang", "Cao Bằng", "Lạng Sơn",
    "Quảng Bình", "Quảng Trị", "Thừa Thiên Huế", "Quảng Nam", "Quảng Ngãi",
    "Bình Định", "Phú Yên", "Khánh Hòa", "Ninh Thuận", "Bình Thuận",
    "Kon Tum", "Gia Lai", "Đắk Lắk", "Đắk Nông", "Lâm Đồng",
    "Bình Phước", "Tây Ninh", "Bình Dương", "Đồng Nai", "Bà Rịa - Vũng Tàu",
    "Long An", "Tiền Giang", "Bến Tre", "Trà Vinh", "Vĩnh Long",
    "Đồng Tháp", "An Giang", "Kiên Giang", "Hậu Giang", "Sóc Trăng",
    "Bạc Liêu", "Cà Mau"
]

def generate_student_code(index):
    """Generate student code in format SV + year + sequential number"""
    current_year = datetime.now().year
    return f"SV{current_year}{str(index).zfill(4)}"

def generate_random_score():
    """Generate random score between 0 and 10, or None (missing data)"""
    if random.random() < 0.15:  # 15% chance of missing data
        return None
    return round(random.uniform(0, 10), 2)

def generate_students(count=100):
    """Generate sample student data"""
    students = []
    
    for i in range(1, count + 1):
        # Random chance of missing data for each field
        missing_first_name = random.random() < 0.05  # 5% missing
        missing_last_name = random.random() < 0.03   # 3% missing
        missing_email = random.random() < 0.10       # 10% missing
        missing_dob = random.random() < 0.08         # 8% missing
        missing_hometown = random.random() < 0.12    # 12% missing
        
        first_name = None if missing_first_name else fake.first_name()
        last_name = None if missing_last_name else fake.last_name()
        
        # Generate email based on name if available
        if missing_email or missing_first_name or missing_last_name:
            email = None
        else:
            email = f"{first_name.lower()}.{last_name.lower()}{random.randint(1, 999)}@student.edu.vn"
        
        # Generate date of birth (18-25 years old)
        if missing_dob:
            dob = None
        else:
            age = random.randint(18, 25)
            days_offset = random.randint(0, 365)
            dob = datetime.now() - timedelta(days=age*365 + days_offset)
        
        student = Student(
            student_code=generate_student_code(i),
            first_name=first_name,
            last_name=last_name,
            email=email,
            date_of_birth=dob.date() if dob else None,
            hometown=None if missing_hometown else random.choice(HOMETOWNS),
            math_score=generate_random_score(),
            literature_score=generate_random_score(),
            english_score=generate_random_score()
        )
        students.append(student)
    
    return students

def main():
    print("Generating 100 sample students...")
    
    db = SessionLocal()
    try:
        # Clear existing data
        db.query(Student).delete()
        db.commit()
        
        # Generate and insert students
        students = generate_students(100)
        db.bulk_save_objects(students)
        db.commit()
        
        print(f"Successfully generated {len(students)} students!")
        
        # Display some statistics using pandas
        student_data = []
        for student in db.query(Student).all():
            student_data.append({
                'student_code': student.student_code,
                'first_name': student.first_name,
                'last_name': student.last_name,
                'email': student.email,
                'date_of_birth': student.date_of_birth,
                'hometown': student.hometown,
                'math_score': student.math_score,
                'literature_score': student.literature_score,
                'english_score': student.english_score
            })
        
        df = pd.DataFrame(student_data)
        
        print("\n=== Data Statistics ===")
        print(f"Total students: {len(df)}")
        print(f"\nMissing data count:")
        print(df.isnull().sum())
        print(f"\nScore statistics:")
        print(df[['math_score', 'literature_score', 'english_score']].describe())
        print(f"\nFirst 10 students:")
        print(df.head(10).to_string())
        
        # Export to CSV
        df.to_csv('students_data.csv', index=False, encoding='utf-8-sig')
        print(f"\nData exported to students_data.csv")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()


