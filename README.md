# Linkify

Linkify is a simple and powerful URL shortening service with support for custom aliases, QR/barcode generation, and click analytics.

## Technology Stack

- **Backend:** Python, FastAPI, PostgreSQL, SQLAlchemy, JWT authentication
- **Frontend:** Next.js (React), Context API/Redux Toolkit,
- **UI:** Tailwind CSS, Shadcn UI
- **Infrastructure:** Docker, GitHub Actions, Render, AWS

## Documentation

- **Database Schema:** [docs/database-schema.md](docs/database-schema.md)
- **API Reference:** [docs/api.md](docs/api.md)
- **Environment & Deployment:** coming soon in [docs/env-deployment.md](docs/env-deployment.md)

## Project Structure

```
LinkifyServices/
├── .env                # Environment variables
├── alembic/            # Database migrations
├── app/                # Main application
│   ├── api/            # API routes (auth, users, qrcode, etc.)
│   ├── core/           # Core modules (config, security, dependencies)
│   ├── db/             # Database initialization and session management
│   ├── models/         # ORM models
│   ├── schemas/        # Pydantic schemas for data validation
│   ├── services/       # Business logic layer
│   ├── utils/          # Utility functions
│   └── main.py         # FastAPI application entry point
├── docs/               # Project documentation
├── local_test/         # Local test scripts
├── requirements.txt    # Python dependencies
├── README.md           # Project description
```

---

Developers can clone and explore each repository for detailed code and docs:

- **Backend Repo:** `lydia-gao/LinkifyServices`
- **Frontend Repo:** `lydia-gao/Linkify-UI`
