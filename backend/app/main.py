from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routes import health, auth, health_profile, health_concern, medical_document, medical_analysis, health_guidance, health_timeline, doctor_visit

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8443",
        "http://127.0.0.1:8443",
        "https://care-bridge-red.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    health.router,
    prefix="/api/health",
    tags=["Health"]
)

app.include_router(
    auth.router,
    prefix="/api/auth",
    tags=["Authentication"]
)

# Add Health Profile router here
app.include_router(
    health_profile.router,
    prefix="/api/health-profile",
    tags=["Health Profile"]
)
app.include_router(
    health_concern.router,
    prefix="/api/health-concerns",
    tags=["Health Concerns"]
)
app.include_router(
    medical_document.router,
    prefix="/api/medical-documents",
    tags=["Medical Documents"]
)
app.include_router(
    medical_analysis.router,
    prefix="/api/medical-analysis",
    tags=["Medical Analysis"]
)
app.include_router(
    health_guidance.router,
    prefix="/api/health-guidance",
    tags=["Health Guidance"]
)
app.include_router(
    health_timeline.router,
    prefix="/api/health-timeline",
    tags=["Health Timeline"]
)
app.include_router(
    doctor_visit.router,
    prefix="/api/doctor-visits",
    tags=["Doctor Visits"]
)


@app.get("/")
def root():
    return {
        "message": "CareBridge API is running",
        "version": settings.APP_VERSION
    }