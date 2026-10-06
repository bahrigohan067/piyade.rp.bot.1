# -*- coding: utf-8 -*-
"""
Piyade RP Bot 1 - Araç Sistemi & Araç Logları Yönetim Modülü
Tüm araç satın alımları, sahiplikleri, plakaları, durumları ve işlem geçmişini yönetir.
Tekil veri dosyası: data/arac_data.json
"""

import time
import uuid
import datetime
from typing import Dict, Any, List, Optional

from config import ARAC_DATA_FILE
from utils.storage import async_load_json, async_save_json
from utils.logger import setup_logger

logger = setup_logger("AracManager")

def _simdiki_zaman_str() -> str:
    """Türkiye saatiyle ISO formatlı zaman damgası döner."""
    tz = datetime.timezone(datetime.timedelta(hours=3))
    return datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")

async def get_arac_data() -> Dict[str, Any]:
    """Araç veri tabanını güvenli şekilde okur."""
    data = await async_load_json(ARAC_DATA_FILE, {})
    data.setdefault("araclar", {})
    data.setdefault("kullanicilar", {})
    data.setdefault("plakalar", {})
    data.setdefault("loglar", [])
    data.setdefault("katalog", {})
    return data

async def save_arac_data(data: Dict[str, Any]) -> bool:
    """Araç veri tabanını atomik olarak kaydeder."""
    return await async_save_json(ARAC_DATA_FILE, data)

async def plaka_kullaniliyor_mu(plaka: str) -> bool:
    """Verilen plakanın daha önce kaydedilip edilmediğini kontrol eder."""
    data = await get_arac_data()
    temiz_plaka = plaka.strip().upper()
    return temiz_plaka in data["plakalar"]

async def arac_ekle(
    sahip_id: int,
    marka_model: str,
    sinif: str,
    plaka: str,
    renk: str = "Siyah",
    fiyat: int = 0,
    roblox_kullanici: str = "",
    ekleyen_yetkili_id: Optional[int] = None,
    notlar: str = ""
) -> Dict[str, Any]:
    """
    Kullanıcıya yeni bir araç tanımlar, plakayı rezerve eder ve log kaydı oluşturur.
    """
    data = await get_arac_data()
    temiz_plaka = plaka.strip().upper()

    if temiz_plaka in data["plakalar"]:
        return {"success": False, "message": f"`{temiz_plaka}` plakası zaten başka bir araca ait!"}

    # Benzersiz araç kimliği (Örn: ARC-A1B2C3)
    arac_id = f"ARC-{uuid.uuid4().hex[:6].upper()}"
    tarih = _simdiki_zaman_str()

    arac_obj = {
        "arac_id": arac_id,
        "sahip_id": int(sahip_id),
        "roblox_kullanici": roblox_kullanici.strip(),
        "marka_model": marka_model.strip(),
        "sinif": sinif.strip(),
        "plaka": temiz_plaka,
        "renk": renk.strip(),
        "fiyat": fiyat,
        "durum": "Aktif",  # "Aktif", "Garajda", "Bağlandı/Çekildi", "Hurda"
        "satin_alma_tarihi": tarih,
        "notlar": notlar.strip(),
    }

    # 1. Araç kaydı
    data["araclar"][arac_id] = arac_obj

    # 2. Kullanıcı sahiplik listesi
    uid_str = str(sahip_id)
    if uid_str not in data["kullanicilar"]:
        data["kullanicilar"][uid_str] = []
    data["kullanicilar"][uid_str].append(arac_id)

    # 3. Plaka dizini
    data["plakalar"][temiz_plaka] = arac_id

    # 4. İşlem Logu
    log_kaydi = {
        "log_id": f"LOG-{int(time.time())}-{uuid.uuid4().hex[:4]}",
        "islem": "ARAC_EKLEME",
        "arac_id": arac_id,
        "sahip_id": int(sahip_id),
        "yetkili_id": ekleyen_yetkili_id,
        "plaka": temiz_plaka,
        "marka_model": marka_model,
        "detay": f"Yeni araç tanımlandı. ({marka_model} - {temiz_plaka})",
        "tarih": tarih
    }
    data["loglar"].append(log_kaydi)

    await save_arac_data(data)
    logger.info(f"Yeni araç eklendi: {arac_id} | Sahip: {sahip_id} | Plaka: {temiz_plaka}")
    return {"success": True, "arac": arac_obj, "log": log_kaydi}

async def arac_getir(arac_id: str) -> Optional[Dict[str, Any]]:
    """Araç ID ile araç detaylarını getirir."""
    data = await get_arac_data()
    return data["araclar"].get(arac_id.strip().upper())

