from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nama = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    dynamic_buffer = Column(Float, default=500000.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    tagihan = relationship("TagihanUtang", back_populates="user")
    transaksi = relationship("Transaksi", back_populates="user")

class TagihanUtang(Base):
    __tablename__ = "tagihan_utang"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    nama_utang = Column(String, nullable=False)
    total_utang = Column(Float, nullable=False)
    suku_bunga_apr = Column(Float, nullable=False)
    jenis = Column(String, default="paylater")
    status = Column(String, default="aktif")
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="tagihan")

class Transaksi(Base):
    __tablename__ = "transaksi"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    deskripsi = Column(String, nullable=False)
    jumlah = Column(Float, nullable=False)
    kategori = Column(String, default="konsumtif")
    tanggal = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="transaksi")