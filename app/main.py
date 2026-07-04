from fastapi import FastAPI
from app.config import settings
from app.controllers import auth, event, booking
from app.database import Base, engine

# Initialize Schema Layout Framework Mapping
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Ticket Booking Management Core API System Engine",
    version="1.0.0"
)

# Route Wiring Declarations
app.include_router(auth.router)
app.include_router(event.router)
app.include_router(booking.router)

@app.get("/")
def health_check():
    return {"status": "operational", "system": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=True)