# Linkify API Documentation

---

## Table of Contents

- [Linkify API Documentation](#linkify-api-documentation)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [API Endpoints](#api-endpoints)
    - [1. User Management Endpoints](#1-user-management-endpoints)
      [1.1. Register User (Username/Password)](#11-register-user-usernamepassword)
      [1.2. Login (OAuth2 Password Flow)](#12-login-oauth2-password-flow)
      [1.3. Logout (Client-side)](#13-logout-client-side)
      [1.4. Get Current User](#14-get-current-user)
    - [2. Short URL Endpoints](#2-short-url-endpoints)
      - [2.1. Create Short URL](#21-create-short-url)
      - [2.2. List My Short URLs](#22-list-my-short-urls)
      - [2.3. Redirect from Short URL](#23-redirect-from-short-url)
      - [2.4. Check Alias Availability](#24-check-alias-availability)
      - [2.5. Set or Update Alias](#25-set-or-update-alias)
      - [2.6. Get Alias](#26-get-alias)
      - [2.7. Remove Alias](#27-remove-alias)
    - [3. QR Code Endpoints](#3-qr-code-endpoints)
      - [3.1. Generate QR Code (Sync)](#31-generate-qr-code-sync)
      - [3.1.b. Generate QR Code (Async, Celery)](#31b-generate-qr-code-async-celery)
      - [3.2. Get QR Code Image (Redis Cache)](#32-get-qr-code-image-redis-cache)
      - [3.3. Redirect from QR Code](#33-redirect-from-qr-code)
      - [3.4. Get QR Code Task Status (Celery)](#34-get-qr-code-task-status-celery)
    - [4. Barcode Endpoints](#4-barcode-endpoints)
      - [4.1. Generate Barcode (Sync)](#41-generate-barcode-sync)
      - [4.1.b. Generate Barcode (Async, Celery)](#41b-generate-barcode-async-celery)
      - [4.2. Get Barcode Image (Redis Cache)](#42-get-barcode-image-redis-cache)
      - [4.3. Redirect from Barcode](#43-redirect-from-barcode)
      - [4.4. Get Barcode Task Status (Celery)](#44-get-barcode-task-status-celery)
    - [5. Analytics Endpoints](#5-analytics-endpoints)
      - [5.1. Get Short URL Analytics](#51-get-short-url-analytics)
      - [5.2. Get QR Code Analytics](#52-get-qr-code-analytics)
      - [5.3. Get Barcode Analytics](#53-get-barcode-analytics)
      - [5.4. Get Aggregated Analytics](#54-get-aggregated-analytics)
  - [Environment Variables](#environment-variables)
  - [Website Title Extraction](#website-title-extraction)

---

## Overview

This document outlines the API endpoints for the Linkify service. Linkify allows users to:

1. **User Management**
   - Create user accounts (username/password or Google)
   - Manage user profile information
2. **Short URLs**
   - Create short URLs from long ones with automatic title extraction
   - Redirect from short URLs to their original destinations
3. **QR Codes**
   - Generate QR codes from URLs (sync or async via Celery)
   - Get QR code images (cached in Redis)
   - Redirect from QR codes to their original destinations
4. **Barcodes**
   - Generate barcodes from URLs (sync or async via Celery)
   - Get barcode images (cached in Redis)
   - Redirect from barcodes to their original destinations
5. **Analytics**
   - View detailed statistics about individual resources
   - Access aggregated analytics data for visualization

---

## API Endpoints

### 1. User Management Endpoints

      **Endpoint:** `/qrcodes/`
      **Headers:**

      - Authorization: Bearer {access_token}

**Endpoint:** `/auth/`

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

      **Endpoint:** `/qrcodes/async`

---

#### 1.2. Login (OAuth2 Password Flow)

**Purpose:** Authenticate user and get JWT access token.

**Endpoint:** `/auth/token`

**Method:** `POST`

**Request:** `application/x-www-form-urlencoded`

Fields:
"status": "SUCCESS",
"result": {

**Response:** (200 OK)

```json
{
  "access_token": "<jwt>",
  "token_type": "bearer"
}
```

---

**Purpose:** Client removes tokens from storage. No server-side action required with pure JWT.

**Note:** In a pure JWT implementation, logout is handled client-side by removing the tokens from storage. The frontend application should delete both the access token and refresh token from localStorage or cookies when the user logs out, and then redirect to the login page.

---

#### 1.4. Get Current User

**Purpose:** Retrieve current user profile information.

**Endpoint:** `/users/`

**Method:** `GET`

**Headers:**

- Authorization: Bearer {access_token}

**Response:** (200 OK)

```json
      **Endpoint:** `/barcodes/`
      **Headers:**

      - Authorization: Bearer {access_token}
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

> Note: Update profile endpoint is not implemented in the current code.

---

### 2. Short URL Endpoints

#### 2.1. Create Short URL

      **Endpoint:** `/barcodes/async`

**Purpose:** Convert a long URL into a short URL with a randomly generated code. Automatically extracts website title.

**Endpoint:** `/shorturls/`

**Method:** `POST`

**Headers:**

- Authorization: Bearer {access_token}

**Request Body:**

```json
        "status": "SUCCESS",
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

#### 2.2. List My Short URLs

**Purpose:** List all short URLs for the current user.

**Endpoint:** `/shorturls/`

**Method:** `GET`

**Response:** (200 OK) Array of user's short URLs.

---

#### 2.3. Redirect from Short URL

**Purpose:** Redirect visitors to the original URL when they use a short link.

**Endpoint:** `/shorturls/{short_code}`

**Method:** `GET`

**Example:**

- When someone visits `http://localhost:8000/abc123`
- They are redirected to the original URL
- The click counter is incremented

**Response:**

- 307 Temporary Redirect to the original URL
- 404 Not Found if the short code doesn't exist

---

#### 2.4. Check Alias Availability

**Endpoint:** `/shorturls/aliases/check`

**Method:** `POST`

**Request Body:**

```json
{ "alias": "your-custom-alias" }
```

**Response:**

```json
{ "available": true }
```

---

#### 2.5. Set or Update Alias

**Purpose:** Assign or change a custom alias for a short code. Aliases can be set either at creation time (see Create Short URL) or updated later using this endpoint.

**Endpoint:** `/shorturls/{short_code}/alias`

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

#### 2.6. Get Alias

**Purpose:** Retrieve the custom alias for a given short code, if one exists.

**Endpoint:** `/shorturls/{short_code}/alias`

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

#### 2.7. Remove Alias

**Purpose:** Delete the custom alias and revert to the default randomly generated code.

**Endpoint:** `/shorturls/{short_code}/alias`

**Method:** `DELETE`

**Headers:**

- `Authorization: Bearer {access_token}`

**Response:** (204 No Content)

---

#### 2.8. Batch Create Short URLs (Async)

**Purpose:** Submit multiple URLs in one request. Each short link is generated asynchronously via Celery workers, and the completion result is pushed over the websocket channel.

**Endpoint:** `/shorturls/batch`

**Method:** `POST`

**Headers:**

- Authorization: Bearer {access_token}

**Request Body:**

```json
{
  "items": [
    { "original_url": "https://example.com/one" },
    { "original_url": "https://example.com/two", "alias": "two" }
  ]
}
```

`items` accepts 1–50 `ShortenRequest` payloads.

**Response:** (202 Accepted)

```json
{
  "success": true,
  "batch_id": "6f90b8f0-db49-42c0-8c89-32c8f4b3dc31",
  "task_id": "c6fd9932-4972-4b0c-b468-4d7b782f1653",
  "status": "pending",
  "websocket_channel": "ws:user:42"
}
```

- `batch_id` lets the UI correlate websocket payloads with a submission.
- `websocket_channel` is the Redis pub/sub channel listened to by `/ws/batch`.

**Completion Flow:** When every Celery task in the batch finishes, the backend publishes a websocket event:

```json
{
  "type": "batch_completed",
  "entity": "shorturl",
  "batch_id": "6f90b8f0-db49-42c0-8c89-32c8f4b3dc31",
  "count": 2,
  "items": [ {"short_code": "abc123", ...}, {"short_code": "def456", ...} ]
}
```

### 3. QR Code Endpoints

#### 3.1. Generate QR Code (Sync)

**Purpose:** Create a QR code from a URL. Automatically extracts website title.

**Endpoint:** `/qrcodes/`

**Method:** `POST`

**Headers:**

- Authorization: Bearer {access_token}

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

#### 3.1.b. Generate QR Code (Async, Celery)

**Purpose:** Create a QR code from a URL asynchronously using Celery.

**Endpoint:** `/qrcodes/async`

**Method:** `POST`

**Request Body:**

#### 3.1.c. Batch Generate QR Codes (Async)

**Purpose:** Kick off multiple QR code jobs at once. Each job runs inside RabbitMQ/Celery workers and the aggregate result is delivered through the websocket channel.

**Endpoint:** `/qrcodes/batch`

**Method:** `POST`

**Headers:**

- Authorization: Bearer {access_token}

**Request Body:**

```json
{
  "items": [
    { "original_url": "https://example.com/alpha" },
    { "original_url": "https://example.com/beta", "title": "Beta" }
  ]
}
```

**Response:** (202 Accepted)

```json
{
  "success": true,
  "batch_id": "05cb6c98-4a80-459f-9791-9c0d3a1bc13f",
  "task_id": "2f6c5bcd-9fc8-4d37-8e53-2b8962839f1a",
  "status": "pending",
  "websocket_channel": "ws:user:42"
}
```

The websocket payload mirrors the short URL batch example but `"entity": "qrcode"` and each entry contains the QR code metadata plus `image_url`.

```json
{
  "original_url": "https://example.com/your/long/url"
}
```

**Response:** (202 Accepted)

```json
{
  "task_id": "abc123task",
  "status": "pending"
}
```

---

#### 3.2. Get QR Code Image (Redis Cache)

**Purpose:** Retrieve the generated QR code image.

**Endpoint:** `/qrcodes/{qr_code_id}/image`

**Method:** `GET`

**Response:**

- QR code image (PNG format)
- 404 Not Found if the QR code ID doesn't exist

---

#### 3.3. Redirect from QR Code

**Purpose:** Redirect visitors to the original URL when they scan a QR code.

**Endpoint:** `/qrcodes/{qr_code_id}`

**Method:** `GET`

**Example:**

- When someone scans a QR code that leads to `http://localhost:8000/qrcode/qr123`
- The scan counter is incremented
- They are redirected to the original URL

**Response:**

- 307 Temporary Redirect to the original URL
- 404 Not Found if the QR code ID doesn't exist

---

#### 3.4. Get QR Code Task Status (Celery)

**Purpose:** Get the status and result of an asynchronous QR code creation task.

**Endpoint:** `/qrcodes/task/{task_id}`

**Method:** `GET`

**Response:**

```json
{
  "task_id": "abc123task",
  "status": "success",
  "result": {
    "original_url": "https://example.com/your/long/url",
    "qr_code_id": "qr123",
    "qr_code_url": "http://localhost:8000/qrcode/qr123",
    "title": "Example Website Homepage",
    "scans": 0,
    "user_id": 42,
    "created_at": "2025-05-15T14:30:00Z"
  }
}
```

---

### 4. Barcode Endpoints

#### 4.1. Generate Barcode (Sync)

**Purpose:** Create a barcode from a URL. Automatically extracts website title.

**Endpoint:** `/barcodes/`

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

#### 4.1.b. Generate Barcode (Async, Celery)

**Purpose:** Create a barcode from a URL asynchronously using Celery.

**Endpoint:** `/barcodes/async`

**Method:** `POST`

**Request Body:**

```json
{
  "original_url": "https://example.com/your/long/url"
}
```

**Response:** (202 Accepted)

```json
{
  "task_id": "def456task",
  "status": "pending"
}
```

---

#### 4.2. Get Barcode Image (Redis Cache)

**Purpose:** Retrieve the generated barcode image.

**Endpoint:** `/barcodes/{barcode_id}/image`

**Method:** `GET`

**Response:**

- Barcode image (PNG format)
- 404 Not Found if the barcode ID doesn't exist

---

#### 4.3. Redirect from Barcode

**Purpose:** Redirect visitors to the original URL when they scan a barcode.

**Endpoint:** `/barcodes/{barcode_id}`

**Method:** `GET`

**Example:**

- When someone scans a barcode that leads to `http://localhost:8000/barcode/bar123`
- The scan counter is incremented
- They are redirected to the original URL

**Response:**

- 307 Temporary Redirect to the original URL
- 404 Not Found if the barcode ID doesn't exist

---

#### 4.4. Get Barcode Task Status (Celery)

**Purpose:** Get the status and result of an asynchronous barcode creation task.

**Endpoint:** `/barcodes/task/{task_id}`

**Method:** `GET`

**Response:**

```json
{
  "task_id": "def456task",
  "status": "success",
  "result": {
    "original_url": "https://example.com/your/long/url",
    "barcode_id": "bar123",
    "barcode_url": "http://localhost:8000/barcode/bar123",
    "title": "Example Website Homepage",
    "scans": 0,
    "user_id": 42,
    "created_at": "2025-05-15T14:30:00Z"
  }
}
```

---

### 5. Analytics Endpoints

#### 5.1. Get Short URL Analytics

**Purpose:** Retrieve detailed analytics about a short URL.

**Endpoint:** `/analytics/shorturl`

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

#### 5.2. Get QR Code Analytics

**Purpose:** Retrieve detailed analytics about a QR code.

**Endpoint:** `/analytics/qrcode`

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

#### 5.3. Get Barcode Analytics

**Purpose:** Retrieve detailed analytics about a barcode.

**Endpoint:** `/analytics/barcode`

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

#### 5.4. Get Aggregated Analytics

**Purpose:** Retrieve aggregated analytics across all URLs, QR codes, and barcodes.

**Endpoint:** `/analytics/aggregate`

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

| Variable              | Description                         | Default                             |
| --------------------- | ----------------------------------- | ----------------------------------- |
| DB_NAME               | PostgreSQL database name            | url_shortener                       |
| DB_USER               | PostgreSQL username                 | postgres                            |
| DB_PASSWORD           | PostgreSQL password                 | postgres                            |
| DB_HOST               | PostgreSQL host                     | localhost                           |
| DB_PORT               | PostgreSQL port                     | 5432                                |
| JWT_SECRET            | Secret key for signing JWTs         | None                                |
| JWT_ACCESS_EXPIRE     | Access token expiration in seconds  | 3600 (1 hour)                       |
| JWT_REFRESH_EXPIRE    | Refresh token expiration in seconds | 604800 (7 days)                     |
| CELERY_BROKER_URL     | RabbitMQ broker URL                 | amqp://guest:guest@localhost:5672// |
| CELERY_RESULT_BACKEND | Redis result backend URL            | redis://localhost:6379/0            |
| REDIS_URL             | Redis cache URL                     | redis://localhost:6379/1            |

## Website Title Extraction

The Linkify service automatically extracts website titles when creating URLs, QR codes, and barcodes:

- When a user submits a URL, the system makes a request to the target website
- The HTML is parsed to extract the `<title>` tag content
- This title is stored in the database and returned in API responses
- If extraction fails (network issues, invalid URL, missing title), the title field will be null
- No additional input is required from users for this feature

## Realtime Batch Notifications

- **Endpoint:** `ws://{host}/ws/batch?token=<jwt>`
- **Auth:** Supply the same Bearer token used for REST calls via the `token` query parameter.
- **Channel:** Each user receives messages on `ws:user:{user_id}`; the server relays Redis pub/sub events to the websocket.

### Connection Lifecycle

1. Open a websocket and pass the JWT in the query string.
2. The backend validates the token and responds with `{ "type": "ws_ready", "channel": "ws:user:42" }`.
3. Keep the socket open to receive batch updates, e.g.:

```json
{
  "type": "batch_completed",
  "entity": "shorturl",
  "batch_id": "6f90b8f0-db49-42c0-8c89-32c8f4b3dc31",
  "count": 2,
  "items": [ ... ]
}
```

### Frontend Tips

- Use `batch_id` to correlate websocket messages with submitted forms.
- Reconnect on failure and re-fetch any in-progress batches via REST in case updates were missed.
- Multiple browser tabs for the same user can subscribe simultaneously; each socket will receive the same events.
