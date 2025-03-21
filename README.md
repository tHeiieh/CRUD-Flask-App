# RESTful API Documentation

## Overview
This API provides user authentication using JWT and CRUD operations for managing products.

### Base URL
```
http://127.0.0.1:5000
```

---
## Authentication
All protected routes require a **JWT token** in the `Authorization` header:
```
Authorization: Bearer your_jwt_token_here
```

## Endpoints

### 1️⃣ User Authentication

#### ✅ User Signup
**Endpoint:** `POST /signup`
**Description:** Registers a new user.

**Request Body:**
```json
{
    "name": "John Doe",
    "username": "johndoe",
    "password": "securepassword123"
}
```
**Response:**
```json
{
    "message": "User registered successfully"
}
```

---

#### ✅ User Login
**Endpoint:** `POST /login`
**Description:** Authenticates a user and returns a JWT token.

**Request Body:**
```json
{
    "username": "johndoe",
    "password": "securepassword123"
}
```
**Response:**
```json
{
    "token": "your_jwt_token_here"
}
```

---

### 2️⃣ User Management

#### ✅ Update User
**Endpoint:** `PUT /users/{id}`
**Description:** Updates user details (Requires JWT).

**Request Body:**
```json
{
    "name": "Updated Name",
    "username": "newusername"
}
```
**Response:**
```json
{
    "message": "User updated successfully"
}
```

---

### 3️⃣ Product Management

#### ✅ Create Product
**Endpoint:** `POST /products`
**Description:** Adds a new product (Requires JWT).

**Request Body:**
```json
{
    "pname": "Laptop",
    "description": "High-end gaming laptop",
    "price": 1200.50,
    "stock": 10
}
```
**Response:**
```json
{
    "message": "Product added successfully"
}
```

---

#### ✅ Get All Products
**Endpoint:** `GET /products`
**Description:** Retrieves a list of all products (Requires JWT).

**Response:**
```json
[
    {
        "id": 1,
        "name": "Laptop",
        "price": 1200.50,
        "stock": 10
    }
]
```

---

#### ✅ Get a Single Product
**Endpoint:** `GET /products/{pid}`
**Description:** Retrieves details of a specific product (Requires JWT).

**Response:**
```json
{
    "id": 1,
    "name": "Laptop",
    "description": "High-end gaming laptop",
    "price": 1200.50,
    "stock": 10
}
```

---

#### ✅ Update Product
**Endpoint:** `PUT /products/{pid}`
**Description:** Updates a product's details (Requires JWT).

**Request Body:**
```json
{
    "pname": "Updated Laptop",
    "description": "Updated description",
    "price": 1100.00,
    "stock": 5
}
```
**Response:**
```json
{
    "message": "Product updated successfully"
}
```

---

#### ✅ Delete Product
**Endpoint:** `DELETE /products/{pid}`
**Description:** Deletes a product (Requires JWT).

**Response:**
```json
{
    "message": "Product deleted successfully"
}
```

---

### 📌 Notes
- Use **Postman** or a similar tool to test the API.
- Ensure **Authorization Header** is set for JWT-protected routes.
- Use **valid JSON format** in request bodies.

🚀 Happy Coding! Let me know if you need further modifications.

