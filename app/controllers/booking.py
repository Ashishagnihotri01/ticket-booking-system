import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import ShowSeat, SeatStatus, Booking, Waitlist, User
from app.middleware.auth_handler import AuthHandler
from app.services.redis_service import RedisService
from app.services.qr_service import QRService
from app.services.email_service import EmailService
from app.config import settings

router = APIRouter(prefix="/bookings", tags=["Bookings"])

@router.post("/hold/{seat_id}")
def hold_seat(seat_id: int, db: Session = Depends(get_db), current_user: dict = Depends(AuthHandler.get_current_user)):
    """Secures structural reservation placement rules by implementing unique Redis-backed mutual exclusion checks."""
    lock_name = f"seat_{seat_id}"
    
    # 1. Acquire Distributed Mutex Concurrency Lock
    #if not RedisService.acquire_lock(lock_name):
     #   raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Seat is currently being processed by another user.")
    
    try:
        # 2. Fetch inside transactional workspace
        seat = db.query(ShowSeat).filter(ShowSeat.id == seat_id).first()
        if not seat:
            raise HTTPException(status_code=404, detail="Seat parameters not found.")
            
        if seat.status != SeatStatus.AVAILABLE:
            raise HTTPException(status_code=400, detail="Seat status is unavailable for registration hold.")
        
        # 3. Establish Temporary Volatile Caching and Permanent Structural Updates
        seat.status = SeatStatus.HELD
        db.commit()
        
        RedisService.set_seat_hold(seat.show_id, seat.id, current_user["user_id"], settings.SEAT_HOLD_TTL_SECONDS)
        return {"message": "Seat successfully held.", "expires_in_seconds": settings.SEAT_HOLD_TTL_SECONDS}
        
    finally:
        RedisService.release_lock(lock_name)

@router.post("/confirm/{seat_id}")
def confirm_booking(seat_id: int, db: Session = Depends(get_db), current_user: dict = Depends(AuthHandler.get_current_user)):
    """Validates state context and transitions transient locks to a definitive structural database record."""
    seat = db.query(ShowSeat).filter(ShowSeat.id == seat_id).first()
    if not seat or seat.status != SeatStatus.HELD:
        raise HTTPException(status_code=400, detail="No active hold found for this seat layout position.")
    
    # Generate System Reference Identifiers
    booking_ref = f"TKT-{uuid.uuid4().hex[:8].upper()}"
    
    new_booking = Booking(
        booking_reference=booking_ref,
        user_id=current_user["user_id"],
        show_id=seat.show_id,
        seat_id=seat.id
    )
    
    seat.status = SeatStatus.BOOKED
    db.add(new_booking)
    db.commit()
    
    # Remove Expire Task Lifecycle Keys
    RedisService.remove_seat_hold(seat.show_id, seat.id)
    
    # Asynchronously construct verification imagery and dispatch structural updates
    user = db.query(User).filter(User.id == current_user["user_id"]).first()
    qr_img = QRService.generate_booking_qr(booking_ref)
    EmailService.send_booking_confirmation(user.email, booking_ref, qr_img)
    
    return {"message": "Booking confirmed.", "booking_reference": booking_ref}