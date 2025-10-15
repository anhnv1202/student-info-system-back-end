import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from faker import Faker
import pandas as pd
from datetime import datetime, timedelta
from app.database import SessionLocal, engine, Base
from app.models import Student
from analysis.clean_data import clean_student_data

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CSV_DIR = os.path.join(BASE_DIR, 'csvdata')

# Create tables
Base.metadata.create_all(bind=engine)

# fake = Faker(['vi_VN'])  # Vietnamese locale

# # Vietnamese hometown list
# HOMETOWNS = [
#     "Hà Nội", "Hồ Chí Minh", "Đà Nẵng", "Cần Thơ", "Thanh Hóa",
#     "Thái Bình", "Nam Định", "Quảng Ninh", "Thái Nguyên", "Lào Cai"
# ]

# def generate_student_code(index):
#     """Generate student code in format SV + year + sequential number"""
#     current_year = datetime.now().year
#     return f"SV{current_year}{str(index).zfill(4)}"

# def generate_random_score():
#     """Generate random score between 0 and 10, or None (missing data)"""
#     if random.random() < 0.15:  # 15% chance of missing data
#         return None
#     return round(random.uniform(0, 10), 2)

# def generate_students(count=100):
#     """Generate sample student data"""
#     students = []
    
#     for i in range(1, count + 1):
#         # Random chance of missing data for each field
#         missing_first_name = random.random() < 0.05  # 5% missing
#         missing_last_name = random.random() < 0.03   # 3% missing
#         missing_email = random.random() < 0.10       # 10% missing
#         missing_dob = random.random() < 0.08         # 8% missing
#         missing_hometown = random.random() < 0.12    # 12% missing
        
#         first_name = None if missing_first_name else fake.first_name()
#         last_name = None if missing_last_name else fake.last_name()
        
#         # Generate email based on name if available
#         if missing_email or missing_first_name or missing_last_name:
#             email = None
#         else:
#             email = f"{first_name.lower()}.{last_name.lower()}{random.randint(1, 999)}@student.edu.vn"
        
#         # Generate date of birth (18-25 years old)
#         if missing_dob:
#             dob = None
#         else:
#             age = random.randint(18, 25)
#             days_offset = random.randint(0, 365)
#             dob = datetime.now() - timedelta(days=age*365 + days_offset)
        
#         student = Student(
#             student_code=generate_student_code(i),
#             first_name=first_name,
#             last_name=last_name,
#             email=email,
#             date_of_birth=dob.date() if dob else None,
#             hometown=None if missing_hometown else random.choice(HOMETOWNS),
#             math_score=generate_random_score(),
#             literature_score=generate_random_score(),
#             english_score=generate_random_score()
#         )
#         students.append(student)
    
#     return students

def insert_cleaned_data_to_db(cleaned_csv_path):
    df = pd.read_csv(cleaned_csv_path)
    students = []
    for _, row in df.iterrows():
        try:
            date_of_birth = datetime.strptime(str(row['date_of_birth']), "%Y-%m-%d").date()
        except Exception:
            date_of_birth = None

        # Split fullname 
        full_name = str(row.get('full_name', '')).strip()
        parts = full_name.split(' ')
        first_name = parts[-1] if len(parts) > 0 else None
        last_name = ' '.join(parts[:-1]) if len(parts) > 1 else None

        student = Student(
            student_code=row.get('student_code'),
            first_name=first_name,
            last_name=last_name,
            email=row.get('email'),
            date_of_birth=date_of_birth,
            hometown=row.get('hometown'),
            math_score=row.get('math_score'),
            literature_score=row.get('literature_score'),
            english_score=row.get('english_score')
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
        input_path = os.path.join(CSV_DIR, "sample_data.csv")
        output_path = os.path.join(CSV_DIR, "cleaned_data.csv")
        clean_student_data(input_path, output_path)
        students = insert_cleaned_data_to_db(output_path)
        print("\n\n\n students after cleaning : \n\n\n")
        print(students)
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
        csv_to_export = os.path.join(CSV_DIR, "students_data.csv")
        df.to_csv(csv_to_export, index=False, encoding='utf-8-sig')
        print(f"\nData exported to students_data.csv")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()


