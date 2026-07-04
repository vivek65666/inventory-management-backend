"""Tests for product endpoints."""
import pytest
from fastapi import status


class TestProducts:
    """Test suite for product management endpoints."""

    def test_create_product(self, client, headers):
        """Test creating a new product."""
        response = client.post(
            "/api/products",
            headers=headers,
            json={
                "sku": "PROD001",
                "name": "Laptop",
                "description": "High-performance laptop",
                "price": 999.99
            }
        )
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["sku"] == "PROD001"
        assert data["name"] == "Laptop"
        assert data["price"] == 999.99

    def test_create_product_duplicate_sku(self, client, headers):
        """Test creating product with duplicate SKU."""
        # Create first product
        client.post(
            "/api/products",
            headers=headers,
            json={
                "sku": "DUPLICATE",
                "name": "Product 1",
                "price": 100.0
            }
        )

        # Try creating another with same SKU
        response = client.post(
            "/api/products",
            headers=headers,
            json={
                "sku": "DUPLICATE",
                "name": "Product 2",
                "price": 200.0
            }
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_product_without_auth(self, client):
        """Test creating product without authentication."""
        response = client.post(
            "/api/products",
            json={
                "sku": "PROD001",
                "name": "Laptop",
                "price": 999.99
            }
        )
        assert response.status_code == 401

    def test_list_products(self, client, headers):
        """Test listing products."""
        # Create a product
        client.post(
            "/api/products",
            headers=headers,
            json={
                "sku": "PROD001",
                "name": "Product 1",
                "price": 100.0
            }
        )

        # List products
        response = client.get(
            "/api/products",
            headers=headers
        )
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) >= 1

    def test_list_products_with_pagination(self, client, headers):
        """Test listing products with pagination."""
        # Create multiple products
        for i in range(15):
            client.post(
                "/api/products",
                headers=headers,
                json={
                    "sku": f"PROD{i:03d}",
                    "name": f"Product {i}",
                    "price": 100.0 + i
                }
            )

        # Get first page
        response = client.get(
            "/api/products?skip=0&limit=10",
            headers=headers
        )
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 10

    def test_get_product(self, client, headers):
        """Test getting a specific product."""
        # Create product
        create_response = client.post(
            "/api/products",
            headers=headers,
            json={
                "sku": "PROD001",
                "name": "Laptop",
                "price": 999.99
            }
        )
        product_id = create_response.json()["id"]

        # Get product
        response = client.get(
            f"/api/products/{product_id}",
            headers=headers
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["id"] == product_id

    def test_get_nonexistent_product(self, client, headers):
        """Test getting nonexistent product."""
        response = client.get(
            "/api/products/99999",
            headers=headers
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_product(self, client, headers):
        """Test updating a product."""
        # Create product
        create_response = client.post(
            "/api/products",
            headers=headers,
            json={
                "sku": "PROD001",
                "name": "Original Name",
                "price": 100.0
            }
        )
        product_id = create_response.json()["id"]

        # Update product
        response = client.put(
            f"/api/products/{product_id}",
            headers=headers,
            json={
                "name": "Updated Name",
                "price": 150.0
            }
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["name"] == "Updated Name"
        assert data["price"] == 150.0

    def test_delete_product(self, client, headers):
        """Test deleting a product."""
        # Create product
        create_response = client.post(
            "/api/products",
            headers=headers,
            json={
                "sku": "PROD001",
                "name": "To Delete",
                "price": 100.0
            }
        )
        product_id = create_response.json()["id"]

        # Delete product
        response = client.delete(
            f"/api/products/{product_id}",
            headers=headers
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Verify deletion
        get_response = client.get(
            f"/api/products/{product_id}",
            headers=headers
        )
        assert get_response.status_code == status.HTTP_404_NOT_FOUND
