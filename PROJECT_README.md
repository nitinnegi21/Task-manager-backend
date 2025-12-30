# Task Manager - Complete Project Submission

**Submitted by**: Nitin Singh
**Position**: Python Developer  
**Company**: Pelocal Fintech Pvt. Ltd.

## Project Overview

This is a complete Task Management application with RESTful APIs built using Flask and MongoDB, with a React-based frontend interface.

## Repository Links

- **Backend Repository**: https://github.com/nitinnegi21/Task-manager-backend
- **Frontend Repository**: https://github.com/nitinnegi21/Task-manager

## Technology Stack

### Backend
- Python 3.8+
- Flask (Web Framework)
- MongoDB (Database)
- PyMongo (Database Driver)
- Flask-CORS (Cross-origin support)

### Frontend
- React 18
- Tailwind CSS
- Axios
- Lucide React (Icons)

## Features Implemented

✅ Complete CRUD operations for tasks  
✅ RESTful API design  
✅ Database integration with MongoDB  
✅ Input validation and error handling  
✅ Comprehensive logging system  
✅ Exception handling at all levels  
✅ API documentation  
✅ Unit tests for API endpoints  
✅ Responsive web interface  
✅ Task filtering and statistics  

## Project Structure

### Backend Structure
```
task-management-backend/
├── app.py                  # Main application
├── config.py              # Configuration
├── database.py            # Database connection
├── models/                # Data models
├── routes/                # API endpoints
├── utils/                 # Utilities
├── tests/                 # Test cases
├── logs/                  # Application logs
└── README.md             # Setup instructions
```

### Frontend Structure
```
Task-management/
├── src/
│   ├── components/       # React components
│   └── utility/          # API service layer
└── README.md            # Setup instructions
```

## Quick Setup Guide

### Backend Setup

1. Clone the repository:
```bash
git clone https://github.com/nitinnegi21/Task-manager-backend.git
cd Task-manager-backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment:
```bash
cp .env.example .env
# Edit .env with your MongoDB connection string
```

5. Run the application:
```bash
python app.py
```

Backend will run on: `http://localhost:5000`

### Frontend Setup

1. Clone the repository:
```bash
git clone https://github.com/nitinnegi21/Task-manager.git
cd Task-manager
```

2. Install dependencies:
```bash
npm install
```

3. Configure environment:
```bash
# Create .env file with:
REACT_APP_API_BASE_URL=http://localhost:5000/api
```

4. Run the application:
```bash
npm start
```

Frontend will run on: `http://localhost:3000`

## API Documentation

### Base URL
```
http://localhost:5000/api
```

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/tasks` | Get all tasks |
| GET | `/tasks/<id>` | Get specific task |
| POST | `/tasks` | Create new task |
| PUT | `/tasks/<id>` | Update task |
| DELETE | `/tasks/<id>` | Delete task |
| PATCH | `/tasks/<id>/toggle` | Toggle completion |
| GET | `/tasks/stats` | Get statistics |

### Sample Request/Response

**Create Task:**
```json
POST /api/tasks
{
  "title": "Complete assignment",
  "description": "Submit by Wednesday",
  "priority": "high",
  "due_date": "2025-12-31T23:59:59"
}
```

**Response:**
```json
{
  "success": true,
  "status_code": 201,
  "message": "Task created successfully",
  "data": {
    "id": "...",
    "title": "Complete assignment",
    "completed": false,
    "priority": "high",
    "created_at": "2025-12-26T10:30:00"
  }
}
```

## Testing

Run the test suite:
```bash
cd task-management-backend
pytest -v
pytest --cov=. --cov-report=html
```

## Key Implementation Details

### 1. Logging
- Implemented comprehensive logging using Python's logging module
- Logs stored in `logs/app.log` with rotation
- Different log levels for different scenarios

### 2. Exception Handling
- Global exception handlers for all routes
- Specific error handling for validation, database, and API errors
- Standardized error response format

### 3. Database
- MongoDB used instead of SQLite for better scalability
- Proper indexing for performance
- Connection pooling implemented

### 4. Code Organization
- Modular architecture with separation of concerns
- Models, Routes, and Utils in separate modules
- Clean code principles followed

### 5. API Design
- RESTful principles followed
- Consistent response format
- Proper HTTP status codes

## Additional Features

- Task filtering by status and priority
- Pagination support
- Task statistics dashboard
- Real-time updates
- Responsive UI design
- Loading states and error handling

## Notes

- Did not use Django ORM as per requirement
- Implemented raw database queries using PyMongo
- All CRUD operations working as expected
- Tests cover all major endpoints
- Documentation is comprehensive

## Contact

For any questions or clarifications:
- Email: nitinnegi71741@gmail.com
- GitHub: https://github.com/nitinnegi21

---

**Submission Date**: 30th December 2025