# 🛡️ ByteShield Gateway Backend

> A Security-Focused API Gateway built with Django REST Framework, Redis, JWT Authentication, and Real-Time Traffic Analytics.

[![Live Frontend Dashboard](https://img.shields.io/badge/Live-Dashboard-blue?style=for-the-badge&logo=vercel)](https://byteshield-dashboard-frontend.vercel.app/)
[![Backend API Live](https://img.shields.io/badge/Render-Live_API-E57373?style=for-the-badge&logo=render&logoColor=white)](https://byteshield-gateway-backend.onrender.com)

![Python](https://img.shields.io/badge/Python-3.13+-blue?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-6.0+-green?logo=django&logoColor=white)
![Django REST Framework](https://img.shields.io/badge/DRF-3.15+-red?logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16+-blue?logo=postgresql&logoColor=white)
![Supabase](https://img.shields.io/badge/Supabase-Database-green?logo=supabase&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-Cache-critical?logo=redis&logoColor=white)
![Render](https://img.shields.io/badge/Render-Deployment-black?logo=render&logoColor=white)
![JWT](https://img.shields.io/badge/Auth-JWT-orange)

---

# 📌 Overview

**ByteShield Gateway Backend** is a high-performance API Gateway and Security Layer designed to protect backend services from unauthorized access, abuse, and excessive traffic.

The system combines:

- 🔐 JWT Authentication
- 🔑 Secure API Key Management
- ⚡ Redis-Based Rate Limiting
- 🛡️ Custom Gateway Middleware
- 📊 Real-Time Analytics & Monitoring
- 🚫 IP Blacklisting

It acts as a centralized security layer between client applications and protected backend services.

---

# ✨ Key Features

## 🔐 Authentication & Access Control

### JWT Authentication
- Secure login and signup system
- Short-lived Access Tokens
- Refresh Token mechanism
- Protected API routes

### API Key Management
- Generate API Keys
- Activate / Deactivate Keys
- Delete Keys
- User-specific ownership

### Secure Key Storage
API keys are never stored in plain text.

Before saving:

```python
SHA3-256(API_KEY)
```

is generated and stored inside the database.

Even database administrators cannot recover original keys.

---

## 🛡️ Gateway Security Layer

### Custom Middleware Engine

Every incoming request passes through a security middleware that:

- Validates API Keys
- Checks Rate Limits
- Tracks Request Metrics
- Blocks Blacklisted Clients

before reaching application logic.

### IP Blacklisting

Malicious or abusive clients can be instantly blocked.

Blocked IPs are rejected before consuming backend resources.

### Redis Rate Limiting

Uses Redis for ultra-fast request counting.

Current policy:

```text
5 Requests / Minute
```

per client.

This helps mitigate:

- Spam
- Bot Traffic
- Basic DDoS Attempts
- API Abuse

---

## 📊 Traffic Analytics

ByteShield continuously collects telemetry information.

Tracked Metrics:

- Total Requests
- Response Time
- Status Codes
- Endpoint Activity
- User Traffic Patterns

Dashboard Analytics include:

- Request Count
- Average Response Time
- Status Distribution
- Historical Activity Graphs

Example:

```text
200 → 1245 Requests
401 → 52 Requests
429 → 16 Requests
500 → 3 Requests
```

---

# 🏗️ System Architecture

```text
Frontend Dashboard
        │
        ▼
ByteShield Gateway
        │
 ┌──────┼──────┐
 ▼      ▼      ▼
JWT   Redis   PostgreSQL
Auth  Cache   Database
```

---

# 🛠️ Technology Stack

| Category | Technology |
|-----------|------------|
| Language | Python 3.13+ |
| Framework | Django |
| API Framework | Django REST Framework |
| Authentication | SimpleJWT |
| Cache | Redis |
| Database | PostgreSQL (Supabase)|
| Hashing | SHA3-256 |
| Deployment | Render |
| Version Control | Git & GitHub |

---

# 📂 Project Structure

```text
ByteShield/
│
├── api/
│   ├── middleware.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
│
├── ByteShield/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── manage.py
├── requirements.txt
└── README.md
```

---

# 🚀 API Endpoints

## 🔑 Authentication

| Method | Endpoint | Description |
|----------|-----------|-------------|
| POST | `/api/v1/auth/signup/` | Register User |
| POST | `/api/v1/auth/login/` | Login User |
| POST | `/api/v1/auth/token/refresh/` | Refresh Access Token |

---

## 🛠️ API Key Management

| Method | Endpoint |
|----------|----------|
| POST | `/api/v1/api-keys/` |
| GET | `/api/v1/api_key/all/` |
| PATCH | `/api/v1/api_key/inactive/` |
| DELETE | `/api/v1/api_key/delete/` |

---

## 📊 Dashboard Analytics

| Method | Endpoint |
|----------|----------|
| GET | `/api/v1/user/profile/` |
| GET | `/api/v1/dashboard/metrics/` |
| GET | `/api/v1/dashboard/charts/` |

---

## 🛡️ Gateway Verification

| Method | Endpoint | Required Header
|----------|----------|
| POST | `/api/v1/shield/verify/` | X-ByteShield-Key: bsk_live_xxxx

Requires:

```http
X-ByteShield-Key: bsk_live_xxxxxxxxx
```

---

# 🔄 Request Lifecycle

### 1. User Authentication

```text
Signup → Login → JWT Issued
```

### 2. API Key Creation

```text
Generate Key
       │
       ▼
Display Once
       │
       ▼
Store SHA3-256 Hash
```

### 3. Gateway Request

```http
POST /api/v1/shield/verify/

X-ByteShield-Key: bsk_live_xxxxxxxxx
```

### 4. Middleware Validation

Checks:

✔ API Key

✔ Active Status

✔ Rate Limit

✔ Blacklist

✔ Logging

### 5. Analytics Update

Metrics instantly become available on dashboard endpoints.

---
## 🔒 Environment Variables Configuration

Before running the server, create a `.env` file in the root directory and add the following configuration variables (refer to `.env.example` if available):

```text
SECRET_KEY=your_django_secret_key
DEBUG=False
DB_NAME=your_supabase_db_name
DB_USER=your_supabase_db_user
DB_PASSWORD=your_supabase_db_password
DB_HOST=your_supabase_db_host
DB_PORT=5432
REDIS_URL=your_redis_cloud_or_local_url
```

# 📦 Local Installation

## Clone Repository

```bash
git clone https://github.com/karan-bairagi/byteshield-gateway-backend
cd byteshield-gateway-backend
```

## Create Virtual Environment

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Start Redis

```bash
redis-server
```

---

## Run Migrations

```bash
python manage.py migrate
```

---

## Start Development Server

```bash
python manage.py runserver
```

Application will be available at:

```text
http://127.0.0.1:8000/
```

---

# 📈 Future Enhancements

### Multi-Tenant Gateway

Support multiple organizations using isolated API infrastructures.

### Geo Analytics

Traffic heatmaps by country and region.

### Threat Detection Engine

Detection for:

- SQL Injection
- XSS Attempts
- Suspicious Payloads
- Credential Stuffing

### Tier-Based Rate Limiting

```text
Free Plan      → 5 RPM
Pro Plan       → 100 RPM
Enterprise     → Custom
```

---

# 👨‍💻 Author

**Karan Bairagi**
- Backend Architecture & Database Optimization
- API Security Engineering & Middleware Pipelines
- Django REST Framework Deployment
- Redis Memory Layer Caching

---
---

## 🚀 Project Component Links
- **🖥️ Frontend Repository:** [https://github.com/karan-bairagi/byteshield-dashboard-frontend](https://github.com/karan-bairagi/byteshield-dashboard-frontend)
- **🎨 Live Frontend Dashboard:** [https://byteshield-dashboard-frontend.vercel.app/](https://byteshield-dashboard-frontend.vercel.app/)

---

## 🌐 Connect With Me

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/karan-bairagi/)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/karan-bairagi)
[![Render Live API](https://img.shields.io/badge/Render-Live_API-E57373?style=for-the-badge&logo=render&logoColor=white)](https://byteshield-gateway-backend.onrender.com)

---

## ⭐ Support
If you found this project useful, consider giving it a **Star ⭐** on GitHub.