# Frontend - React + TypeScript Application

A modern, responsive frontend application built with React, TypeScript, and Tailwind CSS for document management and AI-powered text analysis.

## Tech Stack

- **React 18** with TypeScript
- **Vite** - Fast build tool and dev server
- **React Router** - Client-side routing
- **TanStack Query (React Query)** - Server state management
- **Tailwind CSS** - Utility-first styling
- **shadcn/ui** - Accessible UI components
- **Axios** - HTTP client
- **Sonner** - Toast notifications
- **Lucide React** - Icon library

## Features

- 🔐 **Authentication** - Login and registration with session management
- 📄 **Document Management** - Create, view, edit, and delete documents
- 📤 **File Upload** - Support for .txt and .rtf files
- 🤖 **AI Analysis** - Text validation with error highlighting
- 🎨 **Dark/Light Mode** - Theme toggle with system preference detection
- 📱 **Responsive Design** - Mobile-first approach
- ♿ **Accessible** - WCAG 2.1 AA compliant components

## Getting Started

### Prerequisites

- Node.js 18+ and npm
- Backend API running (see backend documentation)

### Installation

1. Install dependencies:
```bash
npm install
```

2. Create environment file:
```bash
cp .env.example .env
```

3. Update `.env` with your API URL:
```
VITE_API_URL=http://localhost:8000
```

### Development

Start the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:5173`

### Build

Build for production:
```bash
npm run build
```

Preview production build:
```bash
npm run preview
```

### Linting

```bash
npm run lint
```

## API Integration

The frontend integrates with the following backend endpoints:

### Authentication (`/api/v1/auth/`)
- `POST /users` - Register new user
- `POST /sessions` - Login
- `DELETE /sessions/` - Logout
- `GET /users/me` - Get current user

### Documents (`/api/v1/documents/`)
- `GET /` - Get all documents
- `GET /{id}` - Get document by ID
- `POST /` - Create document
- `POST /from-file` - Upload document file
- `PUT /{id}` - Update document
- `DELETE /{id}` - Delete document

### Validation (`/api/v1/validation/`)
- `POST /` - Create validation
- `POST /{id}/start` - Start validation process
- `GET /{id}` - Get validation status
- `GET /{id}/errors` - Get validation errors
- `PUT /{id}/reset` - Reset validation

## License

See LICENSE file in repository root
