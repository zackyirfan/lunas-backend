from typing import List, Dict

def hitung_avalanche(tagihan: List[Dict], dana_tersedia: float) -> Dict:
    tagihan_sorted = sorted(tagihan, key=lambda x: x["suku_bunga_apr"], reverse=True)

    rencana = []
    sisa_dana = dana_tersedia
    total_bunga_diselamatkan = 0

    for item in tagihan_sorted:
        bunga_bulanan = (item["suku_bunga_apr"] / 100) / 12

        if sisa_dana >= item["total_utang"]:
            alokasi = item["total_utang"]
            status = "LUNAS SEKARANG"
            bunga_diselamatkan = item["total_utang"] * bunga_bulanan * 12

        elif sisa_dana > 0:
            alokasi = sisa_dana
            sisa_utang = item["total_utang"] - alokasi
            bayar_min = max(sisa_utang * 0.02, 50000)
            bulan_lunas = 0
            sisa = sisa_utang

            while sisa > 0:
                bunga = sisa * bunga_bulanan
                sisa = sisa + bunga - bayar_min
                bulan_lunas += 1
                if bulan_lunas > 360:
                    break

            status = f"Sisa {bulan_lunas} bulan"
            bunga_diselamatkan = alokasi * bunga_bulanan * bulan_lunas

        else:
            alokasi = 0
            status = "Dana habis"
            bunga_diselamatkan = 0

        sisa_dana -= alokasi
        total_bunga_diselamatkan += bunga_diselamatkan

        rencana.append({
            "prioritas": len(rencana) + 1,
            "nama_utang": item["nama_utang"],
            "suku_bunga_apr": item["suku_bunga_apr"],
            "total_utang": item["total_utang"],
            "alokasi_pembayaran": round(alokasi, 0),
            "estimasi_status": status,
            "bunga_diselamatkan": round(bunga_diselamatkan, 0)
        })

    return {
        "metode": "Avalanche (Bunga Tertinggi Dulu)",
        "total_dana_digunakan": dana_tersedia - sisa_dana,
        "dana_tidak_terpakai": sisa_dana,
        "total_bunga_diselamatkan": round(total_bunga_diselamatkan, 0),
        "rencana_pembayaran": rencana
    }