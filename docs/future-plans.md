# Linkify Future Plans & Features

---

## Future Feature Roadmap

This document records advanced features and technical solutions that are important but not yet implemented in the Linkify project. These features will be gradually developed according to actual needs and the project roadmap. Contributions and suggestions are welcome!

---

## Table of Contents

- [Password Reset & Management (Planned)](#password-reset--management-planned)
- [Other Planned Advanced Features](#other-planned-advanced-features)

---

## Password Reset & Management (Planned)

### Table: password_reset_tokens (planned)

| Column     | Type      | Constraints                                     | Description                                   |
| ---------- | --------- | ----------------------------------------------- | --------------------------------------------- |
| id         | SERIAL    | PRIMARY KEY                                     | Unique identifier for each reset token record |
| user_id    | INTEGER   | NOT NULL REFERENCES users(id) ON DELETE CASCADE | User requesting the reset                     |
| token      | TEXT      | NOT NULL UNIQUE                                 | Secure random token                           |
| expires_at | TIMESTAMP | NOT NULL                                        | Expiration timestamp for this token           |
| used       | BOOLEAN   | NOT NULL DEFAULT FALSE                          | Whether the token has been used               |
| created_at | TIMESTAMP | NOT NULL DEFAULT CURRENT_TIMESTAMP              | When the token record was created             |

**Indexes:**

- INDEX on `user_id`
- INDEX on `expires_at`

**SQL for creating the table:**

```sql
CREATE TABLE IF NOT EXISTS password_reset_tokens (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  token TEXT NOT NULL UNIQUE,
  expires_at TIMESTAMP NOT NULL,
  used BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_prt_user ON password_reset_tokens (user_id);
CREATE INDEX IF NOT EXISTS idx_prt_expires ON password_reset_tokens (expires_at);
```

**Relationship: User-to-PasswordResetTokens**

- One-to-many: A single user may request multiple password reset tokens, each generating a new record
- Lifecycle: Each token record tracks creation time, expiry, and usage status
- Deletion: When a user is deleted, all their related password reset tokens are also removed (ON DELETE CASCADE)

### Password Management Flows (Planned)

#### 1. Forgot Password (Not Logged In)

1. User submits email, system generates a secure `token` and writes it to the `password_reset_tokens` table
2. System sends a reset link with the token to the user's email
3. User clicks the link, frontend collects new password and submits, backend verifies token validity (not expired, not used)
4. Update user password and mark the token as used

#### 2. Change Password (Logged In)

1. User enters old and new password in the profile center
2. Backend verifies the old password and updates to the new password

---

## Planned Endpoints for Password Reset & Management

The following API endpoints are planned to support the password reset and management features described above:

- Request password reset (initiate reset via email)
- Confirm password reset (submit new password with token)
- Change password (for logged-in users)

Additional advanced features for the future:

- User multi-factor authentication (MFA/2FA)
- User security logs and abnormal login alerts
- User self-service account deletion and data export
- API rate limiting and security protection
- More comprehensive user profile fields and social features

---

> This document describes future plans. Actual implementation is subject to development progress. Discussion and PRs are welcome!

     - Users provide `current_password` and `new_password` via `/users/me/password`, then password is updated immediately without email verification

#### 1.1. Refresh Token

**Purpose:** Get a new access token using a refresh token.

**Endpoint:** `/auth/refresh`

**Method:** `POST`

**Request Body:**

```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response:** (200 OK)

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

---

#### 1.2. Request Password Reset

**Purpose:** Start a password-reset flow by sending a reset link to the user’s email.

**Endpoint:** `/auth/password-reset/request`

**Method:** `POST`

**Request Body:**

```json
{
  "email": "lydia@example.com",
  "username": "lydiagao"
}
```

**Response:** (200 OK)

```json
{
  "message": "Password reset email sent."
}
```

---

#### 1.3. Confirm Password Reset

**Purpose:** Complete password reset using the token sent by email.

**Endpoint:** `/auth/password-reset/confirm`

**Method:** `POST`

**Request Body:**

```json
{
  "token": "abcdef1234567890",
  "new_password": "NewP@ssw0rd!"
}
```

**Response:** (200 OK)

```json
{
  "message": "Password has been reset successfully."
}
```

---

#### 1.4. Change Password (Logged-in User)

**Purpose:** Allow a signed-in user to update their password.

**Endpoint:** `/users/me/password`

**Method:** `PATCH`

**Headers:**

- `Authorization: Bearer {access_token}`

**Request Body:**

```json
{
  "current_password": "OldP@ss1",
  "new_password": "NewP@ssw0rd!"
}
```

**Response:** (200 OK)

```json
{
  "message": "Password changed successfully."
}
```
