from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from sqlmodel import Session, select
from src.models.models import Detector, User
from src.database import engine

class DetectorCreate(BaseModel):
    user_id: str
    team_name: str
    is_bot: bool
    confidence: int = Field(ge=0, le=100)

class DetectorGet(BaseModel):
    id: int
    user_id: str
    team_name: str
    is_bot: bool
    confidence: int

router = APIRouter(prefix="/detector", tags=["detectors"])

@router.get("/", response_model=DetectorGet)
async def get_detector(id: int):
    with Session(engine) as session:
        detector = session.exec(select(Detector).where(Detector.id == id)).first()

        if not detector:
            raise HTTPException(status_code=404, detail="Detector not found")

        return DetectorGet(
            id=detector.id,
            user_id=detector.user_id,
            team_name=detector.team_name,
            is_bot=detector.is_bot,
            confidence=detector.confidence
        )

@router.post("/")
async def create_detector(detector_data: DetectorCreate):
    with Session(engine) as session:
        user = session.exec(
            select(User).where(User.id == detector_data.user_id)
        ).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        new_detector = Detector(
            user_id=detector_data.user_id,
            team_name=detector_data.team_name,
            is_bot=detector_data.is_bot,
            confidence=detector_data.confidence
        )

        session.add(new_detector)
        session.commit()
        session.refresh(new_detector)

        return new_detector
