# -*- coding: utf-8 -*-
"""
Piyade RP Bot 1 - ER:LC Oyun Sunucusu Entegrasyon İstemcisi
Roblox ER:LC (Emergency Response: Liberty County) Private Server API ile iletişim kurar.
"""

import aiohttp
import asyncio
from typing import Optional, Dict, Any, List

from config import ERLC_API_KEY, ERLC_BASE_URL
from utils.logger import setup_logger

logger = setup_logger("ERLC_Client")

_GLOBAL_SESSION: Optional[aiohttp.ClientSession] = None

async def get_session() -> aiohttp.ClientSession:
    """Yeniden kullanılabilir ve soket sızıntısı yapmayan aiohttp oturumu sağlar."""
    global _GLOBAL_SESSION
    if _GLOBAL_SESSION is None or _GLOBAL_SESSION.closed:
        _GLOBAL_SESSION = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=8)
        )
    return _GLOBAL_SESSION

def get_headers() -> Dict[str, str]:
    """ER:LC API kimlik doğrulama başlıklarını döner."""
    return {
        "Server-Key": ERLC_API_KEY,
        "Content-Type": "application/json"
    }

def sanitize_roblox_text(text: str) -> str:
    """Roblox oyun içi komut satırında bozulabilecek Türkçe karakterleri dönüştürür."""
    tr_map = {
        'ı': 'i', 'İ': 'I', 'ş': 's', 'Ş': 'S', 'ğ': 'g', 'Ğ': 'G',
        'ü': 'u', 'Ü': 'U', 'ö': 'o', 'Ö': 'O', 'ç': 'c', 'Ç': 'C'
    }
    for tr_char, safe_char in tr_map.items():
        text = text.replace(tr_char, safe_char)
    return text

async def check_connection() -> Dict[str, Any]:
    """ER:LC sunucu bağlantısını ve API anahtarını test eder."""
    if not ERLC_API_KEY:
        return {"success": False, "message": "ERLC_API_KEY tanımlanmamış."}

    try:
        session = await get_session()
        async with session.get(f"{ERLC_BASE_URL}/server", headers=get_headers()) as resp:
            if resp.status == 200:
                data = await resp.json()
                return {"success": True, "data": data}
            elif resp.status == 403:
                return {"success": False, "message": "Yetkisiz API Anahtarı (403 Forbidden)."}
            else:
                return {"success": False, "message": f"API Yanıt Kodu: {resp.status}"}
    except Exception as e:
        logger.error(f"ER:LC bağlantı testi hatası: {e}")
        return {"success": False, "message": str(e)}

async def get_server_info() -> Optional[Dict[str, Any]]:
    """Oyun sunucusunun anlık genel durumunu (oyuncu sayısı, kuyruk vb.) çeker."""
    if not ERLC_API_KEY:
        return None

    try:
        session = await get_session()
        url = f"{ERLC_BASE_URL}/server?Queue=true"
        async with session.get(url, headers=get_headers()) as resp:
            if resp.status == 200:
                return await resp.json()
    except Exception as e:
        logger.error(f"Sunucu bilgisi alınamadı: {e}")
    return None

async def get_players(with_locations: bool = True) -> List[Dict[str, Any]]:
    """Oyun sunucusundaki aktif oyuncuları ve koordinatlarını çeker."""
    if not ERLC_API_KEY:
        return []

    try:
        session = await get_session()
        param = "true" if with_locations else "false"
        url = f"{ERLC_BASE_URL}/server?Players={param}"
        async with session.get(url, headers=get_headers()) as resp:
            if resp.status == 200:
                data = await resp.json()
                return data.get("Players", [])
    except Exception as e:
        logger.error(f"Oyuncu listesi alınamadı: {e}")
    return []

async def get_kill_logs() -> List[Dict[str, Any]]:
    """Oyun sunucusundaki son öldürme (kill) kayıtlarını çeker."""
    if not ERLC_API_KEY:
        return []

    try:
        session = await get_session()
        url = f"{ERLC_BASE_URL}/server?KillLogs=true"
        async with session.get(url, headers=get_headers()) as resp:
            if resp.status == 200:
                data = await resp.json()
                return data.get("KillLogs", [])
    except Exception as e:
        logger.error(f"Kill logları alınamadı: {e}")
    return []

async def get_join_logs() -> List[Dict[str, Any]]:
    """Oyun sunucusundaki giriş-çıkış loglarını çeker."""
    if not ERLC_API_KEY:
        return []

    try:
        session = await get_session()
        url = f"{ERLC_BASE_URL}/server?JoinLogs=true"
        async with session.get(url, headers=get_headers()) as resp:
            if resp.status == 200:
                data = await resp.json()
                return data.get("JoinLogs", [])
    except Exception as e:
        logger.error(f"Join logları alınamadı: {e}")
    return []

async def send_command(command: str) -> Dict[str, Any]:
    """
    Oyun sunucusuna doğrudan uzaktan komut gönderir (Örn: :m Duyuru metni, :kick vs.).
    v2 ve v1 uç noktaları arasında otomatik geçiş yapar.
    """
    if not ERLC_API_KEY:
        return {"success": False, "message": "ERLC_API_KEY tanımlı değil."}

    clean_cmd = sanitize_roblox_text(command)
    payload = {"command": clean_cmd}
    session = await get_session()

    # Önce v2 uç noktası
    url_v2 = f"{ERLC_BASE_URL}/server/command"
    try:
        async with session.post(url_v2, headers=get_headers(), json=payload) as resp:
            if resp.status in (200, 204):
                logger.info(f"ER:LC Komutu İletildi: '{clean_cmd}'")
                return {"success": True, "status": resp.status}
            elif resp.status == 404:
                # v1 Fallback
                url_v1 = "https://api.erlc.gg/v1/server/command"
                async with session.post(url_v1, headers=get_headers(), json=payload) as resp_v1:
                    if resp_v1.status in (200, 204):
                        logger.info(f"ER:LC v1 Komutu İletildi: '{clean_cmd}'")
                        return {"success": True, "status": resp_v1.status}
                    return {"success": False, "status": resp_v1.status, "message": await resp_v1.text()}
            else:
                return {"success": False, "status": resp.status, "message": await resp.text()}
    except Exception as e:
        logger.error(f"ER:LC komut gönderme hatası: {e}")
        return {"success": False, "message": str(e)}
