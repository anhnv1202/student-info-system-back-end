"""
Student Controller
Lớp xử lý HTTP requests/responses
Định nghĩa các API endpoints và gọi service
"""

from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.services import StudentService
from app.schemas import (
    StudentCreate,
    StudentUpdate,
    StudentResponse,
    StudentListResponse,
    MessageResponse
)

from app.crawling.clean_data import clean_student_data
from app.crawling.students_crawl import crawl_students
from app.crawling.analysis_data import analysis_data
import os
from zipfile import ZipFile

# Tạo router cho student endpoints
router = APIRouter(
    prefix="/api/students",  # Tất cả routes sẽ bắt đầu với /api/students
    tags=["students"]  # Tag cho Swagger documentation
)


@router.post("/", response_model=StudentResponse, status_code=201)
def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db)
):
    """
    API: Tạo sinh viên mới
    
    Method: POST
    Endpoint: /api/students/
    
    Request Body:
        {
            "student_code": "SV20240001",  // Bắt buộc
            "first_name": "Minh",          // Optional
            "last_name": "Nguyen",         // Optional
            "email": "minh@student.edu.vn",// Optional
            "date_of_birth": "2002-05-15", // Optional (YYYY-MM-DD)
            "hometown": "Hà Nội",          // Optional
            "math_score": 8.5,             // Optional (0-10)
            "literature_score": 7.5,       // Optional (0-10)
            "english_score": 9.0           // Optional (0-10)
        }
    
    Response: StudentResponse (status 201 Created)
        {
            "id": 1,
            "student_code": "SV20240001",
            "first_name": "Minh",
            ...
        }
    
    Errors:
        - 400: Mã sinh viên đã tồn tại
        - 422: Dữ liệu không hợp lệ (validation error)
    
    Example curl:
        curl -X POST "http://localhost:8000/api/students/" \\
             -H "Content-Type: application/json" \\
             -d '{"student_code": "SV001", "first_name": "Minh"}'
    """
    service = StudentService(db)
    return service.create_student(student)


@router.get("/", response_model=StudentListResponse)
def get_students(
    skip: int = Query(
        0, 
        ge=0, 
        description="Số lượng record bỏ qua (dùng cho pagination)"
    ),
    limit: int = Query(
        100, 
        ge=1, 
        le=1000, 
        description="Số lượng record tối đa trả về (1-1000)"
    ),
    search: Optional[str] = Query(
        None, 
        description="Từ khóa tìm kiếm (tìm trong mã SV, tên, email, quê quán)"
    ),
    db: Session = Depends(get_db)
):
    """
    API: Lấy danh sách tất cả sinh viên
    
    Method: GET
    Endpoint: /api/students/
    
    Query Parameters:
        - skip: Số record bỏ qua (mặc định: 0)
        - limit: Số record tối đa (mặc định: 100, max: 1000)
        - search: Từ khóa tìm kiếm (optional)
    
    Response: StudentListResponse
        {
            "total": 100,
            "students": [
                {
                    "id": 1,
                    "student_code": "SV20240001",
                    "first_name": "Minh",
                    ...
                },
                ...
            ]
        }
    
    Example URLs:
        - Lấy 10 sinh viên đầu tiên:
          GET /api/students/?skip=0&limit=10
          
        - Lấy sinh viên từ 11-20 (page 2):
          GET /api/students/?skip=10&limit=10
          
        - Tìm kiếm sinh viên tên "Nguyen":
          GET /api/students/?search=Nguyen
          
        - Kết hợp search và pagination:
          GET /api/students/?search=Nguyen&skip=0&limit=10
    """
    service = StudentService(db)
    return service.get_all_students(skip=skip, limit=limit, search=search)


@router.get("/{student_id}", response_model=StudentResponse)
def get_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    """
    API: Lấy thông tin 1 sinh viên theo ID
    
    Method: GET
    Endpoint: /api/students/{student_id}
    
    Path Parameters:
        - student_id: ID của sinh viên
    
    Response: StudentResponse
        {
            "id": 1,
            "student_code": "SV20240001",
            "first_name": "Minh",
            ...
        }
    
    Errors:
        - 404: Không tìm thấy sinh viên
    
    Example:
        GET /api/students/1
    """
    service = StudentService(db)
    return service.get_student_by_id(student_id)


