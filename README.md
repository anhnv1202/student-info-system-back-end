# Student Management System - Backend API

FastAPI-based REST API quản lý thông tin sinh viên với SQLite database.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📋 Mục lục

- [Tính năng](#-tính-năng)
- [Công nghệ sử dụng](#-công-nghệ-sử-dụng)
- [Kiến trúc](#-kiến-trúc)
- [Cài đặt](#-cài-đặt)
- [Sử dụng](#-sử-dụng)
- [API Documentation](#-api-documentation)
- [Database](#-database)
- [Tài liệu chi tiết](#-tài-liệu-chi-tiết)

---

## ✨ Tính năng

- ✅ **CRUD Operations**: Create, Read, Update, Delete sinh viên
- 🔍 **Search & Filter**: Tìm kiếm theo mã SV, tên, email, quê quán
- 📄 **Pagination**: Phân trang dữ liệu hiệu quả
- 📦 **Bulk Operations**: Tạo nhiều sinh viên cùng lúc
- ✔️ **Data Validation**: Pydantic schemas tự động validate
- 📚 **Auto Documentation**: Swagger UI và ReDoc
- 🌐 **CORS Support**: Hỗ trợ tích hợp frontend
- 🎲 **Sample Data**: Script tạo 100 sinh viên mẫu với dữ liệu thiếu

---

## 🛠️ Công nghệ sử dụng

| Technology | Version | Purpose |
|------------|---------|---------|
| **FastAPI** | 0.104.1 | Modern Python web framework |
| **SQLAlchemy** | 2.0.23 | SQL toolkit và ORM |
| **SQLite** | Built-in | Lightweight embedded database |
| **Pydantic** | 2.5.0 | Data validation |
| **Pandas** | 2.2+ | Data preprocessing và analysis |
| **Faker** | 20.1.0 | Generate realistic sample data |
| **Uvicorn** | 0.24.0 | ASGI server |
| **python-dotenv** | 1.0.0 | Environment variables |

---

## 🏗️ Kiến trúc

Project sử dụng **3-layer architecture** (Repository - Service - Controller pattern):

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                  # FastAPI app initialization
│   ├── database.py              # Database connection & session
│   │
│   ├── models/                  # 🗄️ Database Models (SQLAlchemy ORM)
│   │   ├── __init__.py
│   │   └── student.py          # Student table definition
│   │
│   ├── schemas/                 # ✅ Pydantic Schemas (Validation)
│   │   ├── __init__.py
│   │   └── student.py          # Request/Response schemas
│   │
│   ├── repositories/            # 💾 Data Access Layer
│   │   ├── __init__.py
│   │   └── student_repository.py  # Database operations (CRUD)
│   │
│   ├── services/                # 💼 Business Logic Layer
│   │   ├── __init__.py
│   │   └── student_service.py  # Business rules & validation
│   │
│   └── controllers/             # 🌐 Presentation Layer
│       ├── __init__.py
│       └── student_controller.py  # API endpoints (HTTP handlers)
│
├── scripts/
│   ├── __init__.py
│   └── generate_sample_data.py  # Generate 100 sample students
│
├── requirements.txt             # Python dependencies
├── run.py                       # Application runner
├── .env.example                 # Environment variables template
├── .gitignore                   # Git ignore rules
│
├── view_database.py             # Tool: View database content
├── query_db.py                  # Tool: Run SQL queries
│
├── README.md                    # This file
├── ARCHITECTURE.md              # Architecture documentation
└── FLOW_GUIDE.md               # Detailed flow explanation
```

### Luồng xử lý request:

```
Client Request
    ↓
Controller (HTTP handling)
    ↓
Service (Business logic & validation)
    ↓
Repository (Database operations)
    ↓
SQLite Database
```

📖 **Đọc thêm**: [ARCHITECTURE.md](ARCHITECTURE.md), [FLOW_GUIDE.md](FLOW_GUIDE.md)

---

## 📦 Cài đặt

### Prerequisites

- **Python 3.8+** ([Download](https://www.python.org/downloads/))
- **pip** (Python package manager)
- **Git** (optional)

### Bước 1: Clone/Download project

```bash
cd backend
```

### Bước 2: Tạo virtual environment (Khuyến nghị)

```bash
# Tạo virtual environment
python -m venv venv

# Kích hoạt virtual environment

# Windows (Command Prompt)
venv\Scripts\activate

# Windows (PowerShell)
venv\Scripts\Activate.ps1

# Windows (Git Bash)
source venv/Scripts/activate

# Linux/Mac
source venv/bin/activate
```

**Lưu ý**: Sau khi activate, terminal sẽ hiển thị `(venv)` ở đầu dòng.

### Bước 3: Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### Bước 4: Cấu hình Environment Variables (Optional)

File `.env` đã có sẵn với cấu hình mặc định. Nếu muốn thay đổi:

```bash
# Copy template
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac

# Chỉnh sửa .env
DATABASE_URL=sqlite:///./students.db
API_HOST=0.0.0.0
API_PORT=8000
```

---

## 🚀 Sử dụng

### 1. Chạy API Server

```bash
python run.py
```

**Output**:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Started server process
INFO:     Application startup complete.
```

✅ Server đang chạy tại: **http://localhost:8000**

### 2. Tạo dữ liệu mẫu (100 sinh viên)

```bash
python scripts/generate_sample_data.py
```

**Kết quả**:
- ✅ Tạo 100 sinh viên với dữ liệu tiếng Việt thực tế
- ✅ Một số trường thiếu dữ liệu (5-15% mỗi trường)
- ✅ Hiển thị thống kê với pandas
- ✅ Export ra file `students_data.csv`

### 3. Xem dữ liệu trong database

#### Cách 1: Script Python (Nhanh nhất)

```bash
# Xem tất cả sinh viên
python view_database.py

# Tìm kiếm sinh viên
python view_database.py Nguyen
```

#### Cách 2: Interactive SQL Query

```bash
python query_db.py
```

Sau đó gõ SQL:
```sql
SQL> SELECT * FROM students LIMIT 5;
SQL> SELECT student_code, first_name, math_score FROM students WHERE math_score > 8;
SQL> exit
```

#### Cách 3: GUI Tool

Download **DB Browser for SQLite**: https://sqlitebrowser.org/
- Mở file: `backend/students.db`
- Xem, edit, query bằng giao diện đồ họa

#### Cách 4: VS Code Extension

- Cài extension: **SQLite** hoặc **SQLite Viewer**
- Click vào file `students.db` trong VS Code

### 4. Test API

**Mở trình duyệt**:
- API Root: http://localhost:8000/
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

**Hoặc dùng curl**:
```bash
# Get all students
curl http://localhost:8000/api/students/

# Search students
curl http://localhost:8000/api/students/?search=Nguyen&limit=5
```

---

## 📚 API Documentation

### Interactive Documentation

Sau khi chạy server, truy cập:

- **Swagger UI** (Recommended): http://localhost:8000/docs
  - Giao diện đẹp, dễ dùng
  - Test API trực tiếp trên trình duyệt
  - Xem request/response schemas
  
- **ReDoc**: http://localhost:8000/redoc
  - Documentation đầy đủ, dễ đọc
  - Export sang PDF/HTML

### API Endpoints

#### Students Endpoints

| Method | Endpoint | Description | Request Body |
|--------|----------|-------------|--------------|
| **GET** | `/api/students/` | Lấy danh sách sinh viên | Query params: `skip`, `limit`, `search` |
| **POST** | `/api/students/` | Tạo sinh viên mới | `StudentCreate` schema |
| **GET** | `/api/students/{id}` | Lấy 1 sinh viên theo ID | - |
| **PUT** | `/api/students/{id}` | Cập nhật sinh viên | `StudentUpdate` schema |
| **DELETE** | `/api/students/{id}` | Xóa sinh viên | - |
| **POST** | `/api/students/bulk` | Tạo nhiều sinh viên | Array of `StudentCreate` |

#### System Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| **GET** | `/` | API information |
| **GET** | `/health` | Health check |

### Request/Response Examples

#### 1. Tạo sinh viên mới

**Request**:
```bash
POST http://localhost:8000/api/students/
Content-Type: application/json

{
  "student_code": "SV20240001",
  "first_name": "Minh",
  "last_name": "Nguyen",
  "email": "minh.nguyen@student.edu.vn",
  "date_of_birth": "2002-05-15",
  "hometown": "Hà Nội",
  "math_score": 8.5,
  "literature_score": 7.5,
  "english_score": 9.0
}
```

**Response** (201 Created):
```json
{
  "id": 1,
  "student_code": "SV20240001",
  "first_name": "Minh",
  "last_name": "Nguyen",
  "email": "minh.nguyen@student.edu.vn",
  "date_of_birth": "2002-05-15",
  "hometown": "Hà Nội",
  "math_score": 8.5,
  "literature_score": 7.5,
  "english_score": 9.0
}
```

#### 2. Lấy danh sách sinh viên (có phân trang)

**Request**:
```bash
GET http://localhost:8000/api/students/?skip=0&limit=10
```

**Response** (200 OK):
```json
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
```

#### 3. Tìm kiếm sinh viên

**Request**:
```bash
GET http://localhost:8000/api/students/?search=Nguyen&limit=5
```

Tìm trong: `student_code`, `first_name`, `last_name`, `email`, `hometown`

#### 4. Cập nhật sinh viên (chỉ update 1 số fields)

**Request**:
```bash
PUT http://localhost:8000/api/students/1
Content-Type: application/json

{
  "math_score": 9.5
}
```

**Response** (200 OK): Student object với `math_score` đã được update

#### 5. Xóa sinh viên

**Request**:
```bash
DELETE http://localhost:8000/api/students/1
```

**Response** (200 OK):
```json
{
  "message": "Đã xóa sinh viên SV20240001"
}
```

#### 6. Bulk create (Tạo nhiều sinh viên)

**Request**:
```bash
POST http://localhost:8000/api/students/bulk
Content-Type: application/json

[
  {
    "student_code": "SV001",
    "first_name": "An",
    "math_score": 8.0
  },
  {
    "student_code": "SV002",
    "first_name": "Binh",
    "math_score": 7.5
  }
]
```

**Response** (200 OK):
```json
{
  "message": "Đã tạo thành công 2 sinh viên"
}
```

---

## 🗄️ Database

### SQLite Configuration

- **Type**: SQLite (Embedded database, không cần cài đặt server)
- **File**: `students.db` (tự động tạo khi chạy server lần đầu)
- **ORM**: SQLAlchemy
- **Schema**: Tự động tạo từ Models (không cần migration)

### Database Schema

**Table: `students`**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | ID tự động tăng |
| `student_code` | VARCHAR | UNIQUE, NOT NULL | Mã sinh viên (unique) |
| `first_name` | VARCHAR | NULLABLE | Tên sinh viên |
| `last_name` | VARCHAR | NULLABLE | Họ sinh viên |
| `email` | VARCHAR | NULLABLE | Email |
| `date_of_birth` | DATE | NULLABLE | Ngày sinh (YYYY-MM-DD) |
| `hometown` | VARCHAR | NULLABLE | Quê quán |
| `math_score` | FLOAT | NULLABLE, CHECK(0-10) | Điểm Toán |
| `literature_score` | FLOAT | NULLABLE, CHECK(0-10) | Điểm Văn |
| `english_score` | FLOAT | NULLABLE, CHECK(0-10) | Điểm Anh |

**Indexes**:
- PRIMARY KEY on `id`
- UNIQUE INDEX on `student_code`

### Database Operations

```bash
# Reset database (xóa tất cả dữ liệu)
# Windows
del students.db
# Linux/Mac
rm students.db

# Chạy lại server để tạo database mới
python run.py
```

---

## 📖 Tài liệu chi tiết

### 1. ARCHITECTURE.md
Kiến trúc chi tiết của project:
- Giải thích 3-layer pattern
- Vai trò từng layer (Controller - Service - Repository)
- Best practices
- Cách thêm chức năng mới

### 2. FLOW_GUIDE.md
Luồng xử lý request chi tiết:
- Biến môi trường (Environment Variables)
- Luồng khởi động server
- Luồng xử lý từng API request
- Database transaction flow
- Dependency Injection

### 3. Code Comments
Tất cả code đều có docstring đầy đủ:
- Module docstring
- Class docstring
- Function/Method docstring
- Args, Returns, Raises
- Example usage

---

## 🔧 Development

### Auto-reload Mode

Server tự động reload khi code thay đổi (đã config trong `run.py`):

```python
uvicorn.run(
    "app.main:app",
    reload=True  # ← Auto-reload
)
```

### Environment Variables

File `.env` (không commit vào Git):
```bash
DATABASE_URL=sqlite:///./students.db
API_HOST=0.0.0.0
API_PORT=8000
```

### CORS Configuration

Development (cho phép tất cả origins):
```python
allow_origins=["*"]
```

Production (chỉ định frontend domain):
```python
allow_origins=["http://localhost:3000", "https://yourdomain.com"]
```

Sửa trong `app/main.py`.

---

## ❌ Error Handling

API trả về HTTP status codes chuẩn:

| Status Code | Meaning | Example |
|-------------|---------|---------|
| **200** | Success | GET, PUT, DELETE thành công |
| **201** | Created | POST tạo mới thành công |
| **400** | Bad Request | Mã sinh viên trùng, business rule lỗi |
| **404** | Not Found | Không tìm thấy sinh viên với ID |
| **422** | Validation Error | Dữ liệu không đúng format (Pydantic validation) |
| **500** | Internal Server Error | Lỗi server |

**Example Error Response**:
```json
{
  "detail": "Mã sinh viên SV20240001 đã tồn tại"
}
```

---

## 🧪 Testing

### Test với Swagger UI

1. Chạy server: `python run.py`
2. Mở http://localhost:8000/docs
3. Click "Try it out" trên endpoint bất kỳ
4. Nhập data và click "Execute"

### Test với curl

```bash
# Create student
curl -X POST "http://localhost:8000/api/students/" \
  -H "Content-Type: application/json" \
  -d '{"student_code": "SV001", "first_name": "Test"}'

# Get students
curl "http://localhost:8000/api/students/"

# Update student
curl -X PUT "http://localhost:8000/api/students/1" \
  -H "Content-Type: application/json" \
  -d '{"math_score": 9.5}'

# Delete student
curl -X DELETE "http://localhost:8000/api/students/1"
```

### Test với Python requests

```python
import requests

# Create student
response = requests.post(
    "http://localhost:8000/api/students/",
    json={
        "student_code": "SV001",
        "first_name": "Test"
    }
)
print(response.json())
```

---

## 🚀 Production Deployment

### Option 1: Uvicorn với multiple workers

```bash
uvicorn app.main:app \
  --host 0.0.0.0 \
  --port 8000 \
  --workers 4
```

### Option 2: Gunicorn với Uvicorn workers

```bash
pip install gunicorn

gunicorn app.main:app \
  -w 4 \
  -k uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
```

### Option 3: Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 🎯 Roadmap

- [ ] User authentication & authorization (JWT)
- [ ] File upload (student photos)
- [ ] Export data to Excel/PDF
- [ ] Advanced filtering & sorting
- [ ] Data analytics dashboard
- [ ] Email notifications
- [ ] Audit logging
- [ ] Unit tests & Integration tests
- [ ] CI/CD pipeline
- [ ] Dockerize

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details

---

## 📞 Support

Nếu có vấn đề hoặc câu hỏi:

- 📖 Đọc [ARCHITECTURE.md](ARCHITECTURE.md) và [FLOW_GUIDE.md](FLOW_GUIDE.md)
- 🐛 Report bugs: [GitHub Issues](https://github.com/yourrepo/issues)
- 💬 Questions: [GitHub Discussions](https://github.com/yourrepo/discussions)

---

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Amazing Python web framework
- [SQLAlchemy](https://www.sqlalchemy.org/) - The Python SQL toolkit
- [Pydantic](https://docs.pydantic.dev/) - Data validation using Python type hints
- [Uvicorn](https://www.uvicorn.org/) - Lightning-fast ASGI server

---

**Made with ❤️ using FastAPI**
