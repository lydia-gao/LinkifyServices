# Linkify API Documentation

---

## Table of Contents

- [Linkify API Documentation](#linkify-api-documentation)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [API Endpoints](#api-endpoints)
    - [1. User Management Endpoints](#1-user-management-endpoints)
      - [1.1. Register User (Username/Password)](#11-register-user-usernamepassword)
      - [1.2. Register with Google](#12-register-with-google)
      - [1.3. Login (Username/Password)](#13-login-usernamepassword)
      - [1.4. Logout (Client-side)](#14-logout-client-side)
      - [1.5. Get User Profile](#15-get-user-profile)
      - [1.6. Update User Profile](#16-update-user-profile)
    - [2. Short URL Endpoints](#2-short-url-endpoints)
      - [2.1. Create Short URL](#21-create-short-url)
      - [2.2. Redirect from Short URL](#22-redirect-from-short-url)
      - [2.3. Set or Update Alias](#23-set-or-update-alias)
      - [2.4. Get Alias](#24-get-alias)
      - [2.5. Remove Alias](#25-remove-alias)
    - [3. QR Code Endpoints](#3-qr-code-endpoints)
      - [3.1. Generate QR Code](#31-generate-qr-code)
      - [3.2. Get QR Code Image](#32-get-qr-code-image)
      - [3.3. Redirect from QR Code](#33-redirect-from-qr-code)
    - [4. Barcode Endpoints](#4-barcode-endpoints)
      - [4.1. Generate Barcode](#41-generate-barcode)
      - [4.2. Get Barcode Image](#42-get-barcode-image)
      - [4.3. Redirect from Barcode](#43-redirect-from-barcode)
    - [5. History Endpoints](#5-history-endpoints)
      - [5.1. Get URL History](#51-get-url-history)
      - [5.2. Get QR Code History](#52-get-qr-code-history)
      - [5.3. Get Barcode History](#53-get-barcode-history)
    - [6. Analytics Endpoints](#6-analytics-endpoints)
      - [6.1. Get Short URL Analytics](#61-get-short-url-analytics)
      - [6.2. Get QR Code Analytics](#62-get-qr-code-analytics)
      - [6.3. Get Barcode Analytics](#63-get-barcode-analytics)
      - [6.4. Get Aggregated Analytics](#64-get-aggregated-analytics)
  - [Environment Variables](#environment-variables)
  - [Website Title Extraction](#website-title-extraction)

---

## Overview

This document outlines the API endpoints for the Linkify service. Linkify allows users to:

1. **User Management (more features in the future)**

   1. Create user accounts (username/password or Google)
   2. Login and logout via JWT authentication
   3. Manage user profile information

2. **Short URLs**

   1. Create short URLs from long ones with automatic title extraction
   2. Redirect from short URLs to their original destinations

3. **QR Codes**

   1. Generate QR codes from URLs with automatic title extraction
   2. Get QR code images (generated on demand)
   3. Redirect from QR codes to their original destinations

4. **Barcodes**

   1. Generate barcodes from URLs with automatic title extraction
   2. Get barcode images (generated on demand)
   3. Redirect from barcodes to their original destinations

5. **History**

   1. View paginated history of URLs created by a user
   2. View paginated history of QR codes created by a user
   3. View paginated history of barcodes created by a user

6. **Analytics**
   1. View detailed statistics about individual resources
   2. Track usage by location, device, browser, etc.
   3. Access aggregated analytics data for visualization

Each resource (URL, QR code, barcode) automatically extracts and stores the title of the target website for better context in the history and analytics views.

---

## API Endpoints

### 1. User Management Endpoints

#### 1.1. Register User (Username/Password)

**Purpose:** Create a new user account with username and password.

**Endpoint:** `/auth/register`

**Method:** `POST`

**Request Body:**

```json
{
  "username": "lydiagao",
  "email": "lydia@example.com",
  "password": "securepassword123"
}
```

**Response:** (201 Created)

```json
{
  "id": 42,
  "username": "lydiagao",
  "email": "lydia@example.com",
  "created_at": "2025-05-15T14:30:00Z"
}
```

---

#### 1.2. Register with Google

**Purpose:** Create a new user account with Google authentication.

**Endpoint:** `/auth/google`

**Method:** `POST`

**Request Body:**

```json
{
  "token": "google_oauth_token"
}
```

**Response:** (201 Created)

```json
{
  "id": 43,
  "username": "lydiagao",
  "email": "lydia@example.com",
  "created_at": "2025-05-15T14:35:00Z",
  "auth_provider": "google"
}
```

---

#### 1.3. Login (Username/Password)

**Purpose:** Authenticate user and get JWT access token and refresh token.

**Endpoint:** `/auth/login`

**Method:** `POST`

**Request Body:**

```json
{
  "username": "lydiagao",
  "password": "securepassword123"
}
```

**Response:** (200 OK)

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600,
  "user": {
    "id": 42,
    "username": "lydiagao",
    "email": "lydia@example.com"
  }
}
```

---

#### 1.4. Logout (Client-side)

**Purpose:** Client removes tokens from storage. No server-side action required with pure JWT.

**Note:** In a pure JWT implementation, logout is handled client-side by removing the tokens from storage. The frontend application should delete both the access token and refresh token from localStorage or cookies when the user logs out, and then redirect to the login page.

---

#### 1.5. Get User Profile

**Purpose:** Retrieve current user profile information.

**Endpoint:** `/users/me`

**Method:** `GET`

**Headers:**

- Authorization: Bearer {access_token}

**Response:** (200 OK)

```json
{
  "id": 42,
  "username": "lydiagao",
  "email": "lydia@example.com",
  "created_at": "2025-05-15T14:30:00Z",
  "stats": {
    "urls_created": 15,
    "qr_codes_created": 8,
    "barcodes_created": 5
  }
}
```

---

#### 1.6. Update User Profile

**Purpose:** Update user profile information.

**Endpoint:** `/users/me`

**Method:** `PATCH`

**Headers:**

- Authorization: Bearer {access_token}

**Request Body:**

```json
{
  "username": "lydiagao_new",
  "email": "new_lydia@example.com"
}
```

**Response:** (200 OK)

```json
{
  "id": 42,
  "username": "lydiagao_new",
  "email": "new_lydia@example.com",
  "created_at": "2025-05-15T14:30:00Z"
}
```

---

### 2. Short URL Endpoints

#### 2.1. Create Short URL

**Purpose:** Convert a long URL into a short URL with a randomly generated code. Automatically extracts website title.

**Endpoint:** `/shorten/`

**Method:** `POST`

**Headers:**

- Authorization: Bearer {access_token} (optional, for authenticated users)

**Request Body:**

```json
{
  "original_url": "https://example.com/your/long/url",
  "alias": "your-custom-alias" // optional: custom alias (3–30 chars, letters/numbers/_/-)
}
```

**Response:**

- 400 Bad Request if `alias` or `original_url` is invalid.
- 409 Conflict if `alias` is already taken.
- 201 Created:

```json
{
  "original_url": "https://example.com/your/long/url",
  "short_code": "abc123",
  "alias": "your-custom-alias", // present if alias provided
  "short_url": "https://{your-domain}/{alias-or-code}",
  "title": "Example Website Homepage",
  "clicks": 0,
  "user_id": 42,
  "created_at": "2025-05-15T14:30:00Z"
}
```

---

#### 2.2. Redirect from Short URL

**Purpose:** Redirect visitors to the original URL when they use a short link.

**Endpoint:** `/{short_code}`

**Method:** `GET`

**Example:**

- When someone visits `http://localhost:8000/abc123`
- They are redirected to the original URL
- The click counter is incremented

**Response:**

- 307 Temporary Redirect to the original URL
- 404 Not Found if the short code doesn't exist

---

#### 2.3. Set or Update Alias

**Purpose:** Assign or change a custom alias for a short code. Aliases can be set either at creation time (see Create Short URL) or updated later using this endpoint.

**Endpoint:** `/urls/{shortCode}`

**Method:** `PATCH`

**Headers:**

- `Authorization: Bearer {access_token}`

**Request Body:**

```json
{
  "alias": "your-custom-alias"
}
```

**Response:** (200 OK)

```json
{
  "original_url": "https://example.com/your/long/url",
  "short_code": "abc123",
  "alias": "your-custom-alias",
  "short_url": "https://your-domain.com/your-custom-alias",
  "clicks": 0,
  "user_id": 42,
  "created_at": "2025-07-12T00:00:00Z"
}
```

---

#### 2.4. Get Alias

**Purpose:** Retrieve the custom alias for a given short code, if one exists.

**Endpoint:** `/urls/{shortCode}/alias`

**Method:** `GET`

**Headers:**

- `Authorization: Bearer {access_token}`

**Response:** (200 OK)

```json
{
  "short_code": "abc123",
  "alias": "your-custom-alias"
}
```

---

#### 2.5. Remove Alias

**Purpose:** Delete the custom alias and revert to the default randomly generated code.

**Endpoint:** `/urls/{shortCode}/alias`

**Method:** `DELETE`

**Headers:**

- `Authorization: Bearer {access_token}`

**Response:** (204 No Content)

---

### 3. QR Code Endpoints

#### 3.1. Generate QR Code

**Purpose:** Create a QR code from a URL. Automatically extracts website title.

**Endpoint:** `/qrcode/`

**Method:** `POST`

**Headers:**

- Authorization: Bearer {access_token} (optional, for authenticated users)

**Request Body:**

```json
{
  "original_url": "https://example.com/your/long/url"
}
```

**Response:** (201 Created)

```json
{
  "original_url": "https://example.com/your/long/url",
  "qr_code_id": "qr123",
  "qr_code_url": "http://localhost:8000/qrcode/qr123",
  "title": "Example Website Homepage",
  "scans": 0,
  "user_id": 42,
  "created_at": "2025-05-15T14:30:00Z"
}
```

---

#### 3.2. Get QR Code Image

**Purpose:** Retrieve the generated QR code image.

**Endpoint:** `/qrcode/{qr_code_id}/image`

**Method:** `GET`

**Response:**

- QR code image (PNG format)
- 404 Not Found if the QR code ID doesn't exist

---

#### 3.3. Redirect from QR Code

**Purpose:** Redirect visitors to the original URL when they scan a QR code.

**Endpoint:** `/qrcode/{qr_code_id}`

**Method:** `GET`

**Example:**

- When someone scans a QR code that leads to `http://localhost:8000/qrcode/qr123`
- The scan counter is incremented
- They are redirected to the original URL

**Response:**

- 307 Temporary Redirect to the original URL
- 404 Not Found if the QR code ID doesn't exist

---

### 4. Barcode Endpoints

#### 4.1. Generate Barcode

**Purpose:** Create a barcode from a URL. Automatically extracts website title.

**Endpoint:** `/barcode/`

**Method:** `POST`

**Headers:**

- Authorization: Bearer {access_token} (optional, for authenticated users)

**Request Body:**

```json
{
  "original_url": "https://example.com/your/long/url"
}
```

**Response:** (201 Created)

```json
{
  "original_url": "https://example.com/your/long/url",
  "barcode_id": "bar123",
  "barcode_url": "http://localhost:8000/barcode/bar123",
  "title": "Example Website Homepage",
  "scans": 0,
  "user_id": 42,
  "created_at": "2025-05-15T14:30:00Z"
}
```

---

#### 4.2. Get Barcode Image

**Purpose:** Retrieve the generated barcode image.

**Endpoint:** `/barcode/{barcode_id}/image`

**Method:** `GET`

**Response:**

- Barcode image (PNG format)
- 404 Not Found if the barcode ID doesn't exist

---

#### 4.3. Redirect from Barcode

**Purpose:** Redirect visitors to the original URL when they scan a barcode.

**Endpoint:** `/barcode/{barcode_id}`

**Method:** `GET`

**Example:**

- When someone scans a barcode that leads to `http://localhost:8000/barcode/bar123`
- The scan counter is incremented
- They are redirected to the original URL

**Response:**

- 307 Temporary Redirect to the original URL
- 404 Not Found if the barcode ID doesn't exist

---

### 5. History Endpoints

#### 5.1. Get URL History

**Purpose:** Retrieve all shortened URLs created by the current user with pagination.

**Endpoint:** `/urls/history`

**Method:** `GET`

**Headers:**

- Authorization: Bearer {access_token}

**Query Parameters:**

- `page=1` - Page number for pagination (default: 1)
- `limit=20` - Number of items per page (default: 20)
- `sort=created_at|clicks` - Sort field (default: created_at)
- `order=asc|desc` - Sort order (default: desc)

**Response:**

```json
{
  "page": 1,
  "limit": 20,
  "total": 35,
  "urls": [
    {
      "original_url": "https://example.com/your/long/url",
      "short_code": "abc123",
      "short_url": "http://localhost:8000/abc123",
      "title": "Example Website Homepage",
      "clicks": 42,
      "created_at": "2025-05-15T14:30:00Z"
    },
    {
      "original_url": "https://example.com/another/page",
      "short_code": "def456",
      "short_url": "http://localhost:8000/def456",
      "title": "Another Example Page",
      "clicks": 18,
      "created_at": "2025-05-16T10:15:00Z"
    }
  ]
}
```

---

#### 5.2. Get QR Code History

**Purpose:** Retrieve all QR codes created by the current user with pagination.

**Endpoint:** `/qrcodes/history`

**Method:** `GET`

**Headers:**

- Authorization: Bearer {access_token}

**Query Parameters:**

- `page=1` - Page number for pagination (default: 1)
- `limit=20` - Number of items per page (default: 20)
- `sort=created_at|scans` - Sort field (default: created_at)
- `order=asc|desc` - Sort order (default: desc)

**Response:**

```json
{
  "page": 1,
  "limit": 20,
  "total": 22,
  "qrcodes": [
    {
      "original_url": "https://example.com/your/long/url",
      "qr_code_id": "qr123",
      "qr_code_url": "http://localhost:8000/qrcode/qr123",
      "title": "Example Website Homepage",
      "scans": 35,
      "created_at": "2025-05-15T14:30:00Z"
    },
    {
      "original_url": "https://example.com/another/url",
      "qr_code_id": "qr456",
      "qr_code_url": "http://localhost:8000/qrcode/qr456",
      "title": "Another Example Page",
      "scans": 24,
      "created_at": "2025-05-16T10:15:00Z"
    }
  ]
}
```

---

#### 5.3. Get Barcode History

**Purpose:** Retrieve all barcodes created by the current user with pagination.

**Endpoint:** `/barcodes/history`

**Method:** `GET`

**Headers:**

- Authorization: Bearer {access_token}

**Query Parameters:**

- `page=1` - Page number for pagination (default: 1)
- `limit=20` - Number of items per page (default: 20)
- `sort=created_at|scans` - Sort field (default: created_at)
- `order=asc|desc` - Sort order (default: desc)

**Response:**

```json
{
  "page": 1,
  "limit": 20,
  "total": 15,
  "barcodes": [
    {
      "original_url": "https://example.com/your/long/url",
      "barcode_id": "bar123",
      "barcode_url": "http://localhost:8000/barcode/bar123",
      "title": "Example Website Homepage",
      "scans": 28,
      "created_at": "2025-05-15T14:30:00Z"
    },
    {
      "original_url": "https://example.com/another/url",
      "barcode_id": "bar456",
      "barcode_url": "http://localhost:8000/barcode/bar456",
      "title": "Another Example Page",
      "scans": 16,
      "created_at": "2025-05-16T10:15:00Z"
    }
  ]
}
```

---

### 6. Analytics Endpoints

#### 6.1. Get Short URL Analytics

**Purpose:** Retrieve detailed analytics about a short URL.

**Endpoint:** `/analytics/url/{short_code}`

**Method:** `GET`

**Headers:**

- Authorization: Bearer {access_token} (required for user's URLs)

**Response:**

```json
{
  "original_url": "https://example.com/your/long/url",
  "short_code": "abc123",
  "short_url": "http://localhost:8000/abc123",
  "title": "Example Website Homepage",
  "created_at": "2025-05-15T14:30:00Z",
  "owner": {
    "id": 42,
    "username": "lydiagao"
  },
  "clicks": 42,
  "click_data": {
    "daily": [
      { "date": "2025-05-15", "clicks": 10 },
      { "date": "2025-05-16", "clicks": 15 },
      { "date": "2025-05-17", "clicks": 17 }
    ],
    "referrers": [
      { "source": "direct", "count": 20 },
      { "source": "twitter.com", "count": 12 },
      { "source": "facebook.com", "count": 10 }
    ],
    "browsers": [
      { "name": "Chrome", "count": 25 },
      { "name": "Firefox", "count": 10 },
      { "name": "Safari", "count": 7 }
    ],
    "locations": [
      { "country": "United States", "count": 20 },
      { "country": "Canada", "count": 12 },
      { "country": "United Kingdom", "count": 10 }
    ],
    "devices": [
      { "type": "desktop", "count": 25 },
      { "type": "mobile", "count": 15 },
      { "type": "tablet", "count": 2 }
    ]
  }
}
```

---

#### 6.2. Get QR Code Analytics

**Purpose:** Retrieve detailed analytics about a QR code.

**Endpoint:** `/analytics/qrcode/{qr_code_id}`

**Method:** `GET`

**Headers:**

- Authorization: Bearer {access_token} (required for user's QR codes)

**Response:**

```json
{
  "original_url": "https://example.com/your/long/url",
  "qr_code_id": "qr123",
  "qr_code_url": "http://localhost:8000/qrcode/qr123",
  "title": "Example Website Homepage",
  "created_at": "2025-05-15T14:30:00Z",
  "owner": {
    "id": 42,
    "username": "lydiagao"
  },
  "scans": 35,
  "scan_data": {
    "daily": [
      { "date": "2025-05-15", "scans": 8 },
      { "date": "2025-05-16", "scans": 12 },
      { "date": "2025-05-17", "scans": 15 }
    ],
    "devices": [
      { "type": "iOS", "count": 20 },
      { "type": "Android", "count": 15 }
    ],
    "locations": [
      { "country": "United States", "count": 18 },
      { "country": "Canada", "count": 10 },
      { "country": "United Kingdom", "count": 7 }
    ]
  }
}
```

---

#### 6.3. Get Barcode Analytics

**Purpose:** Retrieve detailed analytics about a barcode.

**Endpoint:** `/analytics/barcode/{barcode_id}`

**Method:** `GET`

**Headers:**

- Authorization: Bearer {access_token} (required for user's barcodes)

**Response:**

```json
{
  "original_url": "https://example.com/your/long/url",
  "barcode_id": "bar123",
  "barcode_url": "http://localhost:8000/barcode/bar123",
  "title": "Example Website Homepage",
  "created_at": "2025-05-15T14:30:00Z",
  "owner": {
    "id": 42,
    "username": "lydiagao"
  },
  "scans": 28,
  "scan_data": {
    "daily": [
      { "date": "2025-05-15", "scans": 5 },
      { "date": "2025-05-16", "scans": 10 },
      { "date": "2025-05-17", "scans": 13 }
    ],
    "devices": [
      { "type": "iOS", "count": 16 },
      { "type": "Android", "count": 12 }
    ],
    "locations": [
      { "country": "United States", "count": 15 },
      { "country": "Canada", "count": 8 },
      { "country": "United Kingdom", "count": 5 }
    ]
  }
}
```

---

#### 6.4. Get Aggregated Analytics

**Purpose:** Retrieve aggregated analytics across all URLs, QR codes, and barcodes.

**Endpoint:** `/analytics/summary`

**Method:** `GET`

**Headers:**

- Authorization: Bearer {access_token}

**Query Parameters:**

- `period=day|week|month|year` - Time period for analytics (default: month)
- `start_date=YYYY-MM-DD` - Start date for custom range (optional)
- `end_date=YYYY-MM-DD` - End date for custom range (optional)

**Response:**

```json
{
  "period": "month",
  "start_date": "2025-04-17",
  "end_date": "2025-05-17",
  "total_urls": 125,
  "total_qrcodes": 84,
  "total_barcodes": 62,
  "total_clicks": 3542,
  "total_qr_scans": 1846,
  "total_barcode_scans": 1253,
  "daily_activity": [
    {
      "date": "2025-05-17",
      "clicks": 152,
      "qr_scans": 87,
      "barcode_scans": 65
    }
  ],
  "top_urls": [
    {
      "short_code": "abc123",
      "original_url": "https://example.com/popular-page",
      "title": "Popular Example Page",
      "clicks": 328
    }
  ],
  "top_qrcodes": [
    {
      "qr_code_id": "qr789",
      "original_url": "https://example.com/popular-qr-page",
      "title": "Popular QR Page",
      "scans": 187
    }
  ],
  "top_barcodes": [
    {
      "barcode_id": "bar456",
      "original_url": "https://example.com/popular-barcode-page",
      "title": "Popular Barcode Page",
      "scans": 142
    }
  ]
}
```

## Environment Variables

The application requires the following environment variables to be set:

| Variable           | Description                         | Default         |
| ------------------ | ----------------------------------- | --------------- |
| DB_NAME            | PostgreSQL database name            | url_shortener   |
| DB_USER            | PostgreSQL username                 | postgres        |
| DB_PASSWORD        | PostgreSQL password                 | postgres        |
| DB_HOST            | PostgreSQL host                     | localhost       |
| DB_PORT            | PostgreSQL port                     | 5432            |
| JWT_SECRET         | Secret key for signing JWTs         | None            |
| JWT_ACCESS_EXPIRE  | Access token expiration in seconds  | 3600 (1 hour)   |
| JWT_REFRESH_EXPIRE | Refresh token expiration in seconds | 604800 (7 days) |

## Website Title Extraction

The Linkify service automatically extracts website titles when creating URLs, QR codes, and barcodes:

- When a user submits a URL, the system makes a request to the target website
- The HTML is parsed to extract the `<title>` tag content
- This title is stored in the database and returned in API responses
- If extraction fails (network issues, invalid URL, missing title), the title field will be null
- No additional input is required from users for this feature
