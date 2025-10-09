# Kiến trúc Project - Student Management System

## 📐 Tổng quan kiến trúc

Project sử dụng **3-layer architecture** với pattern:
- **Controller Layer** (Presentation)
- **Service Layer** (Business Logic)
- **Repository Layer** (Data Access)

```
┌─────────────────────────────────────────┐
│         HTTP Request/Response           │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│     CONTROLLER (student_controller.py)  │
│  - Xử lý HTTP requests                  │
│  - Validate input từ user               │
│  - Gọi Service layer                    │
│  - Format response                      │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│      SERVICE (student_service.py)       │
│  - Business logic                       │
│  - Business rules validation            │
│  - Xử lý exceptions                     │
│  - Gọi Repository layer                 │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│   REPOSITORY (student_repository.py)    │
│  - Database operations (CRUD)           │
│  - Query database                       │
│  - Không chứa business logic            │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│          DATABASE (SQLite)              │
│  - Lưu trữ dữ liệu                      │
└─────────────────────────────────────────┘
```

## 📁 Cấu trúc thư mục

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI app initialization
│   ├── database.py                # Database connection
│   │
│   ├── models/                    # Database Models (ORM)
│   │   ├── __init__.py
│   │   └── student.py            # Student table definition
│   │
│   ├── schemas/                   # Pydantic Schemas (Validation)
│   │   ├── __init__.py
│   │   └── student.py            # Request/Response schemas
│   │
│   ├── repositories/              # Data Access Layer
│   │   ├── __init__.py
│   │   └── student_repository.py # Database operations
│   │
│   ├── services/                  # Business Logic Layer
│   │   ├── __init__.py
│   │   └── student_service.py    # Business rules
│   │
│   └── controllers/               # Presentation Layer
│       ├── __init__.py
│       └── student_controller.py # API endpoints
│
├── scripts/
│   └── generate_sample_data.py   # Generate sample data
│
├── requirements.txt
├── run.py
└── README.md
```

## 🎯 Nhiệm vụ từng Layer

### 1. Controller Layer (`controllers/student_controller.py`)

**Vai trò**: Xử lý HTTP requests/responses

**Nhiệm vụ**:
- ✅ Define API endpoints (routes)
- ✅ Nhận HTTP request
- ✅ Parse query parameters, path parameters
- ✅ Gọi Service layer
- ✅ Trả về HTTP response
- ❌ KHÔNG chứa business logic
- ❌ KHÔNG tương tác trực tiếp với database

**Ví dụ**:
```python
@router.post("/", response_model=StudentResponse, status_code=201)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    """API endpoint để tạo sinh viên"""
    service = StudentService(db)
    return service.create_student(student)  # Gọi service
```

### 2. Service Layer (`services/student_service.py`)

**Vai trò**: Chứa business logic

**Nhiệm vụ**:
- ✅ Business rules và validation
- ✅ Xử lý logic phức tạp
- ✅ Kết hợp nhiều repository operations
- ✅ Handle exceptions
- ✅ Gọi Repository layer
- ❌ KHÔNG xử lý HTTP
- ❌ KHÔNG viết SQL/query trực tiếp

**Ví dụ**:
```python
def create_student(self, student_data: StudentCreate) -> StudentResponse:
    """Business logic: Tạo sinh viên với validation"""
    
    # Business rule: Check duplicate student code
    existing = self.repository.get_by_student_code(student_data.student_code)
    if existing:
        raise HTTPException(status_code=400, detail="Mã SV đã tồn tại")
    
    # Gọi repository để save
    student = self.repository.create(student_data)
    return StudentResponse.model_validate(student)
```

### 3. Repository Layer (`repositories/student_repository.py`)

**Vai trò**: Tương tác với database

**Nhiệm vụ**:
- ✅ Database queries (SELECT, INSERT, UPDATE, DELETE)
- ✅ CRUD operations
- ✅ Data access logic
- ❌ KHÔNG chứa business rules
- ❌ KHÔNG raise HTTPException
- ❌ KHÔNG biết gì về HTTP

**Ví dụ**:
```python
def create(self, student_data: StudentCreate) -> Student:
    """Tạo student trong database"""
    db_student = Student(**student_data.model_dump())
    self.db.add(db_student)
    self.db.commit()
    self.db.refresh(db_student)
    return db_student
```

## 🔄 Luồng xử lý request

### Ví dụ: Tạo sinh viên mới

```
1. CLIENT gửi POST request
   ↓
   POST /api/students/
   Body: {"student_code": "SV001", "first_name": "Minh"}

2. CONTROLLER nhận request
   ↓
   student_controller.create_student()
   - Parse request body
   - Validate schema (Pydantic)

