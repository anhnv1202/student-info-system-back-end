"""
Student Service
Lớp chứa business logic của ứng dụng
Xử lý validation, business rules, và gọi repository
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories import StudentRepository
from app.schemas import StudentCreate, StudentUpdate, StudentResponse, StudentListResponse
from typing import Optional, List


class StudentService:
    """
    Student Service Class
    
    Service pattern - chứa business logic của ứng dụng.
    Nằm giữa Controller và Repository.
    
    Responsibilities:
        - Business logic và validation
        - Xử lý các rule phức tạp
        - Gọi repository để thao tác với database
        - Xử lý exceptions và error handling
        
    Purpose:
        - Tách business logic khỏi controller (controller chỉ lo HTTP)
        - Tách business logic khỏi repository (repository chỉ lo database)
        - Code dễ test và maintain hơn
    """
    
    def __init__(self, db: Session):
        """
        Initialize service với database session
        
        Args:
            db: SQLAlchemy database session
        """
        self.repository = StudentRepository(db)
    
    def get_student_by_id(self, student_id: int) -> StudentResponse:
        """
        Lấy thông tin sinh viên theo ID
        
        Args:
            student_id: ID của sinh viên
            
        Returns:
            StudentResponse schema
            
        Raises:
            HTTPException 404: Nếu không tìm thấy sinh viên
            
        Example:
            student = service.get_student_by_id(1)
            print(student.student_code)
        """
        student = self.repository.get_by_id(student_id)
        if not student:
            raise HTTPException(
                status_code=404, 
                detail=f"Không tìm thấy sinh viên với ID {student_id}"
            )
        return StudentResponse.model_validate(student)
    
    def get_all_students(
        self, 
        skip: int = 0, 
        limit: int = 100,
        search: Optional[str] = None
    ) -> StudentListResponse:
        """
        Lấy danh sách tất cả sinh viên (có phân trang và tìm kiếm)
        
        Args:
            skip: Số record bỏ qua (pagination)
            limit: Số record tối đa trả về
            search: Từ khóa tìm kiếm
            
        Returns:
            StudentListResponse chứa total và danh sách students
            
        Example:
            # Lấy 10 sinh viên đầu tiên
            result = service.get_all_students(skip=0, limit=10)
            print(f"Total: {result.total}")
            for student in result.students:
                print(student.student_code)
                
            # Tìm kiếm
            result = service.get_all_students(search="Nguyen")
        """
        students = self.repository.get_all(skip=skip, limit=limit, search=search)
        total = self.repository.count(search=search)
        
        return StudentListResponse(
            total=total,
            students=[StudentResponse.model_validate(s) for s in students]
        )
    
    def create_student(self, student_data: StudentCreate) -> StudentResponse:
        """
        Tạo sinh viên mới
        
        Business rules:
            - Mã sinh viên phải unique (không trùng)
            
        Args:
            student_data: Dữ liệu sinh viên cần tạo
            
        Returns:
            StudentResponse của sinh viên vừa tạo
            
        Raises:
            HTTPException 400: Nếu mã sinh viên đã tồn tại
            
        Example:
            new_student_data = StudentCreate(
                student_code="SV20240001",
                first_name="Minh",
                last_name="Nguyen",
                math_score=8.5
            )
            created = service.create_student(new_student_data)
            print(created.id)
        """
        # Business rule: Check mã sinh viên đã tồn tại chưa
        existing = self.repository.get_by_student_code(student_data.student_code)
        if existing:
            raise HTTPException(
                status_code=400,
                detail=f"Mã sinh viên {student_data.student_code} đã tồn tại"
            )
        
        # Tạo sinh viên mới
        student = self.repository.create(student_data)
        return StudentResponse.model_validate(student)
    
    def update_student(
        self, 
        student_id: int, 
        student_data: StudentUpdate
    ) -> StudentResponse:
        """
        Cập nhật thông tin sinh viên
        
        Business rules:
            - Sinh viên phải tồn tại
            - Nếu đổi mã sinh viên, mã mới không được trùng với sinh viên khác
            
        Args:
            student_id: ID sinh viên cần update
            student_data: Dữ liệu cần update
            
        Returns:
            StudentResponse sau khi update
            
        Raises:
            HTTPException 404: Nếu không tìm thấy sinh viên
            HTTPException 400: Nếu mã sinh viên mới bị trùng
            
        Example:
            update_data = StudentUpdate(
                math_score=9.5,
                english_score=8.0
            )
            updated = service.update_student(1, update_data)
        """
        # Check sinh viên có tồn tại không
        existing_student = self.repository.get_by_id(student_id)
        if not existing_student:
            raise HTTPException(
                status_code=404,
                detail=f"Không tìm thấy sinh viên với ID {student_id}"
            )
        
        # Business rule: Nếu đổi student_code, check trùng
        if student_data.student_code:
            duplicate = self.repository.get_by_student_code(student_data.student_code)
            if duplicate and duplicate.id != student_id:
                raise HTTPException(
                    status_code=400,
                    detail=f"Mã sinh viên {student_data.student_code} đã tồn tại"
                )
        
        # Update
        updated_student = self.repository.update(student_id, student_data)
        return StudentResponse.model_validate(updated_student)
    
    def delete_student(self, student_id: int) -> str:
        """
        Xóa sinh viên
        
        Args:
            student_id: ID sinh viên cần xóa
            
        Returns:
            Thông báo xóa thành công
            
        Raises:
            HTTPException 404: Nếu không tìm thấy sinh viên
            
        Example:
            message = service.delete_student(1)
            print(message)  # "Đã xóa sinh viên SV20240001"
        """
        student = self.repository.delete(student_id)
        if not student:
            raise HTTPException(
                status_code=404,
                detail=f"Không tìm thấy sinh viên với ID {student_id}"
            )
        
        return f"Đã xóa sinh viên {student.student_code}"
    
    def bulk_create_students(self, students_data: List[StudentCreate]) -> str:
        """
        Tạo nhiều sinh viên cùng lúc
        
        Business rules:
            - Không được có mã sinh viên trùng trong danh sách
            - Không được trùng với mã sinh viên đã có trong database
            
        Args:
            students_data: List các StudentCreate
            
        Returns:
            Thông báo số lượng sinh viên đã tạo
            
        Raises:
            HTTPException 400: Nếu có mã trùng
            
        Example:
            students = [
                StudentCreate(student_code="SV001", first_name="A"),
                StudentCreate(student_code="SV002", first_name="B"),
            ]
            message = service.bulk_create_students(students)
            print(message)  # "Đã tạo 2 sinh viên"
        """
        # Business rule: Check duplicate trong request
        student_codes = [s.student_code for s in students_data]
        if len(student_codes) != len(set(student_codes)):
            raise HTTPException(
                status_code=400,
                detail="Có mã sinh viên bị trùng trong danh sách"
            )
        
        # Business rule: Check duplicate với database
        for student in students_data:
            existing = self.repository.get_by_student_code(student.student_code)
            if existing:
                raise HTTPException(
                    status_code=400,
                    detail=f"Mã sinh viên {student.student_code} đã tồn tại trong database"
                )
        
        # Create all students
        count = self.repository.bulk_create(students_data)
        return f"Đã tạo thành công {count} sinh viên"

