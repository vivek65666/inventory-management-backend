# FastAPI Inventory Management System - Complete Setup Guide

This guide walks you through setting up the secure RESTful API backend for the retail inventory tracking system.

## Step 1: Navigate to Project Directory

```powershell
cd c:\Users\Vivek\inventory-backend
```

## Step 2: Create Virtual Environment

Create a Python virtual environment to isolate project dependencies:

```powershell
python -m venv venv
```

This creates a `venv` folder containing the isolated Python environment.

## Step 3: Activate Virtual Environment

**On Windows PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

**If you get an execution policy error:**

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then run the activation command again.

**Tip:** You'll see `(venv)` at the start of your terminal prompt when activated.

## Step 4: Upgrade pip

```powershell
pip install --upgrade pip
```

## Step 5: Install All Dependencies

```powershell
pip install -r requirements.txt
```

**What gets installed:**

- **FastAPI** (0.104.1) - Modern async web framework
- **Uvicorn** (0.24.0) - ASGI server to run FastAPI
- **SQLAlchemy** (2.0.23) - Object-relational mapper for databases
- **psycopg2-binary** (2.9.9) - PostgreSQL adapter
- **PyJWT** (2.8.1) - JWT token creation and validation
- **python-dotenv** (1.0.0) - Load environment variables
- **Pydantic** (2.5.0) - Data validation
- **passlib** (1.7.4) - Password hashing with bcrypt
- **python-multipart** (0.0.6) - Handle multipart form data

## Step 6: Set Up PostgreSQL Database

### Option A: Using Local PostgreSQL

**If PostgreSQL is already installed locally:**

1. Open PostgreSQL command line or pgAdmin
2. Create a new database:

```sql
CREATE DATABASE inventory_db;
```

### Option B: Using Docker (Alternative)

```powershell
docker run --name inventory-postgres -e POSTGRES_DB=inventory_db -e POSTGRES_PASSWORD=your_password -p 5432:5432 -d postgres:15
```

## Step 7: Configure Environment Variables

1. Copy the example environment file:

```powershell
cp .env.example .env
```

2. Edit `.env` with your actual values:

```
DATABASE_URL=postgresql://username:password@localhost:5432/inventory_db
SECRET_KEY=your-super-secret-key-change-this-in-production-12345
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=False
```

**Important Notes:**
- Replace `username` and `password` with your PostgreSQL credentials
- Generate a strong `SECRET_KEY` (at least 32 random characters)
- Set `DEBUG=False` in production
- Never commit `.env` to version control

## Step 8: Verify Installation

```powershell
pip list
```

You should see all the packages from requirements.txt listed.

## Step 9: Run the Application

### Option A: Using Python directly

```powershell
python main.py
```

### Option B: Using Uvicorn directly (with auto-reload for development)

```powershell
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Option C: Run without auto-reload (production)

```powershell
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

**Expected output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

## Step 10: Test the API

### Open API Documentation

Visit these URLs in your browser (when server is running):

- **Swagger UI (Interactive)**: http://localhost:8000/docs
- **ReDoc (Read-only)**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

### Test with cURL

**Register a new user:**

```powershell
$body = @{
    username = "admin"
    email = "admin@example.com"
    password = "SecurePass123!"
} | ConvertTo-Json

curl.exe -X POST http://localhost:8000/api/auth/register `
  -H "Content-Type: application/json" `
  -d $body
```

**Login:**

```powershell
$body = @{
    username = "admin"
    password = "SecurePass123!"
} | ConvertTo-Json

curl.exe -X POST http://localhost:8000/api/auth/login `
  -H "Content-Type: application/json" `
  -d $body
```

Copy the `access_token` from the response.

**Create a Product (replace TOKEN with your access_token):**

```powershell
$token = "your-access-token-here"
$body = @{
    sku = "LAPTOP001"
    name = "Dell XPS 15"
    description = "High-performance laptop"
    price = 1299.99
} | ConvertTo-Json

curl.exe -X POST http://localhost:8000/api/products `
  -H "Content-Type: application/json" `
  -H "Authorization: Bearer $token" `
  -d $body
```

## Project Structure Overview

```
inventory-backend/
├── main.py                      # FastAPI application entry point
├── config.py                    # Configuration management
├── database.py                  # Database connection & session setup
├── models.py                    # SQLAlchemy database models
├── schemas.py                   # Pydantic request/response schemas
├── auth.py                      # JWT & password authentication
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variables template
├── .env                         # Actual environment (gitignored)
├── .gitignore                   # Git ignore rules
├── README.md                    # Project documentation
├── LICENSE                      # MIT License
└── routes/
    ├── __init__.py
    ├── auth.py                  # /api/auth endpoints
    ├── products.py              # /api/products endpoints
    └── inventory.py             # /api/inventory endpoints
```

## Common Issues & Solutions

### Issue: "ModuleNotFoundError: No module named 'fastapi'"

**Solution:** Virtual environment not activated
```powershell
.\venv\Scripts\Activate.ps1
```

### Issue: "psycopg2: could not connect to server"

**Solutions:**
- Verify PostgreSQL is running
- Check DATABASE_URL in `.env` file
- Ensure database exists: `CREATE DATABASE inventory_db;`

### Issue: Port 8000 already in use

**Solution:** Use a different port
```powershell
uvicorn main:app --port 8001
```

### Issue: "Secret key too short" or JWT errors

**Solution:** Generate a strong SECRET_KEY
```powershell
# Using Python
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Then update `.env` with the generated key.

## Next Steps

1. **Test API Endpoints**: Use the Swagger UI at `/docs`
2. **Understand Models**: Review `models.py` to understand database structure
3. **Extend Functionality**: Add new endpoints following the existing pattern
4. **Add Tests**: Create test files for endpoints and models
5. **Deploy**: Set up in production environment with proper security

## Security Checklist for Production

- [ ] Generate strong `SECRET_KEY` (32+ characters, random)
- [ ] Set `DEBUG=False` in `.env`
- [ ] Use HTTPS/SSL certificates
- [ ] Restrict CORS origins to specific domains
- [ ] Implement rate limiting
- [ ] Add input validation and sanitization
- [ ] Set up logging and monitoring
- [ ] Use environment-specific configurations
- [ ] Regularly update dependencies
- [ ] Implement API key management for services
- [ ] Add database backups
- [ ] Use managed PostgreSQL (AWS RDS, Azure Database, etc.)

## Useful Commands

```powershell
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Deactivate virtual environment
deactivate

# List installed packages
pip list

# Update a package
pip install --upgrade package-name

# Freeze dependencies to requirements.txt
pip freeze > requirements.txt

# Run tests
pytest

# Run linting
flake8 .

# Format code
black .
```

## Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [PyJWT Documentation](https://pyjwt.readthedocs.io/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Uvicorn Documentation](https://www.uvicorn.org/)

---

**Happy coding!** 🚀
