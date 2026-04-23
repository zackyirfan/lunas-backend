from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import TagihanUtang
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1", tags=["tagihan"])

class TagihanCreate(BaseModel):
    user_id: int
    nama_utang: str
    total_utang: float
    suku_bunga_apr: float
    jenis: str = "paylater"

@router.post("/tagihan")
def tambah_tagihan(tagihan: TagihanCreate, db: Session = Depends(get_db)):
    data = TagihanUtang(
        user_id=tagihan.user_id,
        nama_utang=tagihan.nama_utang,
        total_utang=tagihan.total_utang,
        suku_bunga_apr=tagihan.suku_bunga_apr,
        jenis=tagihan.jenis
    )
    db.add(data)
    db.commit()
    db.refresh(data)
    return data

@router.get("/tagihan/{user_id}")
def get_tagihan(user_id: int, db: Session = Depends(get_db)):
    tagihan = db.query(TagihanUtang).filter(TagihanUtang.user_id == user_id).all()
    if not tagihan:
        raise HTTPException(status_code=404, detail="Tidak ada tagihan untuk user ini")
    return tagihan

@router.delete("/tagihan/{tagihan_id}")
def hapus_tagihan(tagihan_id: int, db: Session = Depends(get_db)):
    tagihan = db.query(TagihanUtang).filter(TagihanUtang.id == tagihan_id).first()
    if not tagihan:
        raise HTTPException(status_code=404, detail="Tagihan tidak ditemukan")
    db.delete(tagihan)
    db.commit()
    return {"message": f"Tagihan {tagihan_id} berhasil dihapus"}