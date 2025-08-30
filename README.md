# 🛡️ Secure Timed Exam Access Link API

A Django REST Framework-based secure exam access system that provides time-bound, one-time-use access links for online exams with robust security features and academic integrity protection.


## 📖 Project Overview

This edtech platform provides a secure system for generating time-bound, cryptographically secure access tokens for online exams. The system ensures academic integrity by preventing unauthorized access, token reuse, and token sharing among students.

### How It Works:
1. **Instructors** (staff users) generate secure access tokens for specific students and exams
2. **Students** use these tokens to access their assigned exams
3. **Tokens** are single-use, time-limited, and cryptographically secure
4. **Email notifications** are sent automatically with exam access links (via Celery)

## ✨ Key Features

- **Secure Token Generation**: Cryptographically secure tokens using Python's `secrets` module
- **Time-Bound Access**: Configurable token validity periods
- **Single-Use Tokens**: Prevents token reuse and sharing
- **Academic Integrity**: Prevents unauthorized access and cheating
- **Email Notifications**: Automatic email delivery of exam links
- **Admin Panel**: Django admin interface for token management
- **Rate Limiting**: Protection against brute-force attacks
- **Comprehensive Logging**: Detailed logging for debugging and monitoring

## 🛠️ Technology Stack

- **Backend Framework**: Django 5.2.5 + Django REST Framework
- **Database**: SQLite (development)
- **Authentication**: JWT (Simple JWT)
- **Task Queue**: Celery + Redis
- **Email**: SMTP (Gmail)
- **Security**: Python secrets module for token generation


## 🚀 Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/Oyshik-ICT/secure-exam-access.git

cd secure-exam-access
```

### 2. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Generate Django Secret Key
First, generate a new secret key by running this command **in your terminal/command prompt**:
```bash
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 5. Environment Setup
Create a `.env` file in the `exam_system/` directory:
```env
SECRET_KEY='your-generated-secret-key-here'
DEBUG=True

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com
```

### 6. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create Superuser
```bash
python manage.py createsuperuser
```

### 8. Start Redis Server
```bash
# Install Redis first, then:
redis-server
```

### 9. Start Celery Worker
```bash
celery -A exam_system worker -l info
```

### 10. Run Development Server
```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`

## 🔗 API Endpoints

### Authentication Endpoints

| Method | Endpoint | Description | Authentication Required |
|--------|----------|-------------|------------------------|
| POST | `/api/register/` | Register new user | No |
| POST | `/api/login/` | Login and get JWT token | No |
| POST | `/api/login/refresh/` | Refresh JWT token | No |
| GET/PUT/PATCH | `/api/user/` | User profile management | Yes (JWT) |

### Exam Access Endpoints

| Method | Endpoint | Description | Authentication Required |
|--------|----------|-------------|------------------------|
| POST | `/api/exams/<exam_id>/generate-token/` | Generate exam access token | Yes (Staff only) |
| GET | `/api/exams/access/<token>/` | Access exam using token | No (Public) |

## 📝 API Usage Examples

---

## 🚨 **IMPORTANT: COMPLETE API TESTING COLLECTION AVAILABLE**

### **🎯 CLICK HERE FOR INSTANT API TESTING** 
**👆 Complete API documentation and testing examples are available in my public Postman workspace:**

# **🔗 [EXAM SYSTEM API - POSTMAN COLLECTION - CLICK HERE](https://www.postman.com/joint-operations-candidate-78622090/workspace/exam-system-api/collection/37564257-6a9fc56d-943a-4ec5-8a4f-9c50a4bc8d59?action=share&creator=37564257)**

**📋 Copy this link if clicking doesn't work:**
```
https://www.postman.com/joint-operations-candidate-78622090/workspace/exam-system-api/collection/37564257-6a9fc56d-943a-4ec5-8a4f-9c50a4bc8d59?action=share&creator=37564257
```

### **🎁 What's Included in the Postman Collection:**
- ✅ **Pre-configured requests** for ALL endpoints
- ✅ **Example responses** for success and error cases
- ✅ **Ready-to-test** examples with sample data

---

### Authentication Examples

#### Register User
```http
POST /api/register/
Content-Type: application/json

{
    "username": "student1",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "password": "securepassword123"
}
```

#### Login (Get JWT Token)
```http
POST /api/login/
Content-Type: application/json

{
    "username": "admin",
    "password": "adminpassword"
}
```

**Response:**
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Exam Token Management

