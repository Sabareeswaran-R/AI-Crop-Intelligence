from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database.database import get_db
from database.models import Farmer, Farm, PredictionHistory

router = APIRouter(tags=["Database Management"])


# ============================================================
# SCHEMAS
# ============================================================

class FarmerCreate(BaseModel):
    name: str
    phone: str | None = None
    language: str = "English"


class FarmerUpdate(BaseModel):
    name: str
    phone: str | None = None
    language: str = "English"


class FarmCreate(BaseModel):
    farmer_id: int
    farm_name: str
    area: float
    area_unit: str = "sqft"
    soil_type: str | None = None
    soil_ph: float | None = None
    latitude: float | None = None
    longitude: float | None = None


class FarmUpdate(BaseModel):
    farmer_id: int
    farm_name: str
    area: float
    area_unit: str = "sqft"
    soil_type: str | None = None
    soil_ph: float | None = None
    latitude: float | None = None
    longitude: float | None = None


class PredictionHistoryCreate(BaseModel):
    farmer_id: int
    farm_id: int
    crop: str
    crop_year: int
    season: str
    state: str
    area: float
    rainfall: float
    fertilizer: float
    pesticide: float
    predicted_yield: float


# ============================================================
# HELPERS
# ============================================================

def farmer_to_dict(row: Farmer):
    return {
        "id": row.id,
        "name": row.name,
        "phone": row.phone,
        "language": row.language,
        "created_at": row.created_at.isoformat() if row.created_at else None,
    }


def farm_to_dict(row: Farm):
    return {
        "id": row.id,
        "farmer_id": row.farmer_id,
        "farm_name": row.farm_name,
        "area": row.area,
        "area_unit": row.area_unit,
        "soil_type": row.soil_type,
        "soil_ph": row.soil_ph,
        "latitude": row.latitude,
        "longitude": row.longitude,
        "created_at": row.created_at.isoformat() if row.created_at else None,
    }


def history_to_dict(row: PredictionHistory):
    return {
        "id": row.id,
        "farmer_id": row.farmer_id,
        "farm_id": row.farm_id,
        "crop": row.crop,
        "crop_year": row.crop_year,
        "season": row.season,
        "state": row.state,
        "area": row.area,
        "rainfall": row.rainfall,
        "fertilizer": row.fertilizer,
        "pesticide": row.pesticide,
        "predicted_yield": row.predicted_yield,
        "created_at": row.created_at.isoformat() if row.created_at else None,
    }


# ============================================================
# FARMERS
# ============================================================

@router.get("/farmers")
def list_farmers(db: Session = Depends(get_db)):
    rows = db.query(Farmer).order_by(Farmer.id.asc()).all()
    return [farmer_to_dict(row) for row in rows]


@router.get("/farmers/{farmer_id}")
def get_farmer(farmer_id: int, db: Session = Depends(get_db)):
    row = db.query(Farmer).filter(Farmer.id == farmer_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Farmer not found")
    return farmer_to_dict(row)


@router.post("/farmers")
def create_farmer(data: FarmerCreate, db: Session = Depends(get_db)):
    name = data.name.strip()
    phone = data.phone.strip() if data.phone else None
    language = data.language.strip() if data.language else "English"

    if not name:
        raise HTTPException(status_code=400, detail="Farmer name is required")

    if phone:
        existing = db.query(Farmer).filter(Farmer.phone == phone).first()
        if existing:
            return {
                "message": "Farmer already exists",
                "farmer_id": existing.id,
                **farmer_to_dict(existing),
            }

    row = Farmer(name=name, phone=phone, language=language)
    db.add(row)
    db.commit()
    db.refresh(row)

    return {
        "message": "Farmer created successfully",
        "farmer_id": row.id,
        **farmer_to_dict(row),
    }


@router.put("/farmers/{farmer_id}")
def update_farmer(
    farmer_id: int,
    data: FarmerUpdate,
    db: Session = Depends(get_db),
):
    row = db.query(Farmer).filter(Farmer.id == farmer_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Farmer not found")

    name = data.name.strip()
    phone = data.phone.strip() if data.phone else None
    language = data.language.strip() if data.language else "English"

    if not name:
        raise HTTPException(status_code=400, detail="Farmer name is required")

    if phone:
        duplicate = (
            db.query(Farmer)
            .filter(Farmer.phone == phone, Farmer.id != farmer_id)
            .first()
        )
        if duplicate:
            raise HTTPException(
                status_code=409,
                detail="Another farmer already uses this phone number",
            )

    row.name = name
    row.phone = phone
    row.language = language
    db.commit()
    db.refresh(row)

    return {
        "message": "Farmer updated successfully",
        "farmer_id": row.id,
        **farmer_to_dict(row),
    }


@router.delete("/farmers/{farmer_id}")
def delete_farmer(farmer_id: int, db: Session = Depends(get_db)):
    row = db.query(Farmer).filter(Farmer.id == farmer_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Farmer not found")

    # Delete linked prediction history and farms first.
    farm_ids = [
        item.id
        for item in db.query(Farm.id).filter(Farm.farmer_id == farmer_id).all()
    ]

    if farm_ids:
        db.query(PredictionHistory).filter(
            PredictionHistory.farm_id.in_(farm_ids)
        ).delete(synchronize_session=False)

    db.query(PredictionHistory).filter(
        PredictionHistory.farmer_id == farmer_id
    ).delete(synchronize_session=False)

    db.query(Farm).filter(Farm.farmer_id == farmer_id).delete(
        synchronize_session=False
    )
    db.delete(row)
    db.commit()

    return {
        "message": "Farmer deleted successfully",
        "farmer_id": farmer_id,
        "deleted_farms": len(farm_ids),
    }


@router.get("/farmers/{farmer_id}/farms")
def list_farmer_farms(farmer_id: int, db: Session = Depends(get_db)):
    farmer = db.query(Farmer).filter(Farmer.id == farmer_id).first()
    if not farmer:
        raise HTTPException(status_code=404, detail="Farmer not found")

    rows = (
        db.query(Farm)
        .filter(Farm.farmer_id == farmer_id)
        .order_by(Farm.id.asc())
        .all()
    )
    return [farm_to_dict(row) for row in rows]


# ============================================================
# FARMS
# ============================================================

@router.get("/farms")
def list_farms(db: Session = Depends(get_db)):
    rows = db.query(Farm).order_by(Farm.id.asc()).all()
    return [farm_to_dict(row) for row in rows]


@router.get("/farms/{farm_id}")
def get_farm(farm_id: int, db: Session = Depends(get_db)):
    row = db.query(Farm).filter(Farm.id == farm_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Farm not found")
    return farm_to_dict(row)


@router.post("/farms")
def create_farm(data: FarmCreate, db: Session = Depends(get_db)):
    farmer = db.query(Farmer).filter(Farmer.id == data.farmer_id).first()
    if not farmer:
        raise HTTPException(status_code=404, detail="Selected farmer not found")

    if data.area <= 0:
        raise HTTPException(status_code=400, detail="Area must be greater than 0")

    row = Farm(
        farmer_id=data.farmer_id,
        farm_name=data.farm_name.strip(),
        area=data.area,
        area_unit=data.area_unit,
        soil_type=data.soil_type,
        soil_ph=data.soil_ph,
        latitude=data.latitude,
        longitude=data.longitude,
    )

    if not row.farm_name:
        raise HTTPException(status_code=400, detail="Farm name is required")

    db.add(row)
    db.commit()
    db.refresh(row)

    return {
        "message": "Farm created successfully",
        "farm_id": row.id,
        **farm_to_dict(row),
    }


@router.put("/farms/{farm_id}")
def update_farm(
    farm_id: int,
    data: FarmUpdate,
    db: Session = Depends(get_db),
):
    row = db.query(Farm).filter(Farm.id == farm_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Farm not found")

    farmer = db.query(Farmer).filter(Farmer.id == data.farmer_id).first()
    if not farmer:
        raise HTTPException(status_code=404, detail="Selected farmer not found")

    farm_name = data.farm_name.strip()
    if not farm_name:
        raise HTTPException(status_code=400, detail="Farm name is required")
    if data.area <= 0:
        raise HTTPException(status_code=400, detail="Area must be greater than 0")

    row.farmer_id = data.farmer_id
    row.farm_name = farm_name
    row.area = data.area
    row.area_unit = data.area_unit
    row.soil_type = data.soil_type
    row.soil_ph = data.soil_ph
    row.latitude = data.latitude
    row.longitude = data.longitude

    db.commit()
    db.refresh(row)

    return {
        "message": "Farm updated successfully",
        "farm_id": row.id,
        **farm_to_dict(row),
    }


@router.delete("/farms/{farm_id}")
def delete_farm(farm_id: int, db: Session = Depends(get_db)):
    row = db.query(Farm).filter(Farm.id == farm_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Farm not found")

    db.query(PredictionHistory).filter(
        PredictionHistory.farm_id == farm_id
    ).delete(synchronize_session=False)

    db.delete(row)
    db.commit()

    return {
        "message": "Farm deleted successfully",
        "farm_id": farm_id,
    }


# ============================================================
# PREDICTION HISTORY
# ============================================================

@router.get("/prediction-history")
def list_prediction_history(db: Session = Depends(get_db)):
    rows = (
        db.query(PredictionHistory)
        .order_by(PredictionHistory.id.desc())
        .all()
    )
    return [history_to_dict(row) for row in rows]


@router.post("/prediction-history")
def create_prediction_history(
    data: PredictionHistoryCreate,
    db: Session = Depends(get_db),
):
    farmer = db.query(Farmer).filter(Farmer.id == data.farmer_id).first()
    if not farmer:
        raise HTTPException(status_code=404, detail="Farmer not found")

    farm = db.query(Farm).filter(Farm.id == data.farm_id).first()
    if not farm:
        raise HTTPException(status_code=404, detail="Farm not found")

    row = PredictionHistory(**data.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)

    return {
        "message": "Prediction history saved successfully",
        **history_to_dict(row),
    }
