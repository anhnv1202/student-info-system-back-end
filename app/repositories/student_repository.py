"""
Student Repository
Lớp chịu trách nhiệm tương tác trực tiếp với database
Chứa các query và database operations
"""

from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models import Student
from app.schemas import StudentCreate, StudentUpdate
from typing import Optional, List


class StudentRepository:
    """
    Student Repository Class
    
    Repository pattern - chịu trách nhiệm tất cả các thao tác với database.
    Các method trong class này chỉ làm việc với database, không chứa business logic.
    
    Purpose:
        - Tách biệt logic truy vấn database khỏi business logic
        - Dễ dàng thay đổi database hoặc query mà không ảnh hưởng tầng trên
        - Dễ test (có thể mock repository)
    """
    
    def __init__(self, db: Session):
        """
        Initialize repository với database session
        
        Args:
            db: SQLAlchemy database session
        """
        self.db = db
    
    def get_by_id(self, student_id: int) -> Optional[Student]:
        """
        Lấy sinh viên theo ID
        
        Args:
            student_id: ID của sinh viên cần tìm
            
        Returns:
            Student object nếu tìm thấy, None nếu không tìm thấy
            
        Example:
            student = repository.get_by_id(1)
            if student:
                print(student.student_code)
        """
        return self.db.query(Student).filter(Student.id == student_id).first()
    
    def get_by_student_code(self, student_code: str) -> Optional[Student]:
        """
        Lấy sinh viên theo mã sinh viên
        
        Args:
            student_code: Mã sinh viên cần tìm
            
        Returns:
            Student object nếu tìm thấy, None nếu không tìm thấy
            
        Example:
            student = repository.get_by_student_code("SV20240001")
        """
        return self.db.query(Student).filter(Student.student_code == student_code).first()
    
    def get_all(
        self, 
        skip: int = 0, 
        limit: int = 100,
        search: Optional[str] = None
    ) -> List[Student]:
        """
        Lấy danh sách sinh viên với phân trang và tìm kiếm
        
        Args:
            skip: Số lượng record bỏ qua (dùng cho pagination)
            limit: Số lượng record tối đa trả về
            search: Từ khóa tìm kiếm (tìm trong code, tên, email, quê quán)
            
        Returns:
            List các Student objects
            
        Example:
            # Lấy 10 sinh viên đầu tiên
            students = repository.get_all(skip=0, limit=10)
            
            # Lấy sinh viên từ 11-20
            students = repository.get_all(skip=10, limit=10)
            
            # Tìm kiếm sinh viên có chứa "Nguyen"
            students = repository.get_all(search="Nguyen")
        """
        query = self.db.query(Student)
        
        # Nếu có search term, tìm kiếm trong nhiều trường
        if search:
            search_filter = or_(
                Student.student_code.contains(search),
                Student.first_name.contains(search),
                Student.last_name.contains(search),
                Student.email.contains(search),
                Student.hometown.contains(search)
            )
            query = query.filter(search_filter)
        
        return query.offset(skip).limit(limit).all()
    
    def count(self, search: Optional[str] = None) -> int:
        """
        Đếm tổng số sinh viên
        
        Args:
            search: Từ khóa tìm kiếm (nếu có)
            
        Returns:
            Số lượng sinh viên
            
        Example:
            total = repository.count()  # Đếm tất cả
            total = repository.count(search="Nguyen")  # Đếm sinh viên tìm được
        """
        query = self.db.query(Student)
        
        if search:
            search_filter = or_(
                Student.student_code.contains(search),
                Student.first_name.contains(search),
                Student.last_name.contains(search),
                Student.email.contains(search),
                Student.hometown.contains(search)
            )
            query = query.filter(search_filter)
        
        return query.count()
    
    def create(self, student_data: StudentCreate) -> Student:
        """
        Tạo sinh viên mới trong database
        
        Args:
            student_data: Dữ liệu sinh viên (StudentCreate schema)
            
        Returns:
            Student object vừa được tạo (có kèm ID)
            
        Example:
            from app.schemas import StudentCreate
            
            student_data = StudentCreate(
                student_code="SV20240001",
                first_name="Minh",
                last_name="Nguyen"
            )
            new_student = repository.create(student_data)
            print(new_student.id)  # ID tự động tạo
        """
        # Convert Pydantic model sang dict
        db_student = Student(**student_data.model_dump())
        
        # Thêm vào database
        self.db.add(db_student)
        self.db.commit()  # Lưu vào database
        self.db.refresh(db_student)  # Lấy data mới (bao gồm ID)
        
        return db_student
    
    def update(self, student_id: int, student_data: StudentUpdate) -> Optional[Student]:
        """
        Cập nhật thông tin sinh viên
        
        Args:
            student_id: ID sinh viên cần update
            student_data: Dữ liệu cần update (StudentUpdate schema)
            
        Returns:
            Student object sau khi update, None nếu không tìm thấy
            
        Example:
            from app.schemas import StudentUpdate
            
            update_data = StudentUpdate(math_score=9.5, english_score=8.0)
            updated_student = repository.update(1, update_data)
        """
        db_student = self.get_by_id(student_id)
        if db_student is None:
            return None
        
        # Chỉ update các trường được gửi lên (exclude_unset=True)
        update_data = student_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_student, field, value)
        
        self.db.commit()
        self.db.refresh(db_student)
        
        return db_student
    
    def delete(self, student_id: int) -> Optional[Student]:
        """
        Xóa sinh viên khỏi database
        
        Args:
            student_id: ID sinh viên cần xóa
            
        Returns:
            Student object đã bị xóa, None nếu không tìm thấy
            
        Example:
            deleted_student = repository.delete(1)
            if deleted_student:
                print(f"Đã xóa {deleted_student.student_code}")
        """
        db_student = self.get_by_id(student_id)
        if db_student is None:
            return None
        
        self.db.delete(db_student)
        self.db.commit()
        
        return db_student
    
    def bulk_create(self, students_data: List[StudentCreate]) -> int:
        """
        Tạo nhiều sinh viên cùng lúc (bulk insert)
        
        Args:
            students_data: List các StudentCreate schemas
            
        Returns:
            Số lượng sinh viên đã tạo
            
        Example:
            students = [
                StudentCreate(student_code="SV001", first_name="A"),
                StudentCreate(student_code="SV002", first_name="B"),
            ]
            count = repository.bulk_create(students)
            print(f"Đã tạo {count} sinh viên")
        """
        # Convert list Pydantic models sang list ORM models
        db_students = [Student(**student.model_dump()) for student in students_data]
        
        # Bulk insert
        self.db.bulk_save_objects(db_students)
        self.db.commit()
        
        return len(db_students)

