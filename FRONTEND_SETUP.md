# Frontend Setup and Usage Guide

## Overview

This repository now includes a modern React + TypeScript frontend application that provides a complete user interface for the document analysis system.

## Architecture

```
┌─────────────┐          ┌──────────────┐          ┌──────────────┐
│   Frontend  │ ──HTTP──>│   Backend    │ ──DB──>  │  Supabase    │
│   (React)   │ <─JSON── │   (FastAPI)  │ <─AUTH─  │  PostgreSQL  │
└─────────────┘          └──────────────┘          └──────────────┘
```

## Quick Start

### Prerequisites

1. **Node.js 18+** and npm
2. **Backend services running** (see backend READMEs)
3. **Environment variables configured**

### Installation

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Configure environment:
```bash
cp .env.example .env
```

4. Update `.env` with your backend URL (default: `http://localhost:8000`):
```env
VITE_API_URL=http://localhost:8000
```

### Development

Start the development server:
```bash
npm run dev
```

The application will be available at: **http://localhost:5173**

### Production Build

Build for production:
```bash
npm run build
```

Preview production build:
```bash
npm run preview
```

## Features

### ✅ Implemented

1. **Authentication**
   - User registration with password strength indicator
   - Login/logout functionality
   - Session management via HTTP-only cookies
   - Protected routes for authenticated content

2. **Document Management**
   - Create documents manually or from file upload
   - View all user documents in a table
   - Edit document title and content
   - Delete documents
   - File upload support (.txt, .rtf)

3. **Document Analysis**
   - Start AI-powered validation on documents
   - View validation results with detailed errors
   - Real-time status updates during analysis
   - Error highlighting with suggestions and explanations

4. **User Interface**
   - Modern, clean design with Tailwind CSS
   - Dark/Light mode toggle
   - Responsive layout (mobile, tablet, desktop)
   - Loading states and error handling
   - Toast notifications for user feedback
   - Accessible components (WCAG 2.1 AA)

5. **Dashboard**
   - Statistics overview
   - Recent documents list
   - Quick actions

## Tech Stack

- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **React Router** - Client-side routing
- **TanStack Query** - Server state management
- **Tailwind CSS** - Styling
- **Axios** - HTTP client
- **Sonner** - Toast notifications
- **Lucide React** - Icons

## Project Structure

```
frontend/
├── src/
│   ├── api/              # API client and endpoints
│   │   ├── client.ts     # Axios configuration
│   │   ├── auth.ts       # Auth endpoints
│   │   ├── documents.ts  # Document CRUD
│   │   └── validation.ts # Validation endpoints
│   ├── components/
│   │   ├── ui/          # Reusable UI components
│   │   └── common/      # App-specific components
│   ├── context/         # React Context providers
│   │   ├── AuthContext.tsx
│   │   └── ThemeContext.tsx
│   ├── pages/           # Page components
│   ├── types/           # TypeScript definitions
│   ├── utils/           # Utility functions
│   ├── lib/             # Third-party configs
│   └── styles/          # Global styles
├── public/
├── index.html
├── package.json
└── vite.config.ts
```

## API Integration

The frontend communicates with the backend API at the following endpoints:

### Authentication (`/api/v1/auth/`)
- `POST /users` - Register
- `POST /sessions` - Login
- `DELETE /sessions/` - Logout
- `GET /users/me` - Get current user

### Documents (`/api/v1/documents/`)
- `GET /` - List all documents
- `GET /{id}` - Get document details
- `POST /` - Create document
- `POST /from-file` - Upload document
- `PUT /{id}` - Update document
- `DELETE /{id}` - Delete document

### Validation (`/api/v1/validation/`)
- `POST /` - Create validation
- `POST /{id}/start` - Start validation
- `GET /{id}` - Get validation status
- `GET /{id}/errors` - Get validation errors

## Usage Guide

### 1. Registration and Login

1. Navigate to http://localhost:5173
2. Click "Get Started" or "Sign Up"
3. Enter email and password
4. After registration, log in with credentials

### 2. Creating Documents

**Manual Entry:**
1. Go to Dashboard or Documents page
2. Click "New Document"
3. Enter title and content
4. Click "Create Document"

**File Upload:**
1. Click "New Document"
2. Select "Upload File" tab
3. Choose a .txt or .rtf file
4. Click "Upload Document"

### 3. Managing Documents

- **View:** Click on any document in the list
- **Edit:** Open document detail page, click "Edit"
- **Delete:** Click trash icon in list or detail page
- **Search:** Use the search bar in the documents list

### 4. Running Analysis

1. Open a document detail page
2. Click "Start Analysis"
3. View real-time progress
4. See results with highlighted errors
5. Click on errors to see suggestions

### 5. Theme Toggle

Click the sun/moon icon in the top navigation to switch between light and dark modes.

## Configuration

### Environment Variables

- `VITE_API_URL` - Backend API base URL (default: `http://localhost:8000`)

### Customization

#### Theme Colors

Edit `src/styles/globals.css` to customize colors:
- Light mode: `:root` section
- Dark mode: `.dark` section

#### API Client

Edit `src/api/client.ts` to customize:
- Base URL
- Request/response interceptors
- Error handling

## Troubleshooting

### Build Errors

If you encounter build errors:
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Clear Vite cache
rm -rf node_modules/.vite
```

### API Connection Issues

1. Ensure backend is running on the configured port
2. Check CORS settings in backend
3. Verify `VITE_API_URL` in `.env`
4. Check browser console for errors

### Authentication Not Working

1. Ensure cookies are enabled in browser
2. Check backend session configuration
3. Verify Supabase credentials

## Development Tips

### Hot Module Replacement (HMR)

Vite provides instant feedback during development. Changes to React components will update without full page reload.

### TypeScript

The project uses strict TypeScript. All API responses are typed in `src/types/api.ts`.

### State Management

- **Server State:** TanStack Query (React Query)
- **Auth State:** React Context
- **Theme State:** React Context + localStorage

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Performance

The production build is optimized with:
- Code splitting
- Tree shaking
- Minification
- Gzip compression

Expected bundle size: ~400 KB (gzipped: ~125 KB)

## License

See LICENSE file in repository root