async def plaka_ile_arac_getir(plaka: str) -> Optional[Dict[str, Any]]:
    """Plaka ile aracı sorgular."""
    data = await get_arac_data()
    arac_id = data["plakalar"].get(plaka.strip().upper())
    if arac_id:
        return data["araclar"].get(arac_id)
    return None

async def kullanici_araclarini_getir(sahip_id: int) -> List[Dict[str, Any]]:
    """Kullanıcının sahip olduğu tüm aktif araçları listeler."""
    data = await get_arac_data()
    uid_str = str(sahip_id)
    arac_idleri = data["kullanicilar"].get(uid_str, [])
    return [data["araclar"][aid] for aid in arac_idleri if aid in data["araclar"]]

async def arac_devret(
    arac_id: str,
    yeni_sahip_id: int,
    yetkili_id: int,
    sebep: str = ""
) -> Dict[str, Any]:
    """Aracın sahipliğini başka bir kullanıcıya devreder ve loglar."""
    data = await get_arac_data()
    aid = arac_id.strip().upper()

    if aid not in data["araclar"]:
        return {"success": False, "message": "Belirtilen araç bulunamadı."}

    arac = data["araclar"][aid]
    eski_sahip = arac["sahip_id"]

    if eski_sahip == int(yeni_sahip_id):
        return {"success": False, "message": "Araç zaten bu kullanıcıya ait!"}

    # Eski sahibin listesinden çıkar
    eski_uid_str = str(eski_sahip)
    if eski_uid_str in data["kullanicilar"] and aid in data["kullanicilar"][eski_uid_str]:
        data["kullanicilar"][eski_uid_str].remove(aid)

    # Yeni sahibin listesine ekle
    yeni_uid_str = str(yeni_sahip_id)
    if yeni_uid_str not in data["kullanicilar"]:
        data["kullanicilar"][yeni_uid_str] = []
    data["kullanicilar"][yeni_uid_str].append(aid)

    # Araç sahibini güncelle
    arac["sahip_id"] = int(yeni_sahip_id)
    tarih = _simdiki_zaman_str()

    # Log kaydı
    log_kaydi = {
        "log_id": f"LOG-{int(time.time())}-{uuid.uuid4().hex[:4]}",
        "islem": "ARAC_DEVIR",
        "arac_id": aid,
        "eski_sahip_id": eski_sahip,
        "yeni_sahip_id": int(yeni_sahip_id),
        "yetkili_id": int(yetkili_id),
        "plaka": arac["plaka"],
        "detay": f"Araç devredildi. Sebep: {sebep or 'Belirtilmedi'}",
        "tarih": tarih
    }
    data["loglar"].append(log_kaydi)

    await save_arac_data(data)
    logger.info(f"Araç devredildi: {aid} ({eski_sahip} -> {yeni_sahip_id})")
    return {"success": True, "arac": arac, "log": log_kaydi}

async def arac_durum_guncelle(
    arac_id: str,
    yeni_durum: str,
    yetkili_id: int,
    sebep: str = ""
) -> Dict[str, Any]:
    """Aracın durumunu günceller (Örn: Aktif, Garajda, Bağlandı/Çekildi, Hurda)."""
    data = await get_arac_data()
    aid = arac_id.strip().upper()

    if aid not in data["araclar"]:
        return {"success": False, "message": "Belirtilen araç bulunamadı."}

    arac = data["araclar"][aid]
    eski_durum = arac["durum"]
    arac["durum"] = yeni_durum
    tarih = _simdiki_zaman_str()

    log_kaydi = {
        "log_id": f"LOG-{int(time.time())}-{uuid.uuid4().hex[:4]}",
        "islem": "DURUM_GUNCELLEME",
        "arac_id": aid,
        "sahip_id": arac["sahip_id"],
        "yetkili_id": int(yetkili_id),
        "eski_durum": eski_durum,
        "yeni_durum": yeni_durum,
        "detay": f"Araç durumu değiştirildi: {eski_durum} ➔ {yeni_durum}. Sebep: {sebep or 'Yok'}",
        "tarih": tarih
    }
    data["loglar"].append(log_kaydi)

    await save_arac_data(data)
    logger.info(f"Araç durumu güncellendi: {aid} ({eski_durum} -> {yeni_durum})")
    return {"success": True, "arac": arac, "log": log_kaydi}

async def son_arac_loglarini_getir(limit: int = 15) -> List[Dict[str, Any]]:
    """En son yapılan araç işlemlerinin loglarını döner."""
    data = await get_arac_data()
    logs = data.get("loglar", [])
    return logs[-limit:][::-1]