#### Generate Token (Staff Only)
```http
POST /api/exams/1/generate-token/
Authorization: Bearer <access-token>
Content-Type: application/json

{
    "student_id": 2,
    "valid_minutes": 30
}
```

**Success Response (201):**
```json
{
    "token": "kL8mN9pQ2rS3tU4vW5xY6zA7bC8dE9fG",
    "message": "Token generated successfully"
}
```

#### Access Exam (Public)
```http
GET /api/exams/access/kL8mN9pQ2rS3tU4vW5xY6zA7bC8dE9fG/
```

**Success Response (200):**
```json
{
    "exam": {
        "title": "Final Python Exam",
        "start_time": "2025-08-30T10:00:00Z",
        "end_time": "2025-08-30T11:30:00Z"
    },
    "student": {
        "name": "John Doe",
        "email": "john@example.com"
    }
}
```

## ✅ Validation Rules

### Token Generation Validations
| Validation | Description | Error Response |
|------------|-------------|----------------|
| **Instructor Permission** | Only staff users can generate tokens | `403 Forbidden: "Unauthorized"` |
| **Valid Exam ID** | Exam must exist in database | `400 Bad Request: "Invalid exam"` |
| **Valid Student ID** | Student must exist in database | `400 Bad Request: "Invalid student"` |
| **Exam Not Ended** | Cannot generate token for past exams | `400 Bad Request: "Exam is already Ended"` |
| **Token Validity** | Token validity cannot exceed exam end time | `400 Bad Request: "Token valid minute must not exceed exam end time"` |
| **Duplicate Prevention** | One token per student per exam | `400 Bad Request: "Token already exists for this student and exam"` |
| **Positive Duration** | valid_minutes must be > 0 | `400 Bad Request: "Ensure this value is greater than or equal to 1"` |

### Token Access Validations
| Validation | Description | Error Response |
|------------|-------------|----------------|
| **Token Existence** | Token must exist in database | `404 Not Found: "Token doesn't exist"` |
| **Token Not Used** | Token must not be previously consumed | `400 Bad Request: "Token is already used"` |
| **Token Not Expired** | Current time must be within validity window | `410 Gone: "Token is expired"` |
| **Atomic Operation** | Token marking as used is atomic | Prevents race conditions |

## 🔐 Security Features

### Token Security
- **Cryptographically Secure**: Uses Python's `secrets.token_urlsafe(16)` for unpredictable tokens
- **Unique Tokens**: Database-level uniqueness constraint prevents collisions
- **Single-Use**: Tokens are invalidated after first use
- **Time-Bound**: Configurable expiration times

### API Security
- **JWT Authentication**: Secure authentication for protected endpoints
- **Role-Based Access**: Instructor-only token generation
- **Rate Limiting**: 200 requests per day for anonymous users on validation endpoint
- **Input Validation**: Comprehensive request validation using DRF serializers

### Data Integrity
- **Atomic Transactions**: Token validation uses database transactions
- **Unique Constraints**: Prevents duplicate tokens for same student-exam pairs
- **Timezone Awareness**: All datetime operations are timezone-aware

## 🎉 Bonus Features Implemented

### ✅ Email Notification System
- **Asynchronous Email Delivery**: Uses Celery for non-blocking email sending
- **Automatic Link Generation**: Students receive ready-to-use exam access links
- **Email Configuration**: Supports SMTP with Gmail integration

### ✅ Django Admin Panel
- **Exam Management**: Full CRUD operations with datetime widgets
- **Token Administration**: View and manage tokens with advanced filtering
- **Search & Filter**: Filter tokens by usage status, expiration, and exam

### ✅ Advanced Logging
- **Comprehensive Logging**: Detailed logs for debugging and monitoring
- **Error Tracking**: Exception logging with stack traces
- **Audit Trail**: Token generation and usage tracking

### ✅ Rate Limiting
- **Brute-Force Protection**: Anonymous rate limiting on token validation endpoint
- **Configurable Limits**: 200 requests per day for anonymous users

### ✅ Service Layer Architecture
- **Business Logic Separation**: Clean separation between views and business logic
- **Reusable Components**: Service methods can be used across different views
- **Testable Code**: Easy unit testing of business logic

## 🔄 Celery Integration

### How Celery Works in This Project:

1. **Setup**: Celery is configured to use Redis as message broker
2. **Task Definition**: Email sending is defined as a Celery task in `tasks.py`
3. **Asynchronous Execution**: When token is generated, email task is queued
4. **Worker Process**: Celery worker processes email tasks in background
5. **Timezone Support**: Configured for Asia/Dhaka timezone

