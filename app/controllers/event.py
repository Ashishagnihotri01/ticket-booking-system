from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Show, ShowSeat

router = APIRouter(prefix="/events", tags=["Events"])

@router.get("/")
def list_shows(db: Session = Depends(get_db)):
    shows = db.query(Show).all()
    return {"shows": [{"id": s.id, "title": s.title, "date_time": s.date_time} for s in shows]}

@router.get("/{show_id}/seats")
def get_seats(show_id: int, db: Session = Depends(get_db)):
    seats = db.query(ShowSeat).filter(ShowSeat.show_id == show_id).all()
    return {
        "seats": [
            {"id": seat.id, "row": seat.row_label, "number": seat.seat_number, "status": seat.status, "price": str(seat.price)}
            for seat in seats
        ]
    }