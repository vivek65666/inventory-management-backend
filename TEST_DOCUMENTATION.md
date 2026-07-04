# Automated Unit Tests Documentation

## Overview

The test suite includes comprehensive pytest-based unit tests that validate:
- ✅ Complete CRUD operations on all resources
- ✅ Authorization enforcement for protected endpoints
- ✅ Prevention of unauthorized inventory modifications
- ✅ Token validation and security

## Test File: `test_crud_and_authorization.py`

### Test Classes & Coverage

#### 1. `TestCRUDOperations`
**Purpose:** Validate complete Create, Read, Update, Delete cycles

**Tests:**

| Test Name | What It Validates | Assertions |
|-----------|-------------------|-----------|
| `test_user_crud_cycle` | User registration, login, and retrieval | User created, logged in, retrieved successfully |
| `test_product_crud_cycle` | Product creation, retrieval, updates, deletion | CRUD operations complete without errors; deletion verified |
| `test_inventory_crud_cycle` | Inventory item CRUD operations | All CRUD operations succeed; item is properly deleted |

**Key Validations:**
- Resources are created with correct data
- Resources can be retrieved by ID
- Updates modify only specified fields
- Deletions are verified (404 on subsequent GET)

#### 2. `TestAuthorizationEnforcement`
**Purpose:** Verify unauthorized users are blocked from operations

**Tests:**

| Test Name | What It Validates | Expected Behavior |
|-----------|-------------------|-------------------|
| `test_unauthorized_user_cannot_create_inventory` | Unauthenticated inventory creation | Returns 403 Forbidden |
| `test_unauthorized_user_cannot_update_inventory` | Unauthenticated inventory update | Returns 403 Forbidden |
| `test_unauthorized_user_cannot_delete_inventory` | Unauthenticated inventory deletion | Returns 403 Forbidden; item remains |
| `test_invalid_token_blocked_from_updating_inventory` | Invalid JWT token usage | Returns 401 Unauthorized |
| `test_unauthorized_user_cannot_create_product` | Unauthenticated product creation | Returns 403 Forbidden |
| `test_unauthorized_user_cannot_update_product` | Unauthenticated product update | Returns 403 Forbidden |
| `test_unauthorized_user_cannot_delete_product` | Unauthenticated product deletion | Returns 403 Forbidden; item remains |

**Security Validations:**
- Missing authentication token returns 403
- Invalid JWT tokens return 401
- Unauthorized users cannot modify protected resources
- Protected resources remain intact after failed deletion attempts

#### 3. `TestInventoryOperationsSecured`
**Purpose:** Focused security tests for inventory-specific operations

**Tests:**

| Test Name | What It Validates | Expected Behavior |
|-----------|-------------------|-------------------|
| `test_only_authenticated_user_can_adjust_quantity` | Quantity adjustment requires auth | Unauthorized: 403; Authorized: 200 with updated quantity |
| `test_authorized_inventory_list_requires_token` | Inventory list requires authentication | Unauthenticated: 403; Authenticated: 200 with data |
| `test_authorized_product_list_requires_token` | Product list requires authentication | Unauthenticated: 403; Authenticated: 200 with data |
| `test_token_expiration_blocks_access` | Expired/malformed tokens block access | Returns 401 Unauthorized |

**Inventory Security Focus:**
- Quantity adjustments require valid authentication
- List endpoints enforce authentication
- Malformed tokens are rejected
- Only authenticated users can view and modify inventory

## Running the Tests

### Run All Tests

```powershell
pytest
```

### Run Specific Test File

```powershell
pytest tests/test_crud_and_authorization.py -v
```

### Run Specific Test Class

```powershell
pytest tests/test_crud_and_authorization.py::TestCRUDOperations -v
pytest tests/test_crud_and_authorization.py::TestAuthorizationEnforcement -v
pytest tests/test_crud_and_authorization.py::TestInventoryOperationsSecured -v
```

### Run Specific Test

```powershell
pytest tests/test_crud_and_authorization.py::TestCRUDOperations::test_product_crud_cycle -v
```

### Run with Coverage Report

```powershell
pytest --cov=. --cov-report=html --cov-report=term
```

Coverage report will be generated in `htmlcov/index.html`

### Run with Detailed Output

```powershell
pytest -v -s
```

The `-s` flag shows print statements and log output

### Run Tests Matching a Pattern

```powershell
pytest -k "authorization" -v
pytest -k "crud" -v
pytest -k "unauthorized" -v
```

## Test Results Explanation

### Expected Output

When all tests pass, you should see:

