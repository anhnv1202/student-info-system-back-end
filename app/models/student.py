"""
Student Model
Định nghĩa cấu trúc bảng students trong database
"""

from sqlalchemy import Column, Integer, String, Float, Date
from app.database import Base


class Student(Base):
    """
    Student ORM Model
    
    Đại diện cho bảng 'students' trong database.
    Mỗi instance của class này tương ứng với 1 row trong database.
    
    Attributes:
        id (int): Primary key, tự động tăng
        student_code (str): Mã sinh viên (unique, bắt buộc)
        first_name (str): Tên sinh viên (optional)
        last_name (str): Họ sinh viên (optional)
        email (str): Email sinh viên (optional)
        date_of_birth (date): Ngày sinh (optional)
        hometown (str): Quê quán (optional)
        math_score (float): Điểm Toán 0-10 (optional)
        literature_score (float): Điểm Văn 0-10 (optional)
        english_score (float): Điểm Anh 0-10 (optional)
    """
    
    __tablename__ = "students"

    # Primary key - ID tự động tăng
    id = Column(Integer, primary_key=True, index=True, comment="ID tự động tăng")
    
    # Mã sinh viên - bắt buộc và unique
    student_code = Column(
        String, 
        unique=True, 
        index=True, 
        nullable=False,
        comment="Mã sinh viên (unique)"
    )
    
    # Thông tin cá nhân - tất cả đều optional
    first_name = Column(String, nullable=True, comment="Tên sinh viên")
    last_name = Column(String, nullable=True, comment="Họ sinh viên")
    email = Column(String, nullable=True, comment="Email sinh viên")
    date_of_birth = Column(Date, nullable=True, comment="Ngày sinh")
    hometown = Column(String, nullable=True, comment="Quê quán")
    
    # Điểm số - tất cả đều optional
    math_score = Column(Float, nullable=True, comment="Điểm Toán (0-10)")
    literature_score = Column(Float, nullable=True, comment="Điểm Văn (0-10)")
    english_score = Column(Float, nullable=True, comment="Điểm Anh (0-10)")

    def __repr__(self):
        """String representation của Student object"""
        return f"<Student {self.student_code}: {self.last_name} {self.first_name}>"

