import secrets
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Path
from fastapi.responses import RedirectResponse
from fastapi.security import APIKeyHeader
from pydantic import ValidationError
from sqlalchemy.orm import Session

from . import models, schemas
from .config import AppConfig
from .database import SessionLocal, engine

header_scheme = APIKeyHeader(name="X-API-TOKEN", auto_error=True)

models.Base.metadata.create_all(bind=engine)

app = FastAPI(**AppConfig().model_dump())


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def api_root():
    return RedirectResponse("/docs")


@app.get("/{short_id}")
def redirect(
    short_id: Annotated[str, Path(title="The shortenete ID.", min_length=6, pattern=r"[A-z0-9]")],
    db: Session = Depends(get_db),
):
    """Redirect urls"""
    obj = db.query(models.URL).filter(models.URL.id == short_id).first()
    return RedirectResponse(obj.target_url, status_code=307)


@app.post("/api/create", response_model=schemas.URL)
def create(url: schemas.URLBase, db: Session = Depends(get_db)):
    """Create new short url."""
    chars = "abcdefghijkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ2345678"
    key = "".join(secrets.choice(chars) for _ in range(6))
    secret_key = secrets.token_urlsafe(24)
    try:
        obj = models.URL(id=key, target_url=str(url.target_url), secret_key=secret_key)
    except ValidationError:
        raise HTTPException(status_code=422, detail="invalid url.")
    db.add(obj)
    db.commit()
    return obj


@app.post("/api/delete/{short_id}")
def delete(
    short_id: Annotated[str, Path(title="The shortenete ID.", min_length=6, pattern=r"[A-z0-9]")],
    secret_key: str = Depends(header_scheme),
    db: Session = Depends(get_db),
):
    """Delete short url entry."""
    obj = db.query(models.URL).filter(models.URL.id == short_id).first()
    if obj is None:
        raise HTTPException(status_code=404)

    if secrets.compare_digest(getattr(obj, "secret_key", ""), secret_key):
        db.delete(obj)
        db.commit()
        return {"status": "deleted"}
    else:
        raise HTTPException(status_code=403, detail="secret_key is invalid.")