@router.put("/{student_id}", response_model=StudentResponse)
def update_student(
    student_id: int,
    student: StudentUpdate,
    db: Session = Depends(get_db)
):
    """
    API: Cập nhật thông tin sinh viên
    
    Method: PUT
    Endpoint: /api/students/{student_id}
    
    Path Parameters:
        - student_id: ID của sinh viên cần update
    
    Request Body: (tất cả đều optional, chỉ gửi trường cần update)
        {
            "math_score": 9.5,
            "english_score": 8.0
        }
        
    Response: StudentResponse (thông tin sinh viên sau khi update)
    
    Errors:
        - 404: Không tìm thấy sinh viên
        - 400: Mã sinh viên mới bị trùng
        - 422: Dữ liệu không hợp lệ
    
    Example:
        # Chỉ update điểm Toán
        PUT /api/students/1
        Body: {"math_score": 9.5}
        
        # Update nhiều trường
        PUT /api/students/1
        Body: {
            "first_name": "Minh Updated",
            "math_score": 9.5,
            "english_score": 8.0
        }
    """
    service = StudentService(db)
    return service.update_student(student_id, student)


@router.delete("/{student_id}", response_model=MessageResponse)
def delete_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    """
    API: Xóa sinh viên
    
    Method: DELETE
    Endpoint: /api/students/{student_id}
    
    Path Parameters:
        - student_id: ID của sinh viên cần xóa
    
    Response: MessageResponse
        {
            "message": "Đã xóa sinh viên SV20240001"
        }
    
    Errors:
        - 404: Không tìm thấy sinh viên
    
    Example:
        DELETE /api/students/1
    """
    service = StudentService(db)
    message = service.delete_student(student_id)
    return MessageResponse(message=message)


@router.post("/bulk", response_model=MessageResponse)
def bulk_create_students(
    students: list[StudentCreate],
    db: Session = Depends(get_db)
):
    """
    API: Tạo nhiều sinh viên cùng lúc (bulk create)
    
    Method: POST
    Endpoint: /api/students/bulk
    
    Request Body: Array của StudentCreate
        [
            {
                "student_code": "SV001",
                "first_name": "Minh",
                "math_score": 8.5
            },
            {
                "student_code": "SV002",
                "first_name": "Lan",
                "math_score": 9.0
            }
        ]
    
    Response: MessageResponse
        {
            "message": "Đã tạo thành công 2 sinh viên"
        }
    
    Errors:
        - 400: Có mã sinh viên trùng (trong request hoặc với database)
        - 422: Dữ liệu không hợp lệ
    
    Use case:
        - Import dữ liệu từ Excel/CSV
        - Tạo nhiều sinh viên cùng lúc
    
    Example curl:
        curl -X POST "http://localhost:8000/api/students/bulk" \\
             -H "Content-Type: application/json" \\
             -d '[
                   {"student_code": "SV001", "first_name": "A"},
                   {"student_code": "SV002", "first_name": "B"}
                 ]'
    """
    service = StudentService(db)
    message = service.bulk_create_students(students)
    return MessageResponse(message=message)


@router.post("/crawl-students")
def crawl_students_api():
    # Step 1: Crawl data and export to CSV
    url = os.getenv("STUDENTS_URL", "http://localhost:3000/students")
    raw_filename = crawl_students(url)

    # Step 2: Clean data
    cleaned_filename = clean_student_data(raw_filename)

    # Step 3: Analyze data and export images
    analysis_data(cleaned_filename)

    # Step 4: Zip images
    image_dir = os.path.join("app", "crawling", "results")
    zip_path = "exported_images.zip"
    with ZipFile(zip_path, "w") as zipf:
        for root, _, files in os.walk(image_dir):
            for file in files:
                zipf.write(os.path.join(root, file), arcname=file)

    # Step 5: Return zip file
    with open(zip_path, "rb") as f:
        zip_bytes = f.read()
    os.remove(zip_path)
    return Response(content=zip_bytes, media_type="application/zip")

