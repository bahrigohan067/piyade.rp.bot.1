# -*- coding: utf-8 -*-
"""
Atomik ve Yarış Durumu (Race Condition) Korumalı JSON Depolama Modülü.
Veri kayıplarını ve bozulmaları önlemek için dosya bazlı kilitler ve atomik os.replace kullanır.
"""

import os
import json
import asyncio
from typing import Any, Dict

_FILE_LOCKS: Dict[str, asyncio.Lock] = {}

def get_file_lock(file_path: str) -> asyncio.Lock:
    """Verilen dosya yoluna özel asenkron kilit nesnesi döndürür."""
    norm_path = os.path.abspath(file_path)
    if norm_path not in _FILE_LOCKS:
        _FILE_LOCKS[norm_path] = asyncio.Lock()
    return _FILE_LOCKS[norm_path]

def load_json(file_path: str, default: Any = None) -> Any:
    """JSON dosyasını güvenli şekilde okur. Dosya yoksa veya bozuksa varsayılan değeri döner."""
    if not os.path.exists(file_path):
        return default if default is not None else {}
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[STORAGE ERROR] {file_path} okunamadı: {e}", flush=True)
        return default if default is not None else {}

def save_json_atomic(file_path: str, data: Any) -> bool:
    """
    Veriyi önce geçici bir .tmp dosyasına yazar, işletim sistemi tamponunu temizler
    ve ardından tek atomik işlemle (os.replace) asıl dosyanın üzerine yazar.
    Bu yöntem elektrik kesintisi veya ani çökmelerde dosyanın 0 bayt kalmasını önler.
    """
    try:
        norm_path = os.path.abspath(file_path)
        os.makedirs(os.path.dirname(norm_path), exist_ok=True)
        tmp_path = norm_path + ".tmp"
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_path, norm_path)
        return True
    except Exception as e:
        print(f"[STORAGE ERROR] {file_path} atomik kaydedilemedi: {e}", flush=True)
        return False

async def async_load_json(file_path: str, default: Any = None) -> Any:
    """Asenkron kilit altında JSON dosyasını okur."""
    lock = get_file_lock(file_path)
    async with lock:
        return load_json(file_path, default)

async def async_save_json(file_path: str, data: Any) -> bool:
    """Asenkron kilit altında yarış durumlarını önleyerek atomik dosya kaydeder."""
    lock = get_file_lock(file_path)
    async with lock:
        return save_json_atomic(file_path, data)
