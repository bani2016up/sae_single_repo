# CORS Configuration

## Overview
The authentication service has CORS (Cross-Origin Resource Sharing) middleware configured to allow requests from the frontend application.

## Current Configuration

The following origins are allowed:
- `http://localhost:5173` - Vite development server (default)
- `http://localhost:3000` - Alternative frontend port

## Credentials
- **Allow Credentials**: `true` - Required for cookie-based authentication
- **Allow Methods**: GET, POST, PUT, DELETE, OPTIONS, PATCH
- **Allow Headers**: All headers (`*`)
- **Max Age**: 3600 seconds (1 hour)

## Adding New Origins

To add production or additional development origins:

1. Open `backend/auth/main.py`
2. Locate the CORS middleware configuration
3. Add your origin to the `allow_origins` list:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "https://your-production-domain.com",  # Add your production URL
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    max_age=3600,
)
```

## Environment-Based Configuration (Optional)

For production deployments, consider using environment variables:

```python
import os

allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    max_age=3600,
)
```

Then set the environment variable:
```bash
export ALLOWED_ORIGINS="http://localhost:5173,https://your-app.com"
```

## Testing CORS

Test the CORS configuration with curl:

```bash
curl -H "Origin: http://localhost:5173" \
  -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: Content-Type" \
  -X OPTIONS \
  http://localhost:8081/api/v1/auth/sessions
```

Expected response headers:
- `Access-Control-Allow-Origin: http://localhost:5173`
- `Access-Control-Allow-Credentials: true`
- `Access-Control-Allow-Methods: ...`

## Troubleshooting

If you still get CORS errors:

1. Verify the origin in your frontend matches exactly (including protocol and port)
2. Check that `withCredentials: true` is set in your Axios client
3. Restart the backend server after making changes
4. Clear browser cache if the error persists
