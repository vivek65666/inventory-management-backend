"""
Comprehensive CRUD and Authorization Tests for Inventory Management API

This test suite validates:
1. Complete CRUD (Create, Read, Update, Delete) operations
2. Authorization enforcement for authenticated endpoints
3. Unauthorized user prevention from modifying inventory
"""
import pytest
from fastapi import status


class TestProductCRUDOperations:
    """Test suite for CRUD operations on products."""

    def test_create_product_with_auth(self, client, headers):
        """Test creating a product with proper authentication."""
        response = client.post(
            "/api/products",
            headers=headers,
            json={
                "sku": "CRUD-PROD-001",
                "name": "CRUD Test Product",
                "description": "Product for testing",
                "price": 299.99
            }
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["name"] == "CRUD Test Product"
        assert response.json()["price"] == 299.99

    def test_read_product_with_auth(self, client, headers):
        """Test reading a product with proper authentication."""
        # Create product
        create_response = client.post(
            "/api/products",
            headers=headers,
            json={
                "sku": "READ-TEST-001",
                "name": "Read Test Product",
                "price": 199.99
            }
        )
        product_id = create_response.json()["id"]

        # Read product
        read_response = client.get(
            f"/api/products/{product_id}",
            headers=headers
        )
        assert read_response.status_code == status.HTTP_200_OK
        assert read_response.json()["id"] == product_id

    def test_update_product_with_auth(self, client, headers):
        """Test updating a product with proper authentication."""
        # Create product
        create_response = client.post(
            "/api/products",
            headers=headers,
            json={
                "sku": "UPDATE-TEST-001",
                "name": "Original Name",
                "price": 99.99
            }
        )
        product_id = create_response.json()["id"]

        # Update product
        update_response = client.put(
            f"/api/products/{product_id}",
            headers=headers,
            json={
                "name": "Updated Name",
                "price": 149.99
            }
        )
        assert update_response.status_code == status.HTTP_200_OK
        assert update_response.json()["name"] == "Updated Name"
        assert update_response.json()["price"] == 149.99

    def test_delete_product_with_auth(self, client, headers):
        """Test deleting a product with proper authentication."""
        # Create product
        create_response = client.post(
            "/api/products",
            headers=headers,
            json={
                "sku": "DELETE-TEST-001",
                "name": "To Delete",
                "price": 199.99
            }
        )
        product_id = create_response.json()["id"]

        # Delete product
        delete_response = client.delete(
            f"/api/products/{product_id}",
            headers=headers
        )
        assert delete_response.status_code == status.HTTP_204_NO_CONTENT

        # Verify deletion
        verify_response = client.get(
            f"/api/products/{product_id}",
            headers=headers
        )
        assert verify_response.status_code == status.HTTP_404_NOT_FOUND


class TestInventoryCRUDOperations:
    """Test suite for CRUD operations on inventory items."""

    def _create_product(self, client, headers):
        """Helper to create a product."""
        response = client.post(
            "/api/products",
            headers=headers,
            json={
                "sku": f"TEST-{id(client)}",
                "name": "Test Product",
                "price": 299.99
            }
        )
        return response.json()["id"]

    def test_create_inventory_with_auth(self, client, headers):
        """Test creating an inventory item with proper authentication."""
        product_id = self._create_product(client, headers)

        response = client.post(
            "/api/inventory",
            headers=headers,
            json={
                "product_id": product_id,
                "quantity": 100,
                "warehouse_location": "A-1-01"
            }
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["quantity"] == 100

    def test_read_inventory_with_auth(self, client, headers):
        """Test reading an inventory item with proper authentication."""
        product_id = self._create_product(client, headers)

        create_response = client.post(
            "/api/inventory",
            headers=headers,
            json={
                "product_id": product_id,
                "quantity": 75
            }
        )
        inventory_id = create_response.json()["id"]

        read_response = client.get(
            f"/api/inventory/{inventory_id}",
            headers=headers
        )
        assert read_response.status_code == status.HTTP_200_OK
        assert read_response.json()["id"] == inventory_id

    def test_update_inventory_with_auth(self, client, headers):
        """Test updating an inventory item with proper authentication."""
        product_id = self._create_product(client, headers)

        create_response = client.post(
            "/api/inventory",
            headers=headers,
            json={
                "product_id": product_id,
                "quantity": 50
            }
        )
        inventory_id = create_response.json()["id"]

        update_response = client.put(
            f"/api/inventory/{inventory_id}",
            headers=headers,
            json={"quantity": 100}
        )
        assert update_response.status_code == status.HTTP_200_OK
        assert update_response.json()["quantity"] == 100

    def test_delete_inventory_with_auth(self, client, headers):
        """Test deleting an inventory item with proper authentication."""
        product_id = self._create_product(client, headers)

        create_response = client.post(
            "/api/inventory",
            headers=headers,
            json={
                "product_id": product_id,
                "quantity": 50
            }
        )
        inventory_id = create_response.json()["id"]

        delete_response = client.delete(
            f"/api/inventory/{inventory_id}",
            headers=headers
        )
        assert delete_response.status_code == status.HTTP_204_NO_CONTENT

        verify_response = client.get(
            f"/api/inventory/{inventory_id}",
            headers=headers
        )
        assert verify_response.status_code == status.HTTP_404_NOT_FOUND


class TestUnauthorizedInventoryModification:
    """Test suite for preventing unauthorized inventory modifications."""

    def _create_test_inventory(self, client, headers):
        """Helper to create a test product and inventory."""
        product_response = client.post(
            "/api/products",
            headers=headers,
            json={
                "sku": f"UNAUTH-TEST-{id(client)}",
                "name": "Unauthorized Test",
                "price": 199.99
            }
        )
        product_id = product_response.json()["id"]

        inventory_response = client.post(
            "/api/inventory",
            headers=headers,
            json={
                "product_id": product_id,
                "quantity": 100
            }
        )
        return inventory_response.json()["id"], product_id

    def test_unauthorized_cannot_create_inventory(self, client):
        """Test that unauthorized users cannot create inventory."""
        response = client.post(
            "/api/inventory",
            json={
                "product_id": 1,
                "quantity": 50
            }
        )
        # Should get 403 Forbidden or 401 Unauthorized
        assert response.status_code in [status.HTTP_403_FORBIDDEN, status.HTTP_401_UNAUTHORIZED]

    def test_unauthorized_cannot_update_inventory(self, client, headers):
        """Test that unauthorized users cannot update inventory."""
        inventory_id, _ = self._create_test_inventory(client, headers)

        # Attempt unauthorized update
        response = client.put(
            f"/api/inventory/{inventory_id}",
            json={"quantity": 200}
        )
        assert response.status_code in [status.HTTP_403_FORBIDDEN, status.HTTP_401_UNAUTHORIZED]

        # Verify the inventory wasn't changed by an authorized check
        verify_response = client.get(
            f"/api/inventory/{inventory_id}",
            headers=headers
        )
        assert verify_response.status_code == status.HTTP_200_OK
        assert verify_response.json()["quantity"] == 100  # Original quantity

    def test_unauthorized_cannot_delete_inventory(self, client, headers):
        """Test that unauthorized users cannot delete inventory."""
        inventory_id, _ = self._create_test_inventory(client, headers)

        # Attempt unauthorized delete
        response = client.delete(f"/api/inventory/{inventory_id}")
        assert response.status_code in [status.HTTP_403_FORBIDDEN, status.HTTP_401_UNAUTHORIZED]

        # Verify inventory still exists
        verify_response = client.get(
            f"/api/inventory/{inventory_id}",
            headers=headers
        )
        assert verify_response.status_code == status.HTTP_200_OK

    def test_invalid_token_blocked_from_inventory_update(self, client, headers):
        """Test that invalid tokens are blocked from updating inventory."""
        inventory_id, _ = self._create_test_inventory(client, headers)

        # Attempt update with invalid token
        response = client.put(
            f"/api/inventory/{inventory_id}",
            headers={"Authorization": "Bearer invalid_token_xyz"},
            json={"quantity": 150}
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_unauthorized_cannot_create_product(self, client):
        """Test that unauthorized users cannot create products."""
        response = client.post(
            "/api/products",
            json={
                "sku": "NOAUTH-001",
                "name": "Unauthorized Product",
                "price": 99.99
            }
        )
        assert response.status_code in [status.HTTP_403_FORBIDDEN, status.HTTP_401_UNAUTHORIZED]

    def test_unauthorized_cannot_update_product(self, client, headers):
        """Test that unauthorized users cannot update products."""
        # Create product with auth
        create_response = client.post(
            "/api/products",
            headers=headers,
            json={
                "sku": "PROD-UNAUTH-001",
                "name": "Original",
                "price": 199.99
            }
        )
        product_id = create_response.json()["id"]

        # Attempt unauthorized update
        response = client.put(
            f"/api/products/{product_id}",
            json={"name": "Unauthorized Change"}
        )
        assert response.status_code in [status.HTTP_403_FORBIDDEN, status.HTTP_401_UNAUTHORIZED]

    def test_unauthorized_cannot_delete_product(self, client, headers):
        """Test that unauthorized users cannot delete products."""
        # Create product with auth
        create_response = client.post(
            "/api/products",
            headers=headers,
            json={
                "sku": "PROD-DEL-UNAUTH-001",
                "name": "To Delete",
                "price": 199.99
            }
        )
        product_id = create_response.json()["id"]

        # Attempt unauthorized delete
        response = client.delete(f"/api/products/{product_id}")
        assert response.status_code in [status.HTTP_403_FORBIDDEN, status.HTTP_401_UNAUTHORIZED]

        # Verify product still exists
        verify_response = client.get(
            f"/api/products/{product_id}",
            headers=headers
        )
        assert verify_response.status_code == status.HTTP_200_OK


class TestSecurityBoundaries:
    """Test suite for security boundary enforcement."""

    def test_missing_auth_header_blocked(self, client):
        """Test that missing auth header blocks access to inventory list."""
        response = client.get("/api/inventory")
        assert response.status_code in [status.HTTP_403_FORBIDDEN, status.HTTP_401_UNAUTHORIZED]

    def test_malformed_auth_header_rejected(self, client):
        """Test that malformed auth headers are rejected."""
        response = client.get(
            "/api/inventory",
            headers={"Authorization": "NotABearerToken"}
        )
        assert response.status_code in [status.HTTP_400_BAD_REQUEST, status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]

    def test_read_operations_require_auth(self, client, headers):
        """Test that read operations also require authentication."""
        # Create item with auth first
        client.post(
            "/api/products",
            headers=headers,
            json={
                "sku": "READ-AUTH-001",
                "name": "Read Auth",
                "price": 99.99
            }
        )

        # Try to read products without auth
        response = client.get("/api/products")
        assert response.status_code in [status.HTTP_403_FORBIDDEN, status.HTTP_401_UNAUTHORIZED]
