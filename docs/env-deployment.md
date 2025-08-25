## Environment Variables

Linkify relies on several environment variables for configuration. Create a `.env` file in the root of the project and add the following variables:

```env
DATABASE_URL=postgresql://user:password@localhost/dbname
SECRET_KEY=your_secret_key
BASE_URL=http://localhost:8000
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
```

## Run the Application
To run the application, use the following command:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