3. CONTROLLER gọi SERVICE
   ↓
   StudentService.create_student()
   - Check business rules (duplicate code?)
   - Nếu OK, gọi Repository

4. SERVICE gọi REPOSITORY
   ↓
   StudentRepository.create()
   - INSERT vào database
   - Return Student object

5. SERVICE nhận kết quả
   ↓
   - Convert Student → StudentResponse
   - Return về Controller

6. CONTROLLER trả response
   ↓
   HTTP 201 Created
   Body: {"id": 1, "student_code": "SV001", ...}

7. CLIENT nhận response
```

## 🎨 Models vs Schemas

### Models (`models/student.py`)
- **ORM Models** (SQLAlchemy)
- Định nghĩa cấu trúc **bảng trong database**
- Map class Python ↔ table database
- Dùng bởi: Repository

```python
class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    student_code = Column(String, unique=True)
    # ... other columns
```

### Schemas (`schemas/student.py`)
- **Pydantic Models**
- Định nghĩa cấu trúc **request/response data**
- Validation dữ liệu từ client
- Serialize/Deserialize JSON
- Dùng bởi: Controller, Service

```python
class StudentCreate(BaseModel):
    student_code: str
    first_name: Optional[str]
    # ... validation rules
```

## 💡 Tại sao chia tách như vậy?

### ✅ Ưu điểm

1. **Separation of Concerns**
   - Mỗi layer có 1 trách nhiệm rõ ràng
   - Dễ hiểu, dễ maintain

2. **Testable**
   - Test từng layer độc lập
   - Mock dependencies dễ dàng

3. **Scalable**
   - Thay đổi 1 layer không ảnh hưởng layer khác
   - Dễ mở rộng chức năng

4. **Reusable**
   - Service có thể gọi từ nhiều controller
   - Repository có thể dùng cho nhiều service

5. **Team Work**
   - Nhiều người làm song song
   - Clear boundaries

### 📚 Ví dụ thực tế

#### ❌ Không tốt (All-in-one)
```python
@router.post("/")
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    # Mix tất cả logic vào controller
    existing = db.query(Student).filter(Student.student_code == student.student_code).first()
    if existing:
        raise HTTPException(400, "Duplicate")
    db_student = Student(**student.dict())
    db.add(db_student)
    db.commit()
    return db_student
```

#### ✅ Tốt (Layered)
```python
# Controller - chỉ lo HTTP
@router.post("/")
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    service = StudentService(db)
    return service.create_student(student)

# Service - business logic
def create_student(self, student_data):
    if self.repository.get_by_student_code(student_data.student_code):
        raise HTTPException(400, "Duplicate")
    return self.repository.create(student_data)

# Repository - database
def create(self, student_data):
    db_student = Student(**student_data.dict())
    self.db.add(db_student)
    self.db.commit()
    return db_student
```

## 🔧 Cách sử dụng

### Thêm chức năng mới

**Ví dụ**: Thêm API tính điểm trung bình

1. **Repository** - Thêm query lấy điểm
```python
# repositories/student_repository.py
def get_scores(self, student_id: int):
    student = self.get_by_id(student_id)
    return {
        'math': student.math_score,
        'literature': student.literature_score,
        'english': student.english_score
    }
```

2. **Service** - Business logic tính trung bình
```python
# services/student_service.py
def calculate_average(self, student_id: int) -> float:
    scores = self.repository.get_scores(student_id)
    # Business logic
    valid_scores = [s for s in scores.values() if s is not None]
    if not valid_scores:
        return 0
    return sum(valid_scores) / len(valid_scores)
```

3. **Controller** - Thêm endpoint
```python
# controllers/student_controller.py
@router.get("/{student_id}/average")
def get_average_score(student_id: int, db: Session = Depends(get_db)):
    service = StudentService(db)
    average = service.calculate_average(student_id)
    return {"average": average}
```

## 📖 Best Practices

1. **Controller** chỉ nên có vài dòng code
2. **Service** chứa toàn bộ business logic
3. **Repository** chỉ nên có database queries
4. Luôn validate ở Service, không tin tưởng input
5. Dùng Schemas cho validation tự động
6. Handle errors ở Service layer
7. Mỗi function nên có docstring rõ ràng

## 🎓 Kết luận

Kiến trúc này giúp code:
- ✅ Dễ đọc, dễ hiểu
- ✅ Dễ test
- ✅ Dễ maintain
- ✅ Dễ mở rộng
- ✅ Phù hợp cho team work
- ✅ Follow best practices

Hãy tuân thủ pattern này khi thêm chức năng mới! 🚀