### Celery Configuration:
```python
# Broker: Redis on localhost:6379/1
# Result Backend: Django database
# Timezone: Asia/Dhaka
# Serialization: JSON
```

### Email Task Flow:
```
Token Generated → Email Task Queued → Celery Worker → Email Sent → Student Receives Link
```


## 🎯 Core Workflow

### Token Generation Process:
1. Instructor logs in and gets JWT token
2. Instructor creates exam in Django admin
3. Instructor calls generate-token API with student_id and validity duration
4. System validates inputs and generates secure token
5. Token is saved to database with time constraints
6. Email with access link is sent asynchronously via Celery
7. Student receives email with exam access link

### Token Validation Process:
1. Student clicks email link or accesses token URL directly
2. System validates token existence, usage status, and expiration
3. If valid, token is marked as used (single-use enforcement)
4. Exam details and student info are returned
5. Student can proceed to take the exam

## 🔍 Error Handling

The system provides comprehensive error handling with specific HTTP status codes:

- **400 Bad Request**: Invalid input data, duplicate tokens, exam/student not found
- **401 Unauthorized**: Missing or invalid JWT token
- **403 Forbidden**: Insufficient permissions (non-staff trying to generate tokens)
- **404 Not Found**: Token doesn't exist
- **410 Gone**: Token expired
- **500 Internal Server Error**: Unexpected server errors



## ⚙️ Configuration Details

### Environment Variables Required:
```env
SECRET_KEY=your-secret-key
DEBUG=True/False
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com
```

### Celery Configuration:
- **Broker URL**: `redis://127.0.0.1:6379/1`
- **Result Backend**: Django database
- **Timezone**: Asia/Dhaka
- **Serialization**: JSON format

## 🤔 Assumptions Made During Implementation

### 1. **User Roles**
- Assumed `User.is_staff=True` represents instructors/admins
- Regular users (students) have `is_staff=False`

### 2. **Exam Creation**
- Exams are created through Django admin panel by staff
- No API endpoint for exam creation (focused on token management)

### 3. **Email Configuration**
- Gmail SMTP is used for email delivery
- App passwords are required for Gmail authentication

### 4. **Token Security**
- 16-byte URL-safe tokens provide sufficient security (128 bits of entropy)
- Single-use policy is strictly enforced

### 5. **Timezone Handling**
- All datetime operations use Asia/Dhaka timezone
- `USE_TZ = False` for simplified timezone handling

### 6. **Rate Limiting**
- 200 requests per day is reasonable for exam access validation
- Only anonymous requests are rate-limited (students accessing tokens)

### 7. **Database**
- SQLite is sufficient for development and testing
- Production would require PostgreSQL or MySQL

### 8. **Error Responses**
- Specific error messages help with debugging while maintaining security
- No sensitive information exposed in error responses

## 🏃‍♂️ Running the Complete System

### Terminal 1: Start Redis
```bash
redis-server
```

### Terminal 2: Start Celery Worker
```bash
cd secure-exam-access
source venv/bin/activate
celery -A exam_system worker -l info
```

### Terminal 3: Start Django Server
```bash
cd exam_system
source venv/bin/activate
python manage.py runserver
```


## 🔧 Development Notes

### Code Quality
- **PEP 8 Compliance**: All code follows Python style guidelines
- **Django Patterns**: Proper use of models, views, serializers pattern
- **Exception Handling**: Custom exceptions with proper error propagation
- **Logging**: Comprehensive logging for debugging and monitoring

### Performance Considerations
- **Database Queries**: Optimized with `select_related` for foreign keys
- **Atomic Transactions**: Prevents race conditions in token validation
- **Asynchronous Tasks**: Email sending doesn't block API responses

### Scalability Features
- **Service Layer**: Business logic separated for easy testing and maintenance
- **Celery Integration**: Ready for distributed task processing
- **Rate Limiting**: Built-in protection against abuse


## 🎯 Key Learning Outcomes

This project demonstrates:
- **Secure API Development**: JWT authentication, secure token generation
- **Asynchronous Processing**: Celery task queue implementation
- **Django Best Practices**: Service layer, proper model design, admin customization
- **Security Principles**: Rate limiting, input validation, atomic operations
- **Real-World Application**: Academic integrity and exam management

---

**📧 For questions or clarifications, please refer to the code comments or check the Postman collection for detailed API examples.**