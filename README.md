# CareBridge

> AI-powered health companion for organizing health information, understanding medical documents, tracking health activity, and preparing for doctor visits.

CareBridge is a full-stack healthcare assistance platform designed to help users manage and understand their personal health information in one place.

It provides a simple interface for recording health concerns, uploading medical reports, maintaining a health profile, tracking health activity, and preparing for doctor consultations.

---

## 🚀 Features

### 🩺 AI Health Assistant
- Provides general health guidance.
- Helps users understand health-related information.
- Designed to assist even when the user has not uploaded medical documents.
- Presents information in a simple and understandable format.

### ❤️ Health Concerns
- Add and manage personal health concerns.
- Track active concerns.
- Store descriptions and relevant information.
- Automatically reflects concern activity on the Dashboard.

### 📄 Medical Reports
- Upload medical documents.
- Track uploaded medical reports.
- Connect medical-document activity with the health timeline.
- Support for AI-assisted medical document analysis.

### 👤 Health Profile
Users can maintain important health information including:

- Date of birth
- Blood group
- Allergies
- Medical conditions
- Current medications
- Emergency contact name
- Emergency contact phone

The Dashboard dynamically calculates profile completeness.

### 📈 Health Timeline
- Records important health-related activities.
- Tracks health concerns.
- Tracks medical document uploads.
- Tracks medical document analysis.
- Displays recent health activity.

### 🧑‍⚕️ Doctor Visit Preparation
Helps users organize information before a doctor visit, including symptoms and questions they may want to discuss.

### 📊 Dynamic Dashboard
The Dashboard dynamically retrieves data from the backend and displays:

- Active health concerns
- Uploaded medical reports
- Timeline events
- Recent health activity
- Health profile completeness

Dashboard data is loaded through authenticated API requests.

### 🔐 Authentication
- User registration and login
- JWT-based authentication
- Protected API endpoints
- Authenticated user-specific health data
- Access-token based API requests

### 🌙 Dark Mode
- Light and dark appearance support.
- Theme preference is persisted locally.

---

# 🏗️ Architecture

