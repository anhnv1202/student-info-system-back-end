# Student Management System - Backend API

A FastAPI-based REST API for managing student information with SQLite database.

## Features

- **CRUD Operations**: Create, Read, Update, Delete students
- **Search & Filter**: Search students by code, name, email, hometown
- **Pagination**: Efficient data pagination
- **Bulk Operations**: Bulk create multiple students
- **Data Validation**: Pydantic schemas for data validation
- **Auto Documentation**: Swagger UI and ReDoc
- **CORS Support**: Configured for frontend integration
- **Sample Data**: Script to generate 100 sample students with missing data

## Technology Stack

- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: SQL toolkit and ORM
- **SQLite**: Lightweight database
- **Pydantic**: Data validation
- **Pandas**: Data preprocessing and analysis
- **Faker**: Generate realistic sample data
- **Uvicorn**: ASGI server

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI application
│   ├── database.py       # Database connection
│   ├── models.py         # SQLAlchemy models
│   ├── schemas.py        # Pydantic schemas
│   ├── crud.py           # CRUD operations
│   └── routes.py         # API routes
├── scripts/
│   ├── __init__.py
│   └── generate_sample_data.py  # Generate sample data
├── requirements.txt      # Python dependencies
├── run.py               # Application runner
├── .env                 # Environment variables
├── .gitignore          # Git ignore file
└── README.md           # This file
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create virtual environment** (recommended):
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment variables**:
   The `.env` file is already configured with default values:
   ```
   DATABASE_URL=sqlite:///./students.db
   API_HOST=0.0.0.0
   API_PORT=8000
   ```

## Usage

### Run the API Server

```bash
python run.py
```

The API will be available at: `http://localhost:8000`

### Generate Sample Data

Generate 100 sample students with some missing data:

```bash
python scripts/generate_sample_data.py
```

This will:
- Create 100 students with realistic Vietnamese data
- Include some missing data (5-15% per field)
- Display statistics using pandas
- Export data to `students_data.csv`

## API Documentation

### Interactive Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### API Endpoints

#### Students

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/students/` | Get all students (with pagination & search) |
| POST | `/api/students/` | Create a new student |
| GET | `/api/students/{id}` | Get student by ID |
| PUT | `/api/students/{id}` | Update student |
| DELETE | `/api/students/{id}` | Delete student |
| POST | `/api/students/bulk` | Bulk create students |

#### System

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information |
| GET | `/health` | Health check |

### Example Requests

#### Create a Student

```bash
curl -X POST "http://localhost:8000/api/students/" \
  -H "Content-Type: application/json" \
  -d '{
    "student_code": "SV20240001",
    "first_name": "Minh",
    "last_name": "Nguyen",
    "email": "minh.nguyen@student.edu.vn",
    "date_of_birth": "2002-05-15",
    "hometown": "Hà Nội",
    "math_score": 8.5,
    "literature_score": 7.5,
    "english_score": 9.0
  }'
```

#### Get All Students

```bash
curl "http://localhost:8000/api/students/?skip=0&limit=10"
```

#### Search Students

```bash
curl "http://localhost:8000/api/students/?search=Nguyen"
```

#### Update Student

```bash
curl -X PUT "http://localhost:8000/api/students/1" \
  -H "Content-Type: application/json" \
  -d '{
    "math_score": 9.0
  }'
```

#### Delete Student

```bash
curl -X DELETE "http://localhost:8000/api/students/1"
```

## Data Model

### Student

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | Integer | Auto | Primary key |
| student_code | String | Yes | Unique student code |
| first_name | String | No | Student's first name |
| last_name | String | No | Student's last name |
| email | String | No | Student's email |
| date_of_birth | Date | No | Date of birth |
| hometown | String | No | Student's hometown |
| math_score | Float (0-10) | No | Math score |
| literature_score | Float (0-10) | No | Literature score |
| english_score | Float (0-10) | No | English score |

## Database

- **Type**: SQLite
- **File**: `students.db` (created automatically)
- **ORM**: SQLAlchemy
- **Migrations**: Auto-created on startup

## Development

### Run in Development Mode

```bash
python run.py
```

The server will auto-reload on code changes.

### View Database

You can use any SQLite client to view the database:
- [DB Browser for SQLite](https://sqlitebrowser.org/)
- VS Code SQLite extension
- Command line: `sqlite3 students.db`

### Reset Database

Delete the `students.db` file and restart the server:

```bash
# Windows
del students.db

# Linux/Mac
rm students.db

python run.py
```

## Testing with Sample Data

1. **Generate sample data**:
   ```bash
   python scripts/generate_sample_data.py
   ```

2. **View the data**:
   - API: http://localhost:8000/api/students/
   - Swagger UI: http://localhost:8000/docs
   - CSV file: `students_data.csv`

3. **Statistics**:
   The generation script shows:
   - Total students created
   - Missing data count per field
   - Score statistics (mean, std, min, max)
   - Sample data preview

## CORS Configuration

CORS is configured to allow all origins for development. For production, update in `app/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Error Handling

The API returns appropriate HTTP status codes:

- `200`: Success
- `201`: Created
- `400`: Bad Request (validation error, duplicate)
- `404`: Not Found
- `422`: Validation Error
- `500`: Internal Server Error

## Future Enhancements

- [ ] User authentication & authorization
- [ ] File upload (student photos)
- [ ] Export data to Excel/PDF
- [ ] Advanced filtering & sorting
- [ ] Data analytics dashboard
- [ ] Email notifications
- [ ] Audit logging

## License

MIT License

## Contact

For questions or support, please contact the development team.