```
tests/test_crud_and_authorization.py::TestCRUDOperations::test_user_crud_cycle PASSED
tests/test_crud_and_authorization.py::TestCRUDOperations::test_product_crud_cycle PASSED
tests/test_crud_and_authorization.py::TestCRUDOperations::test_inventory_crud_cycle PASSED
tests/test_crud_and_authorization.py::TestAuthorizationEnforcement::test_unauthorized_user_cannot_create_inventory PASSED
tests/test_crud_and_authorization.py::TestAuthorizationEnforcement::test_unauthorized_user_cannot_update_inventory PASSED
tests/test_crud_and_authorization.py::TestAuthorizationEnforcement::test_unauthorized_user_cannot_delete_inventory PASSED
tests/test_crud_and_authorization.py::TestAuthorizationEnforcement::test_invalid_token_blocked_from_updating_inventory PASSED
tests/test_crud_and_authorization.py::TestAuthorizationEnforcement::test_unauthorized_user_cannot_create_product PASSED
tests/test_crud_and_authorization.py::TestAuthorizationEnforcement::test_unauthorized_user_cannot_update_product PASSED
tests/test_crud_and_authorization.py::TestAuthorizationEnforcement::test_unauthorized_user_cannot_delete_product PASSED
tests/test_crud_and_authorization.py::TestInventoryOperationsSecured::test_only_authenticated_user_can_adjust_quantity PASSED
tests/test_crud_and_authorization.py::TestInventoryOperationsSecured::test_authorized_inventory_list_requires_token PASSED
tests/test_crud_and_authorization.py::TestInventoryOperationsSecured::test_authorized_product_list_requires_token PASSED
tests/test_crud_and_authorization.py::TestInventoryOperationsSecured::test_token_expiration_blocks_access PASSED
========================= 14 passed in 0.45s =========================
```

## Test Execution Prerequisites

1. **Virtual Environment Activated:**
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

2. **Dependencies Installed:**
   ```powershell
   pip install -r requirements.txt
   ```

3. **Database Configured:**
   - Tests use SQLite in-memory database (configured in `conftest.py`)
   - No external database needed for testing

## Test Coverage Summary

### What's Tested

✅ **User Operations:**
- Registration
- Login
- Authentication token retrieval
- Current user information retrieval

✅ **Product CRUD:**
- Create products with validation
- Read products by ID
- Update product details
- Delete products (with verification)

✅ **Inventory CRUD:**
- Create inventory items
- Read inventory items
- Update inventory details
- Delete inventory items
- Adjust quantities

✅ **Authorization & Security:**
- Missing authentication tokens (403)
- Invalid tokens (401)
- Expired token simulation
- Unauthorized create operations blocked
- Unauthorized read operations blocked
- Unauthorized update operations blocked
- Unauthorized delete operations blocked

### HTTP Status Codes Validated

| Status | Scenario |
|--------|----------|
| 200 OK | Successful operations (GET, POST updates, PUT) |
| 201 Created | Successful resource creation (POST) |
| 204 No Content | Successful deletion (DELETE) |
| 400 Bad Request | Invalid input or negative quantity |
| 401 Unauthorized | Invalid/expired JWT token |
| 403 Forbidden | Missing authentication token |
| 404 Not Found | Resource doesn't exist |

## Continuous Integration

### GitHub Actions Example

Add to `.github/workflows/tests.yml`:

```yaml
name: Run Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: pytest -v --cov=. --cov-report=xml
      - uses: codecov/codecov-action@v2
```

## Best Practices in These Tests

1. **Isolation:** Each test is independent and doesn't rely on others
2. **Fixtures:** Reusable `client` and `auth_token` fixtures from `conftest.py`
3. **Descriptive Names:** Test names clearly describe what's being validated
4. **Comprehensive Assertions:** Multiple assertions verify complete behavior
5. **Security Focus:** Authorization tests verify security boundaries
6. **Cleanup:** Database auto-cleaned between tests (SQLite in-memory)
7. **Error Cases:** Tests include both happy path and error scenarios

## Troubleshooting Tests

### Issue: "ModuleNotFoundError: No module named 'pytest'"

**Solution:**
```powershell
pip install pytest pytest-asyncio httpx
```

### Issue: "Address already in use"

**Solution:** Tests use in-memory SQLite, shouldn't conflict. If it does:
```powershell
# Kill any hanging processes
Get-Process python | Stop-Process -Force
```

### Issue: "FAILED - AssertionError"

**Solution:** Check the assertion message to see what failed. Example:
```
AssertionError: assert 403 == 200
  Expected authorized access (200), but got forbidden (403)
```

Verify that:
- Authentication token is being passed correctly
- User is properly registered before login
- Bearer token format is correct

### Issue: Database Lock

**Solution:** This shouldn't happen with SQLite in-memory, but if it does:
```powershell
# Restart Python kernel
python
```

## Running Full Test Suite

For comprehensive validation before deployment:

```powershell
# Install all dependencies including test tools
pip install -r requirements.txt

# Run all tests with coverage
pytest --cov=. --cov-report=html --cov-report=term -v

# View coverage
start htmlcov/index.html

# Run specific categories
pytest -k "authorization" -v
pytest -k "crud" -v
pytest tests/test_auth.py tests/test_products.py tests/test_inventory.py -v
```

## Next Steps

1. ✅ Run tests to ensure all functionality works
2. ✅ Review coverage report for any gaps
3. ✅ Add more tests for edge cases as needed
4. ✅ Integrate tests into CI/CD pipeline
5. ✅ Run tests before each deployment

---

**Happy testing!** 🧪
