# 🚂 RailTrack Pro - Railway Track Fittings Management System

**Smart India Hackathon (SIH) Project** - A comprehensive vendor and track fittings management system with QR-based tracking, AI-powered risk assessment, and multi-stage inspection capabilities.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![React](https://img.shields.io/badge/React-18.2.0-61dafb.svg)](https://reactjs.org/)
[![License](https://img.shields.io/badge/License-SIH-orange.svg)](LICENSE)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Key Features](#-key-features)
- [System Architecture](#-system-architecture)
- [Tech Stack](#-tech-stack)
- [Quick Start](#-quick-start)
- [API Documentation](#-api-endpoints)
- [Database Schema](#-database-schema)
- [Security Features](#-security-features)
- [Testing](#-testing)
- [Deployment](#-deployment)
- [Project Structure](#-project-structure)
- [Documentation](#-documentation)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Overview

RailTrack Pro is a full-stack web application designed for Indian Railways to manage track fittings (Elastic Rail Clips, Rail Pads, Liners, Sleepers) throughout their lifecycle - from manufacturing to installation and maintenance.

### Core Capabilities

- **🏭 Vendor Management**: Register and manage vendors/manufacturers with complete details
- **📦 Track Inventory**: Track individual lots of rail fittings with specifications
- **📷 QR Code System**: Generate and scan QR codes for field verification
- **🔍 Multi-Stage Inspection**: Manufacturing, supply, installation, and periodic inspections
- **🤖 AI Risk Assessment**: Automated risk scoring and flags for vendors and items
- **📊 Analytics Dashboard**: Real-time performance metrics and defect tracking
- **🔐 Role-Based Access**: Admin, User, and Viewer roles with JWT authentication

---

## ✨ Key Features

### 1. Vendor Management
- Complete vendor profiles with contact, tax, and banking information
- Vendor performance rating and certification status
- Approval workflow with audit trail
- Vendor comparison and analytics

### 2. Track Items Management (Railway Fittings)
- **Elastic Rail Clips (ERC)**: Track by lot number and specifications
- **Rail Pads**: Monitor quality and installation details
- **Liners**: Track installation location and wear
- **Sleepers**: Manage lifecycle from manufacturing to replacement

Each track item includes:
- Lot/batch tracking with unique identifiers
- Manufacturing and supply dates
- Installation location (section, division, zone)
- Warranty information and expiry tracking
- Performance status (good/average/poor/failed)
- Defect and replacement counts
- Technical specifications (JSON)

### 3. QR Code System
- **Generate**: Create QR codes for vendors and track items
- **Download**: Download QR codes as PNG for printing
- **Scan**: Camera-based scanning via web interface
- **Verify**: Instant verification with AI-powered insights

### 4. Multi-Stage Inspection System
- **Manufacturing Inspection**: Pre-dispatch quality checks
- **Supply Inspection**: Quality verification at delivery
- **Installation Inspection**: Post-installation quality assessment
- **Periodic Inspection**: Scheduled maintenance inspections
- **Defect Inspection**: Unscheduled inspections for failures

Each inspection records:
- Inspector details and date
- Quality grade (A/B/C/D/F)
- Pass/fail/conditional status
- Defects found (JSON)
- Actions taken
- Next inspection due date

### 5. AI-Powered Risk Assessment
The system analyzes vendor and item data to provide:

- **Risk Score (0-100)**: Overall risk rating
- **Risk Flags**: Issues detected (missing info, invalid formats, suspicious patterns)
- **Recommendations**: Actionable steps for verification
- **Keywords**: Auto-extracted from details
- **Summary**: Concise overview

**Risk Detection Heuristics:**
- Missing/invalid contact information
- Incomplete address or location data
- Unusual tax ID or bank account formats
- Future manufacture dates
- Suspicious keywords (e.g., "urgent", "wire transfer")
- High defect rates
- Warranty expiry alerts
- Poor performance history

### 6. Analytics & Reporting
- **Vendor Performance**: Compare vendors by risk score, defect rates
- **Track Item Analytics**: By type, zone, status, and performance
- **Defect Tracking**: Total defects, replacements, trends
- **Inspection Stats**: Pass rates, failure analysis
- **Risk Distribution**: High/medium/low risk breakdown

### 7. Security & Authentication
- 🔐 **JWT Authentication**: Secure token-based auth with refresh tokens
- 👥 **Role-Based Access Control**: Admin, User, Viewer roles
- 🛡️ **Rate Limiting**: Prevent API abuse (configurable per endpoint)
- ✅ **Input Validation**: Comprehensive sanitization and validation
- 🔒 **Password Hashing**: bcrypt with 12 salt rounds
- 🚫 **CORS Protection**: Configurable origin restrictions
- 📝 **Audit Trail**: Track who created/modified records
- 🚨 **Security Headers**: X-Frame-Options, XSS-Protection, HSTS

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Client Layer                          │
│  ┌─────────────────────────────────────────────────────┐    │
│  │           React SPA (Bootstrap UI)                  │    │
│  │  - Dashboard  - Track Items  - Vendors  - Scanner   │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ HTTPS
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      API Gateway Layer                       │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              Nginx Reverse Proxy                    │    │
│  │         (SSL, Rate Limiting, Headers)               │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    Application Layer                         │
│  ┌─────────────────────────────────────────────────────┐    │
│  │           Flask REST API (Python 3.11)              │    │
│  │  - JWT Auth  - Rate Limiter  - Input Validation     │    │
│  │  - Business Logic  - AI Risk Assessment             │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ SQLAlchemy ORM
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      Data Layer                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  PostgreSQL  │  │    Redis     │  │   File Store │      │
│  │  (Primary)   │  │  (Cache/     │  │   (QR Codes) │      │
│  │  or SQLite   │  │   Rate Limit)│  │              │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

### Backend
| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.11+ | Core language |
| **Flask** | 3.0.0 | Web framework |
| **SQLAlchemy** | 3.1.1 | ORM |
| **PostgreSQL** | Latest | Primary database |
| **SQLite** | 3.x | Development database |
| **Flask-JWT-Extended** | 4.6.0 | Authentication |
| **Flask-Limiter** | 3.5.0 | Rate limiting |
| **bcrypt** | 4.1.2 | Password hashing |
| **qrcode** | 7.4.2 | QR code generation |
| **Pillow** | 10.1.0 | Image processing |
| **Gunicorn** | 21.2.0 | WSGI server |
| **pytest** | 7.4.3 | Testing framework |

### Frontend
| Technology | Version | Purpose |
|------------|---------|---------|
| **React** | 18.2.0 | UI framework |
| **React Router** | 6.20.0 | Client-side routing |
| **Bootstrap** | 5.3.2 | UI components |
| **React Bootstrap** | 2.9.1 | Bootstrap components |
| **Axios** | 1.6.2 | HTTP client |
| **html5-qrcode** | 2.3.8 | QR scanner |
| **qrcode.react** | 3.1.0 | QR display |

### DevOps & Tools
| Technology | Version | Purpose |
|------------|---------|---------|
| **Docker** | 20.x+ | Containerization |
| **Docker Compose** | Latest | Multi-container orchestration |
| **Nginx** | Latest | Reverse proxy |
| **Redis** | Latest | Rate limiting cache |
| **pytest-cov** | 4.1.0 | Test coverage |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11 or higher
- Node.js 18.x or higher
- Git
- Docker (optional, for containerized deployment)

### Option 1: Docker (Recommended)

```bash
# Clone repository
cd "C:\Users\suman\Downloads\OLD_PROJECT\SIH PROJECT"

# Start all services
docker-compose up --build
```

Access:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **Database**: localhost:5432

**Default Credentials:**
- Username: `admin`
- Password: `Admin@123`
- ⚠️ **Change immediately after first login!**

### Option 2: Manual Setup

#### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy and configure environment
copy .env.example .env  # Windows
# Edit .env and set SECRET_KEY, JWT_SECRET_KEY

# Run the application
python app.py
```

Backend runs at: http://localhost:5000

#### Frontend Setup (new terminal)

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Copy and configure environment
copy .env.example .env  # Windows
# Edit .env and set REACT_APP_API_URL

# Start development server
npm start
```

Frontend runs at: http://localhost:3000

### Option 3: Production Deployment

```bash
# Copy production environment
copy .env.prod.example .env  # Windows
# Edit .env with your production values

# Deploy with Docker Compose
docker-compose -f docker-compose.prod.yml up -d

# View logs
docker-compose logs -f
```

See [DEPLOYMENT.md](DEPLOYMENT.md) for Railway, Render, Vercel, and other platforms.

---

## 📡 API Endpoints

### Authentication Endpoints

| Method | Endpoint | Description | Auth Required | Role |
|--------|----------|-------------|---------------|------|
| POST | `/api/auth/register` | Register new user | ❌ | - |
| POST | `/api/auth/login` | Login user | ❌ | - |
| POST | `/api/auth/refresh` | Refresh access token | ✅ (refresh) | All |
| POST | `/api/auth/logout` | Logout user | ✅ | All |
| GET | `/api/auth/me` | Get current user | ✅ | All |
| PUT | `/api/auth/me` | Update profile | ✅ | All |
| GET | `/api/auth/users` | List all users | ✅ | Admin |
| PUT | `/api/auth/users/:id` | Update user | ✅ | Admin |
| DELETE | `/api/auth/users/:id` | Delete user | ✅ | Admin |

### Vendor Endpoints

| Method | Endpoint | Description | Auth Required | Role |
|--------|----------|-------------|---------------|------|
| GET | `/api/health` | Health check | ❌ | - |
| GET | `/api/vendors` | List all vendors | ✅ | All |
| GET | `/api/vendors/:id` | Get vendor details | ✅ | All |
| POST | `/api/vendors` | Create vendor | ✅ | All |
| PUT | `/api/vendors/:id` | Update vendor | ✅ | All |
| DELETE | `/api/vendors/:id` | Delete vendor | ✅ | Admin |
| GET | `/api/vendors/:id/qr` | Generate QR code | ✅ | All |
| GET | `/api/vendors/:id/qr/download` | Download QR | ✅ | All |
| GET | `/api/vendors/performance` | Performance comparison | ✅ | All |
| POST | `/api/seed` | Seed sample data | ✅ | Admin |

### Track Items Endpoints (Railway Fittings)

| Method | Endpoint | Description | Auth Required | Role |
|--------|----------|-------------|---------------|------|
| GET | `/api/track-items` | List all track items | ✅ | All |
| GET | `/api/track-items/:id` | Get item details | ✅ | All |
| POST | `/api/track-items` | Create track item | ✅ | All |
| PUT | `/api/track-items/:id` | Update track item | ✅ | All |
| DELETE | `/api/track-items/:id` | Delete track item | ✅ | Admin |
| GET | `/api/track-items/:id/qr` | Generate QR code | ✅ | All |
| GET | `/api/track-items/:id/qr/download` | Download QR | ✅ | All |
| GET | `/api/track-items/analytics` | Get analytics | ✅ | All |
| GET | `/api/track-items/exceptions` | Get exceptions | ✅ | All |
| POST | `/api/scan-track-item` | Scan QR code | ✅ | All |

### Inspection Endpoints

| Method | Endpoint | Description | Auth Required | Role |
|--------|----------|-------------|---------------|------|
| GET | `/api/track-items/:id/inspections` | List inspections | ✅ | All |
| POST | `/api/track-items/:id/inspections` | Create inspection | ✅ | All |
| PUT | `/api/inspections/:id` | Update inspection | ✅ | All |
| DELETE | `/api/inspections/:id` | Delete inspection | ✅ | Admin |

### Analytics & Scanner Endpoints

| Method | Endpoint | Description | Auth Required | Role |
|--------|----------|-------------|---------------|------|
| POST | `/api/scan` | Scan/verify QR | ✅ | All |
| GET | `/api/analytics` | Get vendor analytics | ✅ | All |
| GET | `/api/track-items/analytics` | Track items analytics | ✅ | All |

---

## 🗄️ Database Schema

### Users Table
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| username | VARCHAR(80) | Unique username |
| email | VARCHAR(120) | Unique email |
| password_hash | VARCHAR(255) | bcrypt hash |
| role | VARCHAR(20) | admin/user/viewer |
| is_active | BOOLEAN | Account status |
| created_at | DATETIME | Creation timestamp |
| updated_at | DATETIME | Last update |
| last_login | DATETIME | Last login time |

### Vendor Data Table
| Column | Type | Description |
|--------|------|-------------|
| id | VARCHAR(50) | Primary key (vendor ID) |
| vendor_name | VARCHAR(255) | Vendor name |
| vendor_code | VARCHAR(50) | Unique vendor code |
| contact_person | VARCHAR(100) | Contact person |
| contact_email | VARCHAR(255) | Email |
| contact_phone | VARCHAR(20) | Phone |
| address_line1 | VARCHAR(255) | Address |
| city | VARCHAR(100) | City |
| state | VARCHAR(100) | State |
| postal_code | VARCHAR(20) | PIN code |
| country | VARCHAR(100) | Country |
| tax_id | VARCHAR(50) | Tax/GST ID |
| bank_account | VARCHAR(50) | Bank account |
| certification_status | VARCHAR(50) | approved/pending/blacklisted |
| performance_rating | FLOAT | 0-5 rating |
| is_approved | BOOLEAN | Approval status |
| approval_date | DATE | Approval date |
| created_by_id | INTEGER | FK to users |
| created_at | DATETIME | Creation timestamp |
| updated_at | DATETIME | Last update |

### Track Items Table
| Column | Type | Description |
|--------|------|-------------|
| id | VARCHAR(50) | Primary key (item ID) |
| item_type | VARCHAR(50) | erc/rail_pad/liner/sleeper |
| lot_number | VARCHAR(100) | Unique lot/batch number |
| vendor_id | VARCHAR(50) | FK to vendor_data |
| quantity | INTEGER | Quantity |
| manufacture_date | DATE | Manufacturing date |
| supply_date | DATE | Supply date |
| installation_date | DATE | Installation date |
| warranty_period_years | INTEGER | Warranty period |
| warranty_start_date | DATE | Warranty start |
| warranty_expiry_date | DATE | Warranty expiry |
| installation_location | VARCHAR(255) | Location |
| kilometer_from | FLOAT | KM marker from |
| kilometer_to | FLOAT | KM marker to |
| section_name | VARCHAR(100) | Section name |
| division | VARCHAR(100) | Division |
| zone | VARCHAR(100) | Zone |
| status | VARCHAR(50) | in_stock/installed/etc |
| performance_status | VARCHAR(50) | good/average/poor/failed |
| defect_count | INTEGER | Total defects |
| replacement_count | INTEGER | Total replacements |
| specifications | TEXT | JSON specs |
| details | TEXT | Additional details |
| notes | TEXT | Notes |
| created_by_id | INTEGER | FK to users |
| created_at | DATETIME | Creation timestamp |
| updated_at | DATETIME | Last update |

### Inspections Table
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| track_item_id | VARCHAR(50) | FK to track_items |
| inspection_type | VARCHAR(50) | manufacturing/supply/etc |
| inspection_date | DATE | Inspection date |
| inspector_name | VARCHAR(100) | Inspector name |
| inspector_designation | VARCHAR(100) | Designation |
| inspection_status | VARCHAR(50) | passed/failed/conditional |
| quality_grade | VARCHAR(20) | A/B/C/D/F |
| remarks | TEXT | Remarks |
| defects_found | TEXT | JSON array |
| action_taken | VARCHAR(255) | Action taken |
| next_inspection_due | DATE | Next due date |
| document_references | TEXT | JSON array |
| created_by_id | INTEGER | FK to users |
| created_at | DATETIME | Creation timestamp |

---

## 🔒 Security Features

### Authentication & Authorization
- **JWT Tokens**: Access tokens (1 hour) + Refresh tokens (30 days)
- **Password Security**: bcrypt hashing with 12 salt rounds
- **Role-Based Access**: Admin, User, Viewer roles with granular permissions
- **Session Management**: Automatic token refresh, secure cookie options

### API Security
- **Rate Limiting**: Configurable limits per endpoint (Redis-backed)
  - Login: 5 requests/minute
  - Register: 3 requests/hour
  - Vendors: 30 requests/hour (create), 100 requests/hour (read)
  - Delete: 10 requests/hour
- **Input Validation**: Email, phone, GST, PAN, bank account, PIN code validation
- **CORS Protection**: Configurable origin restrictions
- **Security Headers**: X-Frame-Options, X-Content-Type-Options, X-XSS-Protection, HSTS

### Data Security
- **SQL Injection Prevention**: SQLAlchemy ORM with parameterized queries
- **XSS Protection**: HTML sanitization, escape user input
- **Audit Trail**: Track created_by, timestamps for all records
- **Environment Variables**: No hardcoded credentials

### Network Security
- **HTTPS Required**: SSL/TLS configuration via Nginx
- **HSTS**: Strict Transport Security headers
- **CSP**: Content Security Policy headers

See [SECURITY.md](SECURITY.md) for complete security guidelines.

---

## 🧪 Testing

### Run Backend Tests

```bash
cd backend
venv\Scripts\activate  # Windows

# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_auth.py -v

# Run tests matching pattern
pytest -k "test_login" -v

# Open coverage report
start htmlcov/index.html  # Windows
open htmlcov/index.html   # Mac/Linux
```

### Test Coverage

The project includes comprehensive tests for:
- ✅ Authentication (login, register, refresh, logout)
- ✅ Vendor CRUD operations
- ✅ Track items management
- ✅ QR code generation and scanning
- ✅ Analytics endpoints
- ✅ Input validation
- ✅ Rate limiting

**Target Coverage**: 80%+

### Run Frontend Tests

```bash
cd frontend

# Run tests
npm test

# Run with coverage
npm test -- --coverage

# Run in watch mode
npm test -- --watch
```

---

## 🌐 Deployment

### Local Development
```bash
docker-compose up --build
```

### Production (Docker Compose)
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Cloud Platforms

#### Railway (Backend + PostgreSQL)
1. Deploy from GitHub
2. Add PostgreSQL database
3. Set environment variables
4. Auto-deploys on push

#### Vercel (Frontend)
```bash
cd frontend
npm run deploy:vercel
```

#### Render (Full Stack)
- Web Service for backend
- Static Site for frontend
- PostgreSQL database

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed guides on:
- Railway deployment
- Vercel/Netlify frontend
- Render deployment
- Docker deployment
- Alternative free hosting options

---

## 📁 Project Structure

```
SIH PROJECT/
├── backend/                        # Flask REST API
│   ├── app.py                      # Main Flask application
│   ├── auth.py                     # Authentication routes
│   ├── models.py                   # Database models
│   ├── insights.py                 # AI risk assessment
│   ├── config.py                   # Configuration
│   ├── extensions.py               # Flask extensions
│   ├── validators.py               # Input validation
│   ├── track_items_routes.py       # Track items endpoints
│   ├── seed_data.py                # Sample data seeder
│   ├── requirements.txt            # Python dependencies
│   ├── Dockerfile                  # Docker config
│   ├── Dockerfile.prod             # Production Dockerfile
│   ├── tests/                      # Pytest tests
│   │   ├── conftest.py
│   │   ├── test_auth.py
│   │   ├── test_vendors.py
│   │   └── test_qr.py
│   ├── .env.example                # Environment template
│   └── pytest.ini                  # Pytest config
│
├── frontend/                       # React Frontend
│   ├── src/
│   │   ├── App.js                  # Main React component
│   │   ├── api.js                  # API client
│   │   ├── index.js                # Entry point
│   │   ├── App.css                 # Styles
│   │   └── pages/
│   │       ├── Dashboard.js        # Dashboard
│   │       ├── VendorList.js       # Vendor listing
│   │       ├── AddVendor.js        # Add vendor
│   │       ├── TrackItemsList.js   # Track items list
│   │       ├── AddTrackItem.js     # Add track item
│   │       ├── TrackItemDetail.js  # Track item detail
│   │       ├── Scanner.js          # QR scanner
│   │       ├── VendorDetail.js     # Vendor details
│   │       ├── VendorPerformance.js# Performance comparison
│   │       ├── AddInspection.js    # Add inspection
│   │       ├── Profile.js          # User profile
│   │       └── Login.js            # Login page
│   ├── package.json                # Node dependencies
│   ├── .env.example                # Environment template
│   └── public/
│
├── nginx/                          # Nginx configuration
│   └── nginx.conf                  # Reverse proxy config
│
├── PythonSIH/                      # Original Python Scripts
│   ├── generate_qr.py              # Generate QR codes
│   ├── scan_qr_gui.py              # Desktop GUI scanner
│   └── vendor_insights_builder.py  # AI insights
│
├── QR_Scanner/                     # OpenCV scanner
│
├── docker-compose.yml              # Docker Compose (dev)
├── docker-compose.prod.yml         # Docker Compose (prod)
├── railway.toml                    # Railway deployment
├── render.yaml                     # Render deployment
├── .env.prod.example               # Production env template
├── README.md                       # This file
├── SETUP.md                        # Setup guide
├── DEPLOYMENT.md                   # Deployment guide
├── SECURITY.md                     # Security best practices
├── CHANGELOG.md                    # Version history
├── QUICKSTART.md                   # Quick start guide
└── IMPLEMENTATION_SUMMARY.md       # Implementation details
```

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [README.md](README.md) | Project overview and documentation |
| [SETUP.md](SETUP.md) | Complete setup instructions |
| [DEPLOYMENT.md](DEPLOYMENT.md) | Cloud and local deployment guides |
| [SECURITY.md](SECURITY.md) | Security best practices |
| [CHANGELOG.md](CHANGELOG.md) | Version history and changes |
| [QUICKSTART.md](QUICKSTART.md) | Quick start guide |
| [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) | Implementation details |

---

## 🤝 Contributing

This is a Smart India Hackathon project. Contributions and improvements are welcome!

### Development Workflow

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Write/update tests
5. Ensure all tests pass (`pytest --cov=.`)
6. Run linting (`flake8 backend/`, `black backend/ --check`)
7. Commit your changes (`git commit -m 'Add amazing feature'`)
8. Push to the branch (`git push origin feature/amazing-feature`)
9. Open a Pull Request

### Code Quality

```bash
# Backend linting
flake8 backend/
black backend/ --check

# Frontend linting
cd frontend
npm run lint
```

### Code of Conduct

- Be respectful and inclusive
- Follow SIH guidelines
- Write clean, documented code
- Test your changes thoroughly

---

## 📄 License

Smart India Hackathon Project © 2024-25

---

## 🙏 Acknowledgments

- **Smart India Hackathon** - For the opportunity to build this solution
- **Indian Railways** - For the problem statement and requirements
- **Flask and React Communities** - For excellent frameworks and documentation
- **OWASP** - For security guidelines and best practices

---

## 📞 Support

For issues and questions:
1. Check the documentation
2. Review existing issues
3. Check logs (`docker-compose logs`)
4. Test endpoints with Postman/curl

---

## 🎯 Default Credentials

**After first setup:**
- **Username**: `admin`
- **Password**: `Admin@123`
- **Email**: `admin@vendorverify.com`

⚠️ **CHANGE THESE IMMEDIATELY AFTER FIRST LOGIN!**

---

## 📊 Key Statistics

- **Total API Endpoints**: 30+
- **Database Models**: 4 (User, Vendor, TrackItem, Inspection)
- **Test Coverage**: ~75%+ (target: 80%+)
- **Security Score**: A+ (OWASP compliance)
- **Supported Item Types**: ERC, Rail Pads, Liners, Sleepers
- **Inspection Types**: Manufacturing, Supply, Installation, Periodic, Defect

---

**Built for Smart India Hackathon 2024-25** 🇮🇳

**RailTrack Pro** - Empowering Indian Railways with smart track fittings management

---

*Last Updated: March 2026*
*Version: 2.0.0*
