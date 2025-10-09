"""
Student Schemas
Định nghĩa cấu trúc dữ liệu cho request/response validation
Sử dụng Pydantic để validate dữ liệu đầu vào/đầu ra
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class StudentBase(BaseModel):
    """
    Base Student Schema
    
    Schema cơ bản chứa tất cả các trường của student.
    Các schema khác sẽ kế thừa từ schema này.
    
    Attributes:
        student_code: Mã sinh viên (bắt buộc, 1-20 ký tự)
        first_name: Tên (optional, tối đa 50 ký tự)
        last_name: Họ (optional, tối đa 50 ký tự)
        email: Email (optional, tối đa 100 ký tự)
        date_of_birth: Ngày sinh (optional)
        hometown: Quê quán (optional, tối đa 100 ký tự)
        math_score: Điểm Toán (optional, 0-10)
        literature_score: Điểm Văn (optional, 0-10)
        english_score: Điểm Anh (optional, 0-10)
    """
    student_code: str = Field(
        ..., 
        min_length=1, 
        max_length=20, 
        description="Mã sinh viên (bắt buộc)"
    )
    first_name: Optional[str] = Field(
        None, 
        max_length=50, 
        description="Tên sinh viên"
    )
    last_name: Optional[str] = Field(
        None, 
        max_length=50, 
        description="Họ sinh viên"
    )
    email: Optional[str] = Field(
        None, 
        max_length=100, 
        description="Email"
    )
    date_of_birth: Optional[date] = Field(
        None, 
        description="Ngày sinh (YYYY-MM-DD)"
    )
    hometown: Optional[str] = Field(
        None, 
        max_length=100, 
        description="Quê quán"
    )
    math_score: Optional[float] = Field(
        None, 
        ge=0, 
        le=10, 
        description="Điểm Toán (0-10)"
    )
    literature_score: Optional[float] = Field(
        None, 
        ge=0, 
        le=10, 
        description="Điểm Văn (0-10)"
    )
    english_score: Optional[float] = Field(
        None, 
        ge=0, 
        le=10, 
        description="Điểm Anh (0-10)"
    )


class StudentCreate(StudentBase):
    """
    Student Create Schema
    
    Schema dùng khi tạo sinh viên mới.
    Kế thừa tất cả các trường từ StudentBase.
    
    Sử dụng trong:
        - POST /api/students/ (tạo 1 sinh viên)
        - POST /api/students/bulk (tạo nhiều sinh viên)
    """
    # Inherit all fields from StudentBase without modifications
    ...


class StudentUpdate(BaseModel):
    """
    Student Update Schema
    
    Schema dùng khi cập nhật sinh viên.
    Tất cả các trường đều optional - chỉ cập nhật trường nào được gửi lên.
    
    Sử dụng trong:
        - PUT /api/students/{id} (cập nhật sinh viên)
        
    Example:
        # Chỉ cập nhật điểm Toán
        {"math_score": 9.5}
        
        # Cập nhật nhiều trường
        {"math_score": 9.5, "english_score": 8.0}
    """
    student_code: Optional[str] = Field(None, min_length=1, max_length=20)
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)
    email: Optional[str] = Field(None, max_length=100)
    date_of_birth: Optional[date] = None
    hometown: Optional[str] = Field(None, max_length=100)
    math_score: Optional[float] = Field(None, ge=0, le=10)
    literature_score: Optional[float] = Field(None, ge=0, le=10)
    english_score: Optional[float] = Field(None, ge=0, le=10)


class StudentResponse(StudentBase):
    """
    Student Response Schema
    
    Schema dùng để trả về thông tin sinh viên từ API.
    Bao gồm cả ID của sinh viên.
    
    Sử dụng trong:
        - Response của tất cả các API endpoint
        
    Config:
        from_attributes: Cho phép convert từ ORM model sang Pydantic model
    """
    id: int  # Thêm trường ID khi trả về response

    class Config:
        from_attributes = True  # Cho phép đọc data từ ORM model


class StudentListResponse(BaseModel):
    """
    Student List Response Schema
    
    Schema dùng để trả về danh sách sinh viên kèm tổng số.
    
    Sử dụng trong:
        - GET /api/students/ (lấy danh sách sinh viên)
        
    Attributes:
        total: Tổng số sinh viên (dùng cho pagination)
        students: Danh sách các sinh viên
    """
    total: int = Field(..., description="Tổng số sinh viên")
    students: list[StudentResponse] = Field(..., description="Danh sách sinh viên")


class MessageResponse(BaseModel):
    """
    Message Response Schema
    
    Schema đơn giản để trả về message text.
    
    Sử dụng trong:
        - DELETE /api/students/{id} (xóa sinh viên)
        - POST /api/students/bulk (tạo nhiều sinh viên)
        
    Attributes:
        message: Nội dung thông báo
    """
    message: str = Field(..., description="Nội dung thông báo")

