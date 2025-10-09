# Luồng hoạt động chi tiết - Student Management System

## 📋 Mục lục

1. [Biến môi trường](#biến-môi-trường)
2. [Luồng khởi động server](#luồng-khởi-động-server)
3. [Luồng xử lý API request](#luồng-xử-lý-api-request)
4. [Luồng tương tác database](#luồng-tương-tác-database)
5. [Ví dụ chi tiết từng bước](#ví-dụ-chi-tiết)

---

## 🔐 Biến môi trường

### Biến môi trường là gì?

**Environment Variables** (Biến môi trường) là các giá trị cấu hình được lưu **ngoài code**.

**Lợi ích**:
- ✅ Bảo mật (password, API keys không để trong code)
- ✅ Dễ đổi config giữa dev/staging/production
- ✅ Không commit thông tin nhạy cảm vào Git

### Lưu ở đâu?

**File `.env`** trong thư mục `backend/`:

```
backend/
├── .env              ← File biến môi trường (KHÔNG commit)
├── .env.example      ← Template mẫu (CÓ commit)
├── .gitignore        ← Chặn .env không vào Git
└── ...
```

### Cấu trúc file `.env`

```bash
# backend/.env

# Database URL - SQLite file path
DATABASE_URL=sqlite:///./students.db

# API Server settings
API_HOST=0.0.0.0        # 0.0.0.0 = lắng nghe trên tất cả network interfaces
API_PORT=8000           # Port của server

# Debug mode (optional)
DEBUG=True
```

### Cách tạo file `.env`

**Bước 1**: Copy từ template
```bash
cd backend
cp .env.example .env    # Linux/Mac
copy .env.example .env  # Windows
```

**Bước 2**: Chỉnh sửa giá trị trong `.env`
```bash
# Mở file .env và sửa
DATABASE_URL=sqlite:///./students.db
API_PORT=8000
```

### Cách đọc biến môi trường trong code

**File `app/database.py`**:
```python
import os
from dotenv import load_dotenv

# Load biến từ file .env
load_dotenv()

# Đọc biến DATABASE_URL, nếu không có thì dùng default
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./students.db")
#                         ↑                ↑
#                      Tên biến        Giá trị mặc định
```

**File `run.py`**:
```python
import os
from dotenv import load_dotenv

load_dotenv()

host = os.getenv("API_HOST", "0.0.0.0")
port = int(os.getenv("API_PORT", 8000))
```

---

## 🚀 Luồng khởi động server

### Sơ đồ tổng quan

```
1. Chạy: python run.py
        ↓
2. Load file .env (dotenv)
        ↓
3. Import app từ app.main
        ↓
4. app/main.py được execute:
        ↓
    4a. Import database.py
        → Load .env
        → Tạo engine SQLite
        → Tạo SessionLocal
        ↓
    4b. Import models
        → Define bảng Student
        ↓
    4c. Import schemas
        → Define validation rules
        ↓
    4d. Import controllers
        → Import services
        → Import repositories
        ↓
    4e. Base.metadata.create_all()
        → Tạo file students.db (nếu chưa có)
        → Tạo bảng students (nếu chưa có)
        ↓
    4f. Tạo FastAPI app
        → Config CORS
        → Register routes
        ↓
5. Uvicorn start server
        ↓
6. Server lắng nghe tại 0.0.0.0:8000
```

### Chi tiết từng bước

#### **Bước 1: Chạy lệnh**
```bash
cd backend
python run.py
```

#### **Bước 2: File `run.py` execute**

```python
# run.py

import uvicorn
import os
from dotenv import load_dotenv

# 1. Load file .env vào environment variables
load_dotenv()

# 2. Đọc biến môi trường
host = os.getenv("API_HOST", "0.0.0.0")  # Mặc định 0.0.0.0
port = int(os.getenv("API_PORT", 8000))   # Mặc định 8000

# 3. Chạy uvicorn server
uvicorn.run(
    "app.main:app",    # Import app từ file app/main.py
    host=host,
    port=port,
    reload=True        # Auto-reload khi code thay đổi
)
```

#### **Bước 3: File `app/main.py` được import**

```python
# app/main.py

from fastapi import FastAPI
from app.database import engine, Base         # 1. Import database
from app.controllers import student_router    # 2. Import controllers

# 3. TẠO TABLES trong database
Base.metadata.create_all(bind=engine)
# Dòng này check:
#   - File students.db có chưa? → Chưa thì tạo
#   - Bảng students có chưa? → Chưa thì tạo theo Models

# 4. Tạo FastAPI instance
app = FastAPI(
    title="Student Management System API",
    version="2.0.0"
)

# 5. Config CORS (cho frontend gọi được)
app.add_middleware(CORSMiddleware, ...)

# 6. Đăng ký routes
app.include_router(student_router)
# Sau khi chạy dòng này, tất cả routes trong student_router
# đã được register: POST /api/students/, GET /api/students/, etc.
```

#### **Bước 4: Database initialization**

```python
# app/database.py

from sqlalchemy import create_engine

# 1. Load .env
load_dotenv()

# 2. Đọc DATABASE_URL
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./students.db")
# → Giá trị: "sqlite:///./students.db"
#              ↑       ↑
#           Protocol  Path tới file

# 3. Tạo engine (connection đến database)
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # SQLite specific
)

# 4. Tạo Session factory
SessionLocal = sessionmaker(bind=engine)
# SessionLocal() sẽ tạo một session mới để query DB

# 5. Tạo Base class
Base = declarative_base()
# Tất cả Models sẽ inherit từ Base này
```

#### **Bước 5: Models định nghĩa schema**

```python
# app/models/student.py

from app.database import Base

class Student(Base):
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True)
    student_code = Column(String, unique=True, nullable=False)
    # ... các columns khác
```

Khi `Base.metadata.create_all()` chạy:
```sql
-- SQL được generate tự động:
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_code VARCHAR UNIQUE NOT NULL,
    first_name VARCHAR,
    last_name VARCHAR,
    ...
);
```

#### **Bước 6: Server sẵn sàng**

```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

✅ Server đang lắng nghe tại `http://localhost:8000`

---

## 🌐 Luồng xử lý API request

### Ví dụ: Tạo sinh viên mới

#### **Bước 1: Client gửi request**

```bash
POST http://localhost:8000/api/students/
Content-Type: application/json

{
  "student_code": "SV20240001",
  "first_name": "Minh",
  "last_name": "Nguyen",
  "math_score": 8.5
}
```

#### **Bước 2: FastAPI routing**

```
Request: POST /api/students/
    ↓
FastAPI tìm route matching
    ↓
Tìm thấy: @router.post("/") trong student_controller.py
    ↓
Gọi hàm: create_student()
```

#### **Bước 3: Controller nhận request**

```python
# app/controllers/student_controller.py

@router.post("/", response_model=StudentResponse, status_code=201)
def create_student(
    student: StudentCreate,        # ← Pydantic tự động validate JSON
    db: Session = Depends(get_db)  # ← FastAPI tự động inject DB session
):
    """
    1. FastAPI deserialize JSON → StudentCreate object
    2. Pydantic validate:
       - student_code có đủ 1-20 ký tự?
       - math_score có trong khoảng 0-10?
       - Nếu SAI → raise 422 Validation Error
       - Nếu ĐÚNG → tiếp tục
    
    3. FastAPI gọi get_db() để lấy database session
    """
    
    # 4. Tạo Service instance
    service = StudentService(db)
    
    # 5. Gọi service method
    return service.create_student(student)
    # ↑ Kết quả trả về sẽ được FastAPI serialize thành JSON
```

#### **Bước 4: Service xử lý business logic**

```python
# app/services/student_service.py

class StudentService:
    def __init__(self, db: Session):
        # 1. Tạo Repository instance
        self.repository = StudentRepository(db)
    
    def create_student(self, student_data: StudentCreate) -> StudentResponse:
        """
        2. Check business rule: Mã SV có trùng không?
        """
        existing = self.repository.get_by_student_code(student_data.student_code)
        
        if existing:
            # 3a. Nếu trùng → raise HTTPException
            raise HTTPException(
                status_code=400,
                detail="Mã sinh viên đã tồn tại"
            )
        
        # 3b. Nếu OK → Gọi repository để save
        student = self.repository.create(student_data)
        
        # 4. Convert ORM model → Pydantic response
        return StudentResponse.model_validate(student)
```

#### **Bước 5: Repository thao tác database**

```python
# app/repositories/student_repository.py

class StudentRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_student_code(self, student_code: str):
        """Check mã SV có tồn tại không"""
        return self.db.query(Student)\
                      .filter(Student.student_code == student_code)\
                      .first()
        # → Chạy SQL: SELECT * FROM students WHERE student_code = 'SV20240001' LIMIT 1
    
    def create(self, student_data: StudentCreate) -> Student:
        """Tạo sinh viên mới"""
        
        # 1. Convert Pydantic → ORM model
        db_student = Student(**student_data.model_dump())
        # → Student(student_code="SV20240001", first_name="Minh", ...)
        
        # 2. Thêm vào session
        self.db.add(db_student)
        
        # 3. Commit (thực thi INSERT)
        self.db.commit()
        # → Chạy SQL: INSERT INTO students (student_code, first_name, ...) VALUES (...)
        
        # 4. Refresh để lấy ID mới
        self.db.refresh(db_student)
        # → db_student.id giờ có giá trị (ví dụ: 1)
        
        return db_student
```

#### **Bước 6: Database thực thi SQL**

```sql
-- SQLite execute:
INSERT INTO students (
    student_code, 
    first_name, 
    last_name, 
    math_score
) VALUES (
    'SV20240001',
    'Minh',
    'Nguyen',
    8.5
);

-- Return ID: 1
```

#### **Bước 7: Response trả về**

```
Repository returns: Student object (id=1, student_code="SV20240001", ...)
    ↓
Service converts: Student → StudentResponse
    ↓
Controller returns: StudentResponse
    ↓
FastAPI serializes: StudentResponse → JSON
    ↓
HTTP Response:
    Status: 201 Created
    Body: {
        "id": 1,
        "student_code": "SV20240001",
        "first_name": "Minh",
        "last_name": "Nguyen",
        "math_score": 8.5,
        "email": null,
        ...
    }
    ↓
Client nhận được response
```

---

## 💾 Luồng tương tác database

### Database Session Lifecycle

```python
# Khi request đến:

1. FastAPI gọi: db = get_db()
        ↓
    def get_db():
        db = SessionLocal()  # Tạo session mới
        try:
            yield db         # Trả session cho controller
        finally:
            db.close()       # Đóng session sau khi xong

2. Session được pass vào controller
        ↓
3. Controller pass vào Service
        ↓
4. Service pass vào Repository
        ↓
5. Repository dùng session để query
        ↓
6. Sau khi response, finally block chạy
        ↓
7. db.close() - đóng connection
```

### Transaction Flow

```python
# Repository.create()

self.db.add(db_student)     # 1. Thêm vào pending changes
self.db.commit()            # 2. BEGIN TRANSACTION
                            #    → Execute INSERT
                            #    → COMMIT
                            # Nếu lỗi → ROLLBACK

# Nếu không gọi commit():
# - Changes chỉ ở trong session
# - Chưa lưu vào database
# - Khi session.close() → bỏ hết changes
```

---

## 📝 Ví dụ chi tiết: Lấy danh sách sinh viên

### Request
```
GET http://localhost:8000/api/students/?skip=0&limit=10&search=Nguyen
```

### Luồng xử lý

**1. Controller nhận request**
```python
@router.get("/")
def get_students(
    skip: int = 0,
    limit: int = 10,
    search: str = "Nguyen",
    db: Session = Depends(get_db)
):
    service = StudentService(db)
    return service.get_all_students(skip, limit, search)
```

**2. Service gọi repository**
```python
def get_all_students(self, skip, limit, search):
    # Lấy danh sách
    students = self.repository.get_all(skip, limit, search)
    
    # Đếm tổng số
    total = self.repository.count(search)
    
    return StudentListResponse(
        total=total,
        students=[StudentResponse.model_validate(s) for s in students]
    )
```

**3. Repository query database**
```python
def get_all(self, skip, limit, search):
    query = self.db.query(Student)
    
    # Thêm filter nếu có search
    if search:
        query = query.filter(
            or_(
                Student.first_name.contains(search),
                Student.last_name.contains(search),
                ...
            )
        )
    
    # Pagination
    return query.offset(skip).limit(limit).all()
```

**SQL được generate**:
```sql
SELECT * FROM students 
WHERE first_name LIKE '%Nguyen%' 
   OR last_name LIKE '%Nguyen%'
   OR ...
LIMIT 10 OFFSET 0;
```

**4. Response**
```json
{
  "total": 25,
  "students": [
    {
      "id": 1,
      "student_code": "SV20240001",
      "first_name": "Minh",
      "last_name": "Nguyen",
      ...
    },
    ...
  ]
}
```

---

## 🔧 Dependency Injection Flow

FastAPI tự động inject dependencies:

```python
def create_student(
    student: StudentCreate,        # ← FROM: Request body
    db: Session = Depends(get_db)  # ← FROM: Dependency
):
```

**Cách hoạt động**:

```
1. Request đến
    ↓
2. FastAPI thấy Depends(get_db)
    ↓
3. Gọi get_db()
    ↓
4. get_db() return Session object
    ↓
5. Pass session vào parameter db
    ↓
6. Hàm create_student() execute với db đã có
    ↓
7. Sau khi xong, get_db() chạy finally block
    ↓
8. db.close()
```

---

## 🎯 Tóm tắt

### Biến môi trường
- ✅ Lưu trong file `.env`
- ✅ Load bằng `python-dotenv`
- ✅ Đọc bằng `os.getenv()`
- ✅ KHÔNG commit `.env` vào Git

### Luồng tổng quan
```
Client Request
    ↓
Controller (HTTP handling)
    ↓
Service (Business logic)
    ↓
Repository (Database query)
    ↓
Database (SQLite file)
    ↓
Repository returns data
    ↓
Service processes
    ↓
Controller returns response
    ↓
Client receives JSON
```

### Key Points
- 🔄 Mỗi request có 1 database session riêng
- 🔒 Session tự động đóng sau khi response
- ✅ FastAPI tự động validate input/output
- 🎯 Tách biệt rõ ràng: Controller - Service - Repository

---

Đọc file này kèm code để hiểu rõ hơn! 🚀