```text
                    ┌──────────────────────┐
                    │      CareBridge      │
                    │      Frontend        │
                    │ React + TypeScript   │
                    │       + Vite         │
                    └──────────┬───────────┘
                               │
                         REST API / JWT
                               │
                               ▼
                    ┌──────────────────────┐
                    │       FastAPI        │
                    │       Backend        │
                    └──────────┬───────────┘
                               │
                    ┌──────────┴───────────┐
                    │                      │
                    ▼                      ▼
             ┌──────────────┐      ┌──────────────┐
             │  PostgreSQL  │      │ AI Services  │
             │   Database   │      │ / Analysis   │
             └──────────────┘      └──────────────┘

🛠️ Technology Stack
Frontend
- React
- TypeScript
- Vite
- HTML5
- CSS3
- Local Storage
- REST API
Backend
- Python
- FastAPI
- Pydantic
- SQLAlchemy
- Alembic
- PostgreSQL
- JWT Authentication
- Password hashing with Argon2
AI / Document Processing
CareBridge is designed to integrate AI-powered services for:
- Medical document analysis
- Health information assistance
- Plain-language explanations
- Health-related guidance
Development Tools
- Git
- GitHub
- PowerShell
- VS Code
- Uvicorn
- npm

📁 Project Structure

carebridge/
│
├── frontend/
│   ├── src/
│   │   ├── App.tsx
│   │   ├── api.ts
│   │   └── ...
│   │
│   ├── package.json
│   ├── vite.config.ts
│   └── ...
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── models/
│   │   ├── routers/
│   │   ├── schemas/
│   │   ├── core/
│   │   └── ...
│   │
│   ├── alembic/
│   ├── alembic.ini
│   ├── requirements.txt
│   └── ...
│
├── .gitignore
└── README.md

⚙️ Prerequisites
Before running CareBridge locally, install:
- Python 3.14+
- Node.js
- npm
- PostgreSQL
- Git
Verify the installations:
python --version
node --version
npm --version
git --version

🔧 Backend Setup
Navigate to the backend directory:
cd backend

Create a virtual environment:
python -m venv venv

Activate it on Windows:
.\venv\Scripts\Activate.ps1

Install dependencies:
pip install -r requirements.txt

🔐 Environment Variables
Create a .env file in the backend directory.
Example:
APP_NAME=CareBridge
APP_VERSION=1.0.0

DATABASE_URL=postgresql://username:password@localhost:5432/carebridge

JWT_SECRET_KEY=your_secure_secret_key
JWT_ALGORITHM=HS256

🗄️ Database Setup
Run the Alembic migrations:
alembic upgrade head

To check the current migration:
alembic current

To create a new migration after changing database models:
alembic revision --autogenerate -m "description of change"

Then apply it:
alembic upgrade head

▶️ Start the Backend
From the backend directory:
uvicorn app.main:app --reload

The backend will normally be available at:
http://127.0.0.1:8000

🎨 Frontend Setup
Open another PowerShell terminal:
cd frontend

Install dependencies:
npm install

🌐 Frontend Environment Variables
Create:
frontend/.env

Example:
VITE_API_URL=http://127.0.0.1:8000/api

▶️ Start the Frontend
Run:
npm run dev

Vite will display the local development URL in the terminal.
Open that URL in your browser.
🔌 API Integration
The frontend communicates with the FastAPI backend through REST APIs.
The frontend API layer uses:
frontend/src/api.ts

The API client automatically attaches the JWT access token:
Authorization: Bearer <access_token>

Example API operations include:
/api/auth/...
/api/health-profile/
/api/health-concerns/
/api/medical-documents/
/api/health-timeline/

📊 Dashboard Data Flow
The Dashboard retrieves authenticated user data from multiple APIs.
                 User Login
                     │
                     ▼
                JWT Token
                     │
                     ▼
              CareBridge API
                     │
       ┌─────────────┼─────────────┐
       │             │             │
       ▼             ▼             ▼
 Health Concerns  Documents    Health Timeline
       │             │             │
       └─────────────┼─────────────┘
                     │
                     ▼
                Dashboard
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
     Concerns      Reports     Timeline
                     │
                     ▼
              Recent Activity

Dashboard API requests are executed in parallel to reduce unnecessary waiting between requests.
🔒 Security
CareBridge uses authenticated API endpoints to ensure that health information is associated with the authenticated user.
Security mechanisms include:
- JWT authentication
- Password hashing
- Protected API routes
- User-specific database queries
- Environment variables for secrets
- No secrets committed to source control
Never commit:
.env
JWT secrets
Database passwords
API keys
Access tokens
Private keys

🧪 Build the Frontend
Before deployment, test the production build:
cd frontend
npm run build

A successful build should produce:
dist/

You can also preview the production build locally:
npm run preview

🚀 Deployment
CareBridge can be deployed as separate frontend and backend services.
Frontend
The React/Vite frontend can be deployed to a static hosting platform.
Set:
VITE_API_URL=<production-backend-api-url>

Backend
Deploy the FastAPI application to a server capable of running Python applications.
Production server example:
uvicorn app.main:app --host 0.0.0.0 --port 8000

For production deployments, use HTTPS and configure the appropriate CORS policy.
🔄 Development Workflow
A typical development workflow:
1. Start PostgreSQL
        ↓
2. Start FastAPI backend
        ↓
3. Start React frontend
        ↓
4. Login to CareBridge
        ↓
5. Use health features
        ↓
6. Verify API/database changes
        ↓
7. Run frontend build
        ↓
8. Commit changes
        ↓
9. Push to GitHub
        ↓
10. Deploy

🧩 Main Modules
Module	Purpose
Authentication	Registration, login and JWT authentication
AI Health Assistant	General health assistance
Health Concerns	Record and track health concerns
Medical Reports	Upload and analyze medical documents
Health Profile	Maintain personal health information
Health Timeline	Track health-related events
Doctor Visit Prep	Organize information for doctor consultations
Dashboard	Provide a dynamic overview of health activity
Settings	Manage application preferences


🎯 Project Goals
CareBridge aims to make personal health information easier to:
- Understand
- Organize
- Track
- Access
- Prepare for medical consultations
The platform focuses on presenting health information in a user-friendly way while keeping the user's information associated with their authenticated account.
⚠️ Medical Disclaimer
CareBridge is intended as a health information and assistance tool.
It is not a replacement for a qualified healthcare professional, medical diagnosis, emergency services, or professional medical treatment.
Users should consult an appropriate healthcare professional for medical decisions.
In an emergency, contact local emergency services immediately.
🧑‍💻 Development
CareBridge is developed as a full-stack application using modern web technologies and a modular backend architecture.
For development:
git clone <repository-url>
cd carebridge

Then follow the backend and frontend setup instructions above.
📜 License
This project is currently intended for educational, development, and hackathon purposes.
Add your preferred open-source license here if you plan to distribute the project publicly.
👥 Contributors
CareBridge is developed as a collaborative project.
Contributors can submit improvements through GitHub pull requests.
⭐ CareBridge
Connect your health information. Understand it. Prepare better.

### Recommended repository layout

For GitHub, keep the README at:

```text
carebridge/
├── README.md
├── frontend/
├── backend/
└── .gitignore
