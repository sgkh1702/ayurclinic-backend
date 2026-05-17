from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://ayurclinicnew.netlify.app",
]

app = FastAPI(title="Ayurclinic API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      # use the list defined above
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.core.database import Base, engine
from app.models.patient import Patient
from app.models.visit import Visit
from app.models.attachment import Attachment

from app.api.v1.endpoints.patients import router as patients_router
from app.api.v1.endpoints.visits import router as visits_router
from app.api.v1.endpoints.attachments import router as attachments_router



Base.metadata.create_all(bind=engine)



app.include_router(patients_router)
app.include_router(visits_router)
app.include_router(attachments_router)


@app.get("/")
def root():
    return {"message": "Ayurclinic API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}