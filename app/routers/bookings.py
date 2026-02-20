from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from .. import models, schemas
from ..dependencies import get_db
from ..auth import get_current_user

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.post("/", response_model=schemas.BookingResponse)
def create_booking(
    booking: schemas.BookingCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    listing = db.query(models.Listing).filter(
        models.Listing.id == booking.listing_id
    ).first()

    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")

    if listing.owner_id == current_user.id:
        raise HTTPException(status_code=400, detail="You cannot book your own listing")

    if booking.start_date >= booking.end_date:
        raise HTTPException(status_code=400, detail="Invalid date range")

    # Check overlapping bookings
    existing_booking = db.query(models.Booking).filter(
        models.Booking.listing_id == booking.listing_id,
        models.Booking.end_date > booking.start_date,
        models.Booking.start_date < booking.end_date
    ).first()

    if existing_booking:
        raise HTTPException(status_code=400, detail="Listing already booked for these dates")

    new_booking = models.Booking(
        user_id=current_user.id,
        listing_id=booking.listing_id,
        start_date=booking.start_date,
        end_date=booking.end_date
    )

    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)

    return new_booking