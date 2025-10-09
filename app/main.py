"""
Main Application File
Khởi tạo FastAPI application và cấu hình middleware
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.controllers import student_router

# Tạo tất cả các tables trong database (nếu chưa tồn tại)
Base.metadata.create_all(bind=engine)

# Khởi tạo FastAPI application
app = FastAPI(
    title="Student Management System API",
    description="""
    API quản lý thông tin sinh viên
    
    ## Tính năng
    - ✅ CRUD operations (Create, Read, Update, Delete)
    - ✅ Search và Filter
    - ✅ Pagination
    - ✅ Bulk create
    - ✅ Data validation
    
    ## Architecture
    - **Controller**: Xử lý HTTP requests/responses
    - **Service**: Business logic
    - **Repository**: Database operations
    - **Models**: Database schema
    - **Schemas**: Request/Response validation
    """,
    version="2.0.0",
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc"  # ReDoc
)

# Cấu hình CORS (Cross-Origin Resource Sharing)
# Cho phép frontend từ domain khác gọi API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Production: thay bằng domain cụ thể ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],  # Cho phép tất cả methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Cho phép tất cả headers
)

# Đăng ký router
app.include_router(student_router)


@app.get("/", tags=["Root"])
def root():
    """
    Root endpoint - Thông tin API
    
    Returns:
        Thông tin cơ bản về API
    """
    return {
        "message": "Student Management System API",
        "version": "2.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "architecture": "Controller - Service - Repository"
    }


@app.get("/health", tags=["Health"])
def health_check():
    """
    Health check endpoint
    
    Dùng để kiểm tra API có đang hoạt động không.
    Thường dùng cho monitoring tools.
    
    Returns:
        Status healthy nếu API đang chạy
    """
    return {"status": "healthy"}
