import enum
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, Numeric, UniqueConstraint, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    ORGANISER = "organiser"
    CUSTOMER = "customer"

class SeatStatus(str, enum.Enum):
    AVAILABLE = "available"
    HELD = "held"
    BOOKED = "booked"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.CUSTOMER, nullable=False)

class Venue(Base):
    __tablename__ = "venues"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    shows = relationship("Show", back_populates="venue")

class Show(Base):
    __tablename__ = "shows"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    date_time = Column(DateTime, nullable=False)
    venue_id = Column(Integer, ForeignKey("venues.id"), nullable=False)
    organiser_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    venue = relationship("Venue", back_populates="shows")
    seats = relationship("ShowSeat", back_populates="show")

class ShowSeat(Base):
    __tablename__ = "show_seats"
    id = Column(Integer, primary_key=True, index=True)
    show_id = Column(Integer, ForeignKey("shows.id"), nullable=False)
    row_label = Column(String, nullable=False)
    seat_number = Column(Integer, nullable=False)
    category = Column(String, nullable=False)  # Premium, Standard
    price = Column(Numeric(10, 2), nullable=False)
    status = Column(Enum(SeatStatus), default=SeatStatus.AVAILABLE, nullable=False)
    
    show = relationship("Show", back_populates="seats")
    bookings = relationship("Booking", back_populates="seat")
    __table_args__ = (UniqueConstraint('show_id', 'row_label', 'seat_number', name='_show_seat_uc'),)

class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True)
    booking_reference = Column(String, unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    show_id = Column(Integer, ForeignKey("shows.id"), nullable=False)
    seat_id = Column(Integer, ForeignKey("show_seats.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_cancelled = Column(Boolean, default=False)

    seat = relationship("ShowSeat", back_populates="bookings")

class Waitlist(Base):
    __tablename__ = "waitlists"
    id = Column(Integer, primary_key=True, index=True)
    show_id = Column(Integer, ForeignKey("shows.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="waiting")  # waiting, offered, completed, expired