import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from datetime import datetime, timedelta
from app.database import SessionLocal, engine, Base
from app.models import Student
from analysis.clean_data import clean_student_data

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CSV_DIR = os.path.join(BASE_DIR, 'csvdata')

# Create tables
Base.metadata.create_all(bind=engine)

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


