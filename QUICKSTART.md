# ⚡ Quick Start Guide - RailTrack Pro

Get your Railway Track Fittings Management System running in 5 minutes!

---

## 🚀 Local Development (Fast Track)

### Step 1: Install Dependencies

```bash
# Backend
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt

# Frontend (new terminal)
cd frontend
npm install
```

### Step 2: Configure Environment

```bash
# Backend - Copy and edit .env
cd backend
copy .env.example .env  # Windows

# Generate secure keys
python -c "import secrets; print('SECRET_KEY:', secrets.token_hex(32))"
python -c "import secrets; print('JWT_SECRET_KEY:', secrets.token_hex(32))"

# Add these to .env file
```

Edit `backend/.env`:
```env
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-here
DATABASE_URL=sqlite:///vendors.db
CORS_ORIGINS=http://localhost:3000
RATELIMIT_ENABLED=false
```

### Step 3: Run Application

```bash
# Terminal 1 - Backend
cd backend
venv\Scripts\activate
python app.py
# Runs at http://localhost:5000

# Terminal 2 - Frontend
cd frontend
npm start
# Runs at http://localhost:3000
```

### Step 4: Login

**Default Admin Credentials:**
- Username: `admin`
- Password: `Admin@123`
- ⚠️ **Change this immediately!**

---

## 🐳 Docker (Easiest)

```bash
# One command to run everything
docker-compose up --build

# Access:
# Frontend: http://localhost:3000
# Backend: http://localhost:5000
```

**Stop services:**
```bash
docker-compose down
```

---

## 🧪 Run Tests

```bash
cd backend
venv\Scripts\activate

# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Open coverage report
start htmlcov/index.html  # Windows
open htmlcov/index.html   # Mac/Linux
```

---

## 🔑 API Quick Reference

### Register User
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "Test@123"
  }'
```

### Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "Admin@123"
  }'
```

Response:
```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ..."
}
```

### Create Vendor
```bash
curl -X POST http://localhost:5000/api/vendors \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "id": "VENDOR001",
    "vendor_name": "Test Vendor",
    "contact_email": "vendor@example.com",
    "vendor_code": "V001"
  }'
```

### Create Track Item
```bash
curl -X POST http://localhost:5000/api/track-items \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "id": "ITEM001",
    "item_type": "elastic_rail_clip",
    "lot_number": "LOT2024001",
    "vendor_id": "VENDOR001",
    "quantity": 1000,
    "manufacture_date": "2024-01-15",
    "item_type": "erc"
  }'
```

### Get Vendors
```bash
curl -X GET http://localhost:5000/api/vendors \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Get Track Items
```bash
curl -X GET http://localhost:5000/api/track-items \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Generate QR Code
```bash
curl -X GET http://localhost:5000/api/track-items/ITEM001/qr \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Scan QR Code
```bash
curl -X POST http://localhost:5000/api/scan \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "qr_data": "VENDOR001"
  }'
```

### Get Analytics
```bash
curl -X GET http://localhost:5000/api/track-items/analytics \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Seed Sample Data
```bash
curl -X POST http://localhost:5000/api/seed \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## 📁 Important Files

| File | Purpose |
|------|---------|
| `backend/.env` | Backend configuration |
| `frontend/.env` | Frontend configuration |
| `backend/app.py` | Main Flask application |
| `backend/auth.py` | Authentication routes |
| `backend/models.py` | Database models |
| `backend/track_items_routes.py` | Track items endpoints |
| `backend/validators.py` | Input validation |
| `docker-compose.yml` | Docker configuration |
| `frontend/src/App.js` | Main React component |
| `frontend/src/api.js` | API client |

---

## 🆘 Troubleshooting

### Backend won't start
```bash
# Check dependencies
pip install -r requirements.txt

# Check port
netstat -ano | findstr :5000

# Check logs
python app.py 2>&1 | tee app.log
```

### Frontend won't start
```bash
# Clear cache
rm -rf node_modules package-lock.json
npm install

# Check Node version
node --version  # Should be 18+
```

### Database errors
```bash
# Reset database (development only!)
rm instance/vendors.db
python app.py
```

### Tests failing
```bash
# Reinstall test dependencies
pip install pytest pytest-flask pytest-cov

# Run tests with verbose output
pytest -v
```

### Can't login
```bash
# Check credentials
# Username: admin
# Password: Admin@123 (default)

# Reset admin password (if you have database access)
# Delete users table and restart app
```

### CORS errors
```bash
# Check backend .env
CORS_ORIGINS=http://localhost:3000

# Restart backend
```

---

## 📊 Environment Variables

### Minimum Required (backend/.env)

```env
# Flask
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-here

# Database
DATABASE_URL=sqlite:///vendors.db

# CORS
CORS_ORIGINS=http://localhost:3000

# Rate Limiting (disable for development)
RATELIMIT_ENABLED=false
```

### Frontend (frontend/.env)

```env
REACT_APP_API_URL=http://localhost:5000/api
```

---

## 🎯 Next Steps

After getting it running:

1. ✅ **Change default password** (Profile page)
2. ✅ **Generate secure keys** (use secrets.token_hex)
3. ✅ **Run tests** (`pytest --cov=.`)
4. ✅ **Read SECURITY.md** (security best practices)
5. ✅ **Configure CORS** (for your domain)
6. ✅ **Seed sample data** (optional, via API)
7. ✅ **Explore features** (vendors, track items, inspections)

---

## 📚 Full Documentation

- [README.md](README.md) - Project overview
- [SETUP.md](SETUP.md) - Complete setup guide
- [SECURITY.md](SECURITY.md) - Security best practices
- [DEPLOYMENT.md](DEPLOYMENT.md) - Production deployment
- [CHANGELOG.md](CHANGELOG.md) - Version history
- [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) - Implementation details

---

## 🎓 Quick Feature Tour

### Dashboard
- View analytics and statistics
- Risk distribution chart
- Total vendors and track items
- Recent activity

### Track Items
- List all track items (ERC, Rail Pads, Liners, Sleepers)
- Add new track items with specifications
- View item details with inspection history
- Generate and download QR codes
- Scan QR codes in the field

### Vendors
- List all vendors/manufacturers
- Add new vendors
- View vendor details and performance
- Compare vendor performance

### Inspections
- Create inspections for track items
- Record quality grades and defects
- Track inspection history
- Schedule next inspections

### Scanner
- Camera-based QR code scanning
- Instant verification with AI insights
- Risk scores and flags
- Recommendations

---

## 🆘 Need Help?

1. Check logs: `docker-compose logs` or `backend/logs/`
2. Review error messages carefully
3. Test with Postman/curl
4. Read documentation
5. Check test coverage

### Useful Commands

```bash
# View logs
docker-compose logs -f

# Restart services
docker-compose restart

# Check status
docker-compose ps

# Run tests
pytest --cov=.

# Build frontend
cd frontend && npm run build

# Access database
docker-compose exec db psql -U postgres -d vendors
```

---

**Happy Coding! 🚂**

*Last Updated: March 2026*
*Version: 2.0.0*
