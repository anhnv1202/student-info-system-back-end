"""
Script to view SQLite database content
Xem noi dung database SQLite
"""

import sqlite3
import sys
from pathlib import Path

# Path to database file
DB_PATH = Path(__file__).parent / "students.db"

def view_database():
    """View all students in database"""
    
    # Check if database exists
    if not DB_PATH.exists():
        print("Database chua ton tai! Chay server hoac generate_sample_data.py truoc.")
        print(f"Path: {DB_PATH}")
        return
    
    # Connect to database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Get all students
        cursor.execute("SELECT * FROM students")
        rows = cursor.fetchall()
        
        # Get column names
        cursor.execute("PRAGMA table_info(students)")
        columns = [col[1] for col in cursor.fetchall()]
        
        print(f"\n{'='*80}")
        print(f"DATABASE: {DB_PATH.name}")
        print(f"{'='*80}\n")
        
        if not rows:
            print("Database RONG! Chua co sinh vien nao.")
            print("\nChay lenh sau de tao du lieu mau:")
            print("  python scripts/generate_sample_data.py")
            return
        
        print(f"Tong so sinh vien: {len(rows)}\n")
        
        # Print header
        header = " | ".join(f"{col:15}" for col in columns)
        print(header)
        print("-" * len(header))
        
        # Print rows
        for row in rows[:10]:  # Show first 10 rows
            row_str = " | ".join(f"{str(val)[:15]:15}" for val in row)
            print(row_str)
        
        if len(rows) > 10:
            print(f"\n... va {len(rows) - 10} sinh vien khac")
        
        # Statistics
        cursor.execute("""
            SELECT 
                COUNT(*) as total,
                COUNT(math_score) as has_math,
                COUNT(literature_score) as has_lit,
                COUNT(english_score) as has_eng,
                AVG(math_score) as avg_math,
                AVG(literature_score) as avg_lit,
                AVG(english_score) as avg_eng
            FROM students
        """)
        stats = cursor.fetchone()
        
        print(f"\n{'='*80}")
        print("THONG KE:")
        print(f"{'='*80}")
        print(f"Tong so sinh vien: {stats[0]}")
        print(f"Co diem Toan: {stats[1]} ({stats[1]/stats[0]*100:.1f}%)")
        print(f"Co diem Van: {stats[2]} ({stats[2]/stats[0]*100:.1f}%)")
        print(f"Co diem Anh: {stats[3]} ({stats[3]/stats[0]*100:.1f}%)")
        
        if stats[4]:
            print(f"\nDiem trung binh:")
            print(f"  Toan: {stats[4]:.2f}")
            print(f"  Van: {stats[5]:.2f}")
            print(f"  Anh: {stats[6]:.2f}")
        
        print(f"\n{'='*80}\n")
        
    except sqlite3.OperationalError as e:
        print(f"Loi: {e}")
        print("\nBang 'students' chua duoc tao. Chay server hoac generate_sample_data.py truoc.")
    
    finally:
        conn.close()

def search_student(keyword):
    """Search students by keyword"""
    
    if not DB_PATH.exists():
        print("Database chua ton tai!")
        return
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        query = """
            SELECT id, student_code, first_name, last_name, email, hometown
            FROM students
            WHERE student_code LIKE ? 
               OR first_name LIKE ?
               OR last_name LIKE ?
               OR email LIKE ?
               OR hometown LIKE ?
        """
        search_term = f"%{keyword}%"
        cursor.execute(query, (search_term, search_term, search_term, search_term, search_term))
        rows = cursor.fetchall()
        
        print(f"\nTim thay {len(rows)} sinh vien voi tu khoa '{keyword}':\n")
        
        for row in rows:
            print(f"ID: {row[0]}")
            print(f"  Ma SV: {row[1]}")
            print(f"  Ho ten: {row[3]} {row[2]}")
            print(f"  Email: {row[4]}")
            print(f"  Que quan: {row[5]}")
            print()
        
    finally:
        conn.close()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Search mode
        keyword = sys.argv[1]
        search_student(keyword)
    else:
        # View all mode
        view_database()

