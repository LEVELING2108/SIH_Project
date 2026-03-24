# 🚀 Setup Guide - RailTrack Pro

Complete guide to set up the Railway Track Fittings Management System with authentication, security, and inspection capabilities.

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Development Setup](#local-development-setup)
3. [Production Deployment](#production-deployment)
4. [Configuration](#configuration)
5. [Database Initialization](#database-initialization)
6. [Testing](#testing)
7. [Troubleshooting](#troubleshooting)

---

## 🔧 Prerequisites

### Required Software

- **Python**: 3.11 or higher
- **Node.js**: 18.x or higher
- **Git**: Latest version
- **Docker** (optional): 20.x or higher

### System Requirements

- **RAM**: Minimum 4GB (8GB recommended)
- **Storage**: 2GB free space
- **OS**: Windows 10/11, Linux, macOS

### For Windows Users

```powershell
# Install Python (if not installed)
winget install Python.Python.3.11

# Install Node.js
winget install OpenJS.NodeJS.LTS

# Install Git
winget install Git.Git

# Install Docker Desktop (optional)
winget install Docker.DockerDesktop
```

### For Linux/Mac Users

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3.11 python3-pip nodejs npm git

# macOS (with Homebrew)
brew install python@3.11 node git
```

### Verify Installations

```bash
python --version    # Should show Python 3.11+
node --version      # Should show Node 18.x
npm --version       # Should show npm 9.x+
git --version       # Should show git 2.x+
```

---

## 💻 Local Development Setup

### Step 1: Clone Repository

```bash
cd "C:\Users\suman\Downloads\OLD_PROJECT\SIH PROJECT"
# Or navigate to your project directory
```

### Step 2: Backend Setup

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

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Copy environment file
copy .env.example .env  # Windows
# or
cp .env.example .env    # Linux/Mac

# Edit .env file and set your configuration
# IMPORTANT: Change SECRET_KEY and JWT_SECRET_KEY!
```

### Step 3: Generate Secure Keys

```bash
# Generate secure secret keys
python -c "import secrets; print('SECRET_KEY:', secrets.token_hex(32))"
python -c "import secrets; print('JWT_SECRET_KEY:', secrets.token_hex(32))"
```

Copy these values to your `.env` file.

### Step 4: Configure Backend Environment

Edit `backend/.env`:

```env
# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=true

# Security Keys (REPLACE WITH YOUR GENERATED KEYS)
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-here

# Database (SQLite for development)
DATABASE_URL=sqlite:///vendors.db

# CORS (allow frontend)
CORS_ORIGINS=http://localhost:3000

# Rate Limiting (disable for development)
RATELIMIT_ENABLED=false
```

### Step 5: Initialize Database and Create Admin User

```bash
# Run the application (database auto-initializes)
python app.py
```

The app will automatically:
- Create SQLite database (`instance/vendors.db`)
- Create default admin user (username: `admin`, password: `Admin@123`)
- Create all database tables

**⚠️ IMPORTANT**: Change the default admin password immediately!

### Step 6: Seed Sample Data (Optional)

To populate the database with sample vendors and track items:

```bash
# With the server running, call the seed endpoint:
curl -X POST http://localhost:5000/api/seed \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

Or use the frontend interface after logging in.

### Step 7: Frontend Setup

Open a **new terminal** window:

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Copy environment file
copy .env.example .env  # Windows
# or
cp .env.example .env    # Linux/Mac

# Edit .env and set API URL
REACT_APP_API_URL=http://localhost:5000/api
```

### Step 8: Run Development Servers

**Terminal 1 (Backend):**
```bash
cd backend
venv\Scripts\activate  # Windows
python app.py
```

Backend runs at: `http://localhost:5000`

**Terminal 2 (Frontend):**
```bash
cd frontend
npm start
```

Frontend runs at: `http://localhost:3000`

### Step 9: Access the Application

1. Open browser: http://localhost:3000
2. Login with default credentials:
   - Username: `admin`
   - Password: `Admin@123`
3. **Change password immediately** after login!

---

## 🐳 Docker Setup (Recommended for Production)

### Option 1: Development with Docker

```bash
# From project root
docker-compose up --build
```

This starts:
- **Backend**: http://localhost:5000
- **Frontend**: http://localhost:3000
- **PostgreSQL**: localhost:5432

**Advantages:**
- Consistent environment across systems
- No need to install Python/Node locally
- Database persistence

**Stop services:**
```bash
docker-compose down
```

### Option 2: Production Deployment

```bash
# Copy production environment file
copy .env.prod.example .env  # Windows
# or
cp .env.prod.example .env    # Linux/Mac

# Edit .env and set ALL required variables

# Build and run production stack
docker-compose -f docker-compose.prod.yml up -d --build

# View logs
docker-compose logs -f

# Stop services
docker-compose -f docker-compose.prod.yml down
```

**Production Stack Includes:**
- Flask backend with Gunicorn
- PostgreSQL database
- Redis (for rate limiting)
- Nginx reverse proxy

---

## ⚙️ Configuration

### Environment Variables

#### Backend (.env)

**Required Variables:**

```env
# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=true

# Security Keys (GENERATE SECURE RANDOM VALUES)
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-here

# Database
DATABASE_URL=sqlite:///vendors.db
# For PostgreSQL:
# DATABASE_URL=postgresql://user:password@localhost:5432/vendors

# CORS (Comma-separated list of allowed origins)
CORS_ORIGINS=http://localhost:3000
```

**Optional Variables:**

```env
# Rate Limiting
RATELIMIT_ENABLED=false
RATELIMIT_STORAGE_URL=redis://localhost:6379/0

# JWT Token Expiration (seconds)
JWT_ACCESS_TOKEN_EXPIRES=3600
JWT_REFRESH_TOKEN_EXPIRES=2592000

# Logging
LOG_LEVEL=INFO
LOG_FILE=app.log

# Email Configuration (for notifications)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

#### Frontend (.env)

```env
REACT_APP_API_URL=http://localhost:5000/api
```

### Production Environment Variables

See `.env.prod.example` for complete list of production variables.

**Key Production Settings:**

```env
FLASK_ENV=production
FLASK_DEBUG=false

# Use PostgreSQL in production
DATABASE_URL=postgresql://user:password@host:5432/vendors

# Restrict CORS to your domain
CORS_ORIGINS=https://yourdomain.com

# Enable rate limiting
RATELIMIT_ENABLED=true
RATELIMIT_STORAGE_URL=redis://redis:6379/0

# Secure cookies
SESSION_COOKIE_SECURE=true
SESSION_COOKIE_HTTPONLY=true
SESSION_COOKIE_SAMESITE=Lax
```

---

## 🗄️ Database Initialization

### Automatic Initialization

The database is automatically initialized when you run the application for the first time:

```bash
python app.py
```

This creates:
- All database tables
- Default admin user
- Indexes for performance

### Manual Database Setup

If you need to reset the database:

```bash
# For SQLite (development only!)
cd backend
rm instance/vendors.db  # Linux/Mac
del instance\vendors.db  # Windows

# Run app to recreate database
python app.py
```

### Database Migrations (Future Use)

If you add new models or change schema:

```bash
cd backend
venv\Scripts\activate

# Initialize Flask-Migrate (first time only)
flask db init

# Create migration after model changes
flask db migrate -m "Description of changes"

# Apply migrations
flask db upgrade

# Rollback migration
flask db downgrade
```

---

## 🧪 Testing

### Backend Tests

```bash
cd backend
venv\Scripts\activate

# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_auth.py -v

# Run tests matching pattern
pytest -k "test_login" -v

# Run tests and open coverage report
pytest --cov=. --cov-report=html
start htmlcov\index.html  # Windows
open htmlcov/index.html   # Mac/Linux
```

### Test Coverage Report

The test suite covers:
- ✅ Authentication (login, register, refresh, logout)
- ✅ Vendor CRUD operations
- ✅ Track items management
- ✅ QR code generation and scanning
- ✅ Analytics endpoints
- ✅ Input validation
- ✅ Rate limiting

**Target Coverage**: 80%+

### Frontend Tests

```bash
cd frontend

# Run tests
npm test

# Run with coverage
npm test -- --coverage

# Run in watch mode
npm test -- --watchAll
```

---

## 🔒 Security Setup

### 1. Change Default Admin Password

After first login:

**Via Frontend:**
1. Login as admin
2. Go to Profile page
3. Click "Change Password"
4. Enter new password

**Via API:**
```bash
# First, login to get token
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "Admin@123"}'

# Use the access token to change password
curl -X PUT http://localhost:5000/api/auth/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"password": "YourNewSecure@Password123"}'
```

### 2. Configure CORS for Production

In `.env`:
```env
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

**Never use `CORS_ORIGINS=*` in production!**

### 3. Enable Rate Limiting

In `.env`:
```env
RATELIMIT_ENABLED=true
RATELIMIT_STORAGE_URL=redis://localhost:6379/0
```

### 4. Use HTTPS in Production

- Obtain SSL certificate (Let's Encrypt recommended)
- Configure Nginx with SSL (see `nginx/nginx.conf`)
- Redirect HTTP to HTTPS
- Enable HSTS headers

---

## 🚀 Production Deployment Checklist

Before deploying to production:

- [ ] Generate strong SECRET_KEY and JWT_SECRET_KEY
- [ ] Change default admin password
- [ ] Configure CORS for your domain
- [ ] Set up PostgreSQL database
- [ ] Enable rate limiting with Redis
- [ ] Configure HTTPS/SSL
- [ ] Set up logging and monitoring
- [ ] Configure backup strategy
- [ ] Test all endpoints
- [ ] Review security settings
- [ ] Update frontend API URL
- [ ] Run full test suite
- [ ] Document deployment details

---

## 🆘 Troubleshooting

### Backend won't start

**Error: Module not found**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

**Error: Database locked**
```bash
# Delete SQLite database (development only!)
rm instance/vendors.db
python app.py
```

**Error: Port already in use**
```bash
# Find process using port 5000
netstat -ano | findstr :5000

# Kill the process or use different port
# In .env, set:
PORT=5001
```

### Frontend won't start

**Error: Cannot find module**
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

**Error: Port already in use**
```bash
# Use different port
set PORT=3001  # Windows
PORT=3001 npm start  # Linux/Mac
```

**Error: Cannot connect to backend**
```bash
# Check backend is running
curl http://localhost:5000/api/health

# Check CORS settings in backend .env
CORS_ORIGINS=http://localhost:3000
```

### Docker Issues

**Error: Container won't start**
```bash
# View logs
docker-compose logs backend

# Rebuild containers
docker-compose up -d --build --force-recreate

# Clean up volumes (deletes data!)
docker-compose down -v
docker-compose up -d --build
```

**Error: Database connection failed**
```bash
# Check PostgreSQL is running
docker-compose ps

# Check DATABASE_URL in .env
# Format: postgresql://user:password@host:5432/db
```

### Authentication Issues

**Error: Token expired**
- Access tokens expire after 1 hour
- Use refresh token to get new access token
- Frontend handles this automatically

**Error: Invalid credentials**
- Check username/password
- Ensure user is active in database
- Check password hash is correct

**Error: 401 Unauthorized**
- Check token is included in request headers
- Verify token format: `Bearer <token>`
- Check token hasn't been revoked

### QR Scanner Issues

**Camera not working:**
- Ensure site is served over HTTPS (required for camera access)
- Grant camera permissions in browser
- Test in different browser (Chrome, Firefox, Edge)
- Check camera is not used by another application

### Database Issues

**Error: Table doesn't exist**
```bash
# Reset database (development only!)
rm instance/vendors.db
python app.py
```

**Error: Duplicate entry**
- Vendor IDs and lot numbers must be unique
- Use different ID or update existing record

---

## 📞 Support

For issues:
1. Check logs in `backend/logs/` or Docker logs
2. Review error messages carefully
3. Test endpoints with Postman/curl
4. Check database connectivity
5. Verify environment variables
6. Review documentation

### Useful Commands

```bash
# View backend logs
docker-compose logs backend

# View frontend logs
docker-compose logs frontend

# View database logs
docker-compose logs db

# Restart services
docker-compose restart

# Stop all services
docker-compose down

# Start all services
docker-compose up -d

# Check service status
docker-compose ps

# Access backend shell
docker-compose exec backend bash

# Access database shell
docker-compose exec db psql -U postgres -d vendors
```

---

## 🎯 Default Credentials

**After first setup:**
- **Username**: `admin`
- **Password**: `Admin@123`
- **Email**: `admin@vendorverify.com`
- **Role**: Admin

**⚠️ CHANGE THESE IMMEDIATELY!**

---

## 📚 Additional Documentation

- [README.md](README.md) - Project overview
- [DEPLOYMENT.md](DEPLOYMENT.md) - Cloud deployment options
- [SECURITY.md](SECURITY.md) - Security best practices
- [CHANGELOG.md](CHANGELOG.md) - Version history
- [QUICKSTART.md](QUICKSTART.md) - Quick start guide
- [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) - Implementation details

---

## 🎓 Learning Resources

### Flask
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)

### React
- [React Documentation](https://reactjs.org/)
- [React Router](https://reactrouter.com/)
- [React Bootstrap](https://react-bootstrap.github.io/)

### Docker
- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

### Security
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [JWT Best Practices](https://datatracker.ietf.org/doc/html/rfc8725)

---

**Happy Coding! 🚂**

*Last Updated: March 2026*
*Version: 2.0.0*
