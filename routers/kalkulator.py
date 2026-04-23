from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from services.avalanche import hitung_avalanche

router = APIRouter(prefix="/api/v1", tags=["kalkulator"])

class TagihanInput(BaseModel):
    nama_utang: str
    total_utang: float
    suku_bunga_apr: float

class AvalancheRequest(BaseModel):
    user_id: int
    tagihan: List[TagihanInput]
    dana_tersedia: float

@router.post("/hitung-avalanche")
def post_hitung_avalanche(request: AvalancheRequest):
    if not request.tagihan:
        raise HTTPException(status_code=400, detail="Daftar tagihan tidak boleh kosong")
    if request.dana_tersedia <= 0:
        raise HTTPException(status_code=400, detail="Dana tersedia harus lebih dari 0")

    tagihan_dict = [t.dict() for t in request.tagihan]
    hasil = hitung_avalanche(tagihan_dict, request.dana_tersedia)

    return {
        "user_id": request.user_id,
        "hasil_kalkulasi": hasil
    }