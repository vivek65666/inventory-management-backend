# Deployment Guide

This guide covers deploying the FastAPI Inventory Management System to production environments.

## Pre-Deployment Checklist

- [ ] All tests passing: `pytest`
- [ ] No linting errors: `flake8 .`
- [ ] Code formatted: `black .`
- [ ] Environment variables configured for production
- [ ] Database backups configured
- [ ] SSL/TLS certificates obtained
- [ ] Security review completed
- [ ] Performance testing done

## Environment Setup for Production

### Update .env for Production

```
DATABASE_URL=postgresql://prod_user:strong_password@db.example.com:5432/inventory_prod
SECRET_KEY=your-extremely-secure-random-key-32-characters-minimum
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=False
```

### Security Hardening

1. **Generate Strong Secret Key:**
   ```powershell
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

2. **Database User Permissions:**
   ```sql
   CREATE USER prod_user WITH PASSWORD 'strong_password';
   CREATE DATABASE inventory_prod OWNER prod_user;
   GRANT CONNECT ON DATABASE inventory_prod TO prod_user;
   GRANT USAGE ON SCHEMA public TO prod_user;
   GRANT CREATE ON SCHEMA public TO prod_user;
   ```

3. **Enable HTTPS:**
   - Obtain SSL certificate (Let's Encrypt, AWS Certificate Manager, etc.)
   - Configure reverse proxy (Nginx, Apache, or cloud load balancer)

## Deployment Methods

### Method 1: Docker Deployment

#### Create Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Build and Run Docker Container

```powershell
# Build image
docker build -t inventory-api:latest .

# Run container
docker run -d \
  --name inventory-api \
  -p 8000:8000 \
  --env-file .env \
  inventory-api:latest

# View logs
docker logs inventory-api -f
```

### Method 2: Traditional Server Deployment

#### 1. On Linux/Ubuntu Server

```bash
# Install Python and dependencies
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-dev postgresql-client

# Clone/download project
git clone <repository> /opt/inventory-api
cd /opt/inventory-api

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with production values
nano .env
```

#### 2. Set Up Systemd Service

Create `/etc/systemd/system/inventory-api.service`:

```ini
[Unit]
Description=Inventory Management API
After=network.target postgresql.service

[Service]
Type=notify
User=inventory
WorkingDirectory=/opt/inventory-api
Environment="PATH=/opt/inventory-api/venv/bin"
ExecStart=/opt/inventory-api/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Start and enable service:

```bash
sudo systemctl daemon-reload
sudo systemctl start inventory-api
sudo systemctl enable inventory-api
sudo systemctl status inventory-api
```

### Method 3: Cloud Deployment

#### AWS (Elastic Container Service)

1. Create ECR repository
2. Build and push Docker image
3. Create ECS task definition
4. Create ECS service
5. Configure Application Load Balancer

#### Azure (App Service)

1. Create Azure App Service (Python runtime)
2. Configure application settings (equivalent to .env)
3. Set up Azure Database for PostgreSQL
4. Deploy via Git, Docker, or CI/CD

#### Google Cloud (Cloud Run)

1. Create Dockerfile
2. Build and push to Google Container Registry
3. Deploy to Cloud Run
4. Set environment variables in Cloud Run configuration

## Reverse Proxy Configuration

### Nginx Configuration

```nginx
upstream inventory_api {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name api.example.com;
    
    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name api.example.com;
    
    # SSL certificates
    ssl_certificate /etc/letsencrypt/live/api.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.example.com/privkey.pem;
    
    # SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    
    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    
    client_max_body_size 10M;
    
    location / {
        proxy_pass http://inventory_api;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Database Migration

### Using Alembic (Optional Setup)

For production database migrations:

```bash
pip install alembic
alembic init alembic
# Configure alembic/env.py
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

## Monitoring & Logging

### Configure Application Logging

Add to `main.py`:

```python
import logging
from pythonjsonlogger import jsonlogger

# Setup JSON logging for production
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger = logging.getLogger()
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)
```

### Health Check Monitoring

Monitor using health endpoint:

```bash
curl https://api.example.com/health
```

### Log Aggregation

- **ELK Stack** (Elasticsearch, Logstash, Kibana)
- **Datadog**
- **New Relic**
- **CloudWatch** (AWS)
- **Application Insights** (Azure)

## Performance Optimization

1. **Database Connection Pooling:**
   ```python
   # In database.py
   engine = create_engine(
       settings.database_url,
       pool_size=20,
       max_overflow=40,
   )
   ```

2. **Caching:**
   ```bash
   pip install redis
   # Add Redis caching for frequently accessed data
   ```

3. **Rate Limiting:**
   ```bash
   pip install slowapi
   # Configure rate limiting in main.py
   ```

4. **Database Indexing:**
   ```sql
   CREATE INDEX idx_users_username ON users(username);
   CREATE INDEX idx_products_sku ON products(sku);
   CREATE INDEX idx_inventory_product ON inventory_items(product_id);
   ```

## Backup Strategy

### Automated PostgreSQL Backups

```bash
# Daily backup script
#!/bin/bash
BACKUP_DIR="/backups/postgresql"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
pg_dump -h localhost -U prod_user -d inventory_prod > $BACKUP_DIR/backup_$TIMESTAMP.sql
gzip $BACKUP_DIR/backup_$TIMESTAMP.sql

# Keep only last 7 days
find $BACKUP_DIR -name "backup_*.sql.gz" -mtime +7 -delete
```

### Cloud Backup Services

- **AWS RDS Automated Backups**
- **Azure Database Backup**
- **Google Cloud SQL Backups**

## Scaling Considerations

### Horizontal Scaling

1. Load balancer (distribute requests)
2. Multiple API instances
3. Centralized PostgreSQL database
4. Cache layer (Redis)

### Vertical Scaling

1. Increase server resources
2. Optimize database queries
3. Add indexing
4. Connection pooling

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  test-and-deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.11
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Run tests
      run: pytest
    
    - name: Run linting
      run: flake8 .
    
    - name: Deploy to production
      run: |
        # Your deployment script here
        bash deploy.sh
```

## Troubleshooting

### Common Issues

1. **Database Connection Timeout**
   - Check PostgreSQL is running
   - Verify firewall rules
   - Check connection pool settings

2. **High Memory Usage**
   - Monitor connection pool
   - Review query performance
   - Implement caching

3. **Slow API Response**
   - Add database indexes
   - Enable query caching
   - Profile code with APM tools

## Rollback Plan

1. Keep previous version deployed
2. Monitor application metrics
3. Quick rollback procedure documented
4. Database migration reversibility tested

## Post-Deployment

1. Monitor error rates and response times
2. Check application and database logs
3. Verify all endpoints functional
4. Confirm security headers present
5. Test backup and restore procedures
6. Document deployment process

---

**Happy deploying!** 🚀
