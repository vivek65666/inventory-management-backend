# Quick Start Guide

Get the Inventory Management API up and running in 5 minutes.

## Prerequisites

- Python 3.8+ installed
- PostgreSQL database running locally or accessible
- PowerShell (Windows) or Bash (Linux/Mac)

## Quick Setup (Windows PowerShell)

```powershell
# 1. Navigate to project
cd c:\Users\Vivek\inventory-backend

# 2. Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env and update DATABASE_URL

# 5. Run the application
python main.py
```

## Quick Setup (Linux/Mac)

```bash
# 1. Navigate to project
cd ~/inventory-backend

# 2. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env and update DATABASE_URL

# 5. Run the application
python main.py
```

## Access the API

- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## First Steps

### 1. Register a User (in Swagger UI or via curl)

**In Swagger UI:**
- Click on `/api/auth/register`
- Click "Try it out"
- Fill in username, email, and password
- Click "Execute"

**Via PowerShell:**
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

### 2. Login

**In Swagger UI:**
- Click on `/api/auth/login`
- Click "Try it out"
- Enter username and password
- Click "Execute"
- Copy the `access_token` from response

**Via PowerShell:**
```powershell
$body = @{
    username = "admin"
    password = "SecurePass123!"
} | ConvertTo-Json

$response = curl.exe -X POST http://localhost:8000/api/auth/login `
  -H "Content-Type: application/json" `
  -d $body

$token = ($response | ConvertFrom-Json).access_token
Write-Host "Token: $token"
```

### 3. Create a Product

**In Swagger UI:**
- Click "Authorize" button
- Paste the access token
- Click `/api/products` POST endpoint
- Fill in product details
- Execute

**Via PowerShell:**
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

### 4. Create Inventory Item

After creating a product, create an inventory item:

```powershell
$token = "your-access-token-here"
$productId = 1  # From previous response

$body = @{
    product_id = $productId
    quantity = 100
    warehouse_location = "Warehouse A - Shelf 1"
} | ConvertTo-Json

curl.exe -X POST http://localhost:8000/api/inventory `
  -H "Content-Type: application/json" `
  -H "Authorization: Bearer $token" `
  -d $body
```

## Testing

Run all tests:

```powershell
pytest
```

Run specific test file:

```powershell
pytest tests/test_auth.py -v
```

Run with coverage:

```powershell
pytest --cov=. --cov-report=html
```

## Docker Quick Start

```powershell
# Build image
docker build -t inventory-api:latest .

# Run with docker-compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

## Common Commands

```powershell
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Deactivate
deactivate

# Reinstall dependencies
pip install -r requirements.txt

# Run with custom port
uvicorn main:app --port 8001

# Run with logging
uvicorn main:app --log-level debug

# Format code
black .

# Check linting
flake8 .

# Check imports
isort .
```

## API Endpoints Summary

| Endpoint | Method | Auth | Purpose |
|----------|--------|------|---------|
| `/api/auth/register` | POST | No | Register new user |
| `/api/auth/login` | POST | No | Login and get token |
| `/api/auth/me` | GET | Yes | Get current user |
| `/api/products` | GET | Yes | List products |
| `/api/products` | POST | Yes | Create product |
| `/api/products/{id}` | GET | Yes | Get product |
| `/api/products/{id}` | PUT | Yes | Update product |
| `/api/products/{id}` | DELETE | Yes | Delete product |
| `/api/inventory` | GET | Yes | List inventory |
| `/api/inventory` | POST | Yes | Create inventory item |
| `/api/inventory/{id}` | GET | Yes | Get inventory item |
| `/api/inventory/{id}` | PUT | Yes | Update inventory |
| `/api/inventory/{id}` | DELETE | Yes | Delete inventory |
| `/api/inventory/{id}/adjust-quantity` | POST | Yes | Adjust quantity |

## Documentation Files

- **README.md** - Full project documentation
- **SETUP_GUIDE.md** - Detailed setup instructions
- **DEPLOYMENT_GUIDE.md** - Production deployment guide
- **SETUP.md** - This file (quick start)

## Troubleshooting

**Q: "ModuleNotFoundError: No module named 'fastapi'"**
A: Activate virtual environment: `.\venv\Scripts\Activate.ps1`

**Q: "psycopg2: could not connect to server"**
A: Check PostgreSQL is running and DATABASE_URL is correct in .env

**Q: "Port 8000 already in use"**
A: Use different port: `uvicorn main:app --port 8001`

**Q: Can't find .env file**
A: Copy from template: `cp .env.example .env`

## Next Steps

1. Read [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed setup
2. Check [README.md](README.md) for full documentation
3. Review [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for production
4. Explore code in `routes/` directory
5. Run tests: `pytest -v`

## Support

Need help? Check the docs:
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

---

**You're all set! Start building! 🚀**
