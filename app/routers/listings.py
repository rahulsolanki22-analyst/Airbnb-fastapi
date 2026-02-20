from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models, schemas
from ..dependencies import get_db
from ..auth import get_current_user
from fastapi import HTTPException


router = APIRouter(prefix="/listings", tags=["Listings"])


# Create listing (protected)
@router.post("/", response_model=schemas.ListingResponse)
def create_listing(
    listing: schemas.ListingCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    new_listing = models.Listing(
        title=listing.title,
        description=listing.description,
        price=listing.price,
        owner_id=current_user.id
    )

    db.add(new_listing)
    db.commit()
    db.refresh(new_listing)

    return new_listing


# Get all listings (public)
@router.get("/", response_model=list[schemas.ListingResponse])
def get_listings(
    skip: int = 0,
    limit: int = 10,
    min_price: int | None = None,
    max_price: int | None = None,
    search: str | None = None,
    sort_by: str | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Listing)

    # Filter by price range
    if min_price is not None:
        query = query.filter(models.Listing.price >= min_price)

    if max_price is not None:
        query = query.filter(models.Listing.price <= max_price)

    # Search by title (case insensitive)
    if search:
        query = query.filter(models.Listing.title.ilike(f"%{search}%"))

    # Sorting
    if sort_by == "price_asc":
        query = query.order_by(models.Listing.price.asc())
    elif sort_by == "price_desc":
        query = query.order_by(models.Listing.price.desc())

    listings = query.offset(skip).limit(limit).all()
    return listings


@router.get("/{listing_id}", response_model=schemas.ListingResponse)
def get_single_listing(listing_id: int, db: Session = Depends(get_db)):
    listing = db.query(models.Listing).filter(
        models.Listing.id == listing_id
    ).first()

    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")

    return listing

@router.put("/{listing_id}", response_model=schemas.ListingResponse)
def update_listing(
    listing_id: int,
    listing_data: schemas.ListingUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    listing = db.query(models.Listing).filter(
        models.Listing.id == listing_id
    ).first()

    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")

    if listing.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    for key, value in listing_data.model_dump(exclude_unset=True).items():
        setattr(listing, key, value)

    db.commit()
    db.refresh(listing)

    return listing

@router.delete("/{listing_id}")
def delete_listing(
    listing_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    listing = db.query(models.Listing).filter(
        models.Listing.id == listing_id
    ).first()

    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")

    if listing.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    db.delete(listing)
    db.commit()

    return {"message": "Listing deleted"}