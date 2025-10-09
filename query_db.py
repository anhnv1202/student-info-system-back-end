"""
Interactive SQLite query tool
Chay cau lenh SQL truc tiep vao database
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "students.db"

def run_query(query):
    """Run a SQL query and display results"""
    
    if not DB_PATH.exists():
        print("Database chua ton tai!")
        return
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute(query)
        
        # If SELECT query, show results
        if query.strip().upper().startswith("SELECT"):
            rows = cursor.fetchall()
            
            # Get column names from cursor description
            if cursor.description:
                columns = [desc[0] for desc in cursor.description]
                
                # Print header
                header = " | ".join(f"{col:15}" for col in columns)
                print("\n" + header)
                print("-" * len(header))
                
                # Print rows
                for row in rows:
                    row_str = " | ".join(f"{str(val)[:15]:15}" for val in row)
                    print(row_str)
                
                print(f"\nTong so row: {len(rows)}\n")
        else:
            # For INSERT, UPDATE, DELETE
            conn.commit()
            print(f"Query executed. Rows affected: {cursor.rowcount}")
    
    except Exception as e:
        print(f"Loi: {e}")
    
    finally:
        conn.close()

if __name__ == "__main__":
    print("="*80)
    print("SQLite Query Tool")
    print("="*80)
    print(f"Database: {DB_PATH}")
    print("\nVi du cau lenh:")
    print("  SELECT * FROM students LIMIT 5;")
    print("  SELECT student_code, first_name, math_score FROM students WHERE math_score > 8;")
    print("  SELECT COUNT(*) FROM students;")
    print("\nGo 'exit' de thoat\n")
    
    while True:
        query = input("SQL> ").strip()
        
        if query.lower() in ['exit', 'quit', 'q']:
            print("Bye!")
            break
        
        if not query:
            continue
        
        run_query(query)

