# Inventory Management API

A secure RESTful API backend for retail inventory tracking system built with FastAPI, SQLAlchemy, and PostgreSQL.

## Features

- **User Authentication**: JWT-based authentication with secure password hashing (bcrypt)
- **Product Management**: Create, read, update, and delete products
- **Inventory Tracking**: Track stock levels and warehouse locations
- **Database**: PostgreSQL with SQLAlchemy ORM
- **API Documentation**: Automatic interactive API documentation with Swagger UI
- **Security**: CORS support, password validation, token expiration

## Project Structure

```
inventory-backend/
├── main.py                 # Application entry point
├── config.py              # Configuration and settings
├── database.py            # Database setup and session management
├── models.py              # SQLAlchemy database models
├── schemas.py             # Pydantic request/response schemas
├── auth.py                # Authentication and security utilities
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variables template
├── .gitignore             # Git ignore rules
└── routes/
    ├── __init__.py
    ├── auth.py            # Authentication endpoints
    ├── products.py        # Product management endpoints
    └── inventory.py       # Inventory management endpoints
```

## Setup Instructions

### Prerequisites

- Python 3.8+
- PostgreSQL database
- pip (Python package manager)

### 1. Create Virtual Environment

```powershell
cd c:\Users\Vivek\inventory-backend
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 2. Install Dependencies

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configure Environment

Copy `.env.example` to `.env` and update with your settings:

```powershell
cp .env.example .env
```

Edit `.env` with your PostgreSQL connection details:

```
DATABASE_URL=postgresql://username:password@localhost:5432/inventory_db
SECRET_KEY=your-secure-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=False
```

### 4. Create PostgreSQL Database

```sql
CREATE DATABASE inventory_db;
```

### 5. Run the Application

```powershell
python main.py
```

Or with Uvicorn directly:

```powershell
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Documentation

Once running, access:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register a new user |
| POST | `/api/auth/login` | Login and get JWT token |
| GET | `/api/auth/me` | Get current user info (requires auth) |

### Products

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/products` | Create a new product |
| GET | `/api/products` | List all products (paginated) |
| GET | `/api/products/{product_id}` | Get specific product |
| PUT | `/api/products/{product_id}` | Update product |
| DELETE | `/api/products/{product_id}` | Delete product |

### Inventory

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/inventory` | Create inventory item |
| GET | `/api/inventory` | List inventory items (paginated) |
| GET | `/api/inventory/{item_id}` | Get specific inventory item |
| PUT | `/api/inventory/{item_id}` | Update inventory item |
| DELETE | `/api/inventory/{item_id}` | Delete inventory item |
| POST | `/api/inventory/{item_id}/adjust-quantity` | Adjust quantity |

## Example Usage

### 1. Register User

```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "email": "admin@example.com",
    "password": "SecurePassword123"
  }'
```

### 2. Login

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "SecurePassword123"
  }'
```

### 3. Create Product (with token from login)

```bash
curl -X POST http://localhost:8000/api/products \
  -H "Authorization: Bearer {access_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "sku": "PROD001",
    "name": "Laptop",
    "description": "Dell XPS 15",
    "price": 999.99
  }'
```

## Security Considerations

- Change `SECRET_KEY` in production to a strong random value
- Use HTTPS in production
- Restrict CORS origins to your frontend domain
- Set `DEBUG=False` in production
- Use environment variables for sensitive data
- Implement rate limiting for endpoints
- Add logging and monitoring
- Regularly update dependencies

## Development

### Adding New Endpoints

1. Create model in `models.py` if needed
2. Create schema in `schemas.py`
3. Create route file in `routes/` directory
4. Include router in `main.py`

### Running Tests

```powershell
pip install pytest pytest-asyncio httpx
pytest
```

## Troubleshooting

### Database Connection Error

- Verify PostgreSQL is running
- Check DATABASE_URL in `.env`
- Ensure database exists

### Module Import Error

- Verify virtual environment is activated
- Check all files are in correct directories
- Reinstall dependencies: `pip install -r requirements.txt`

### Port Already in Use

Change the port in `.env` or command line:

```powershell
uvicorn main:app --port 8001
```

## License

MIT License - see LICENSE file for details

## Support

For issues or questions, please create an issue in the repository.
