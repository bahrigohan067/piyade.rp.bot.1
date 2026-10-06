# -*- coding: utf-8 -*-
"""
Piyade RP Bot 1 - Yetki ve Rol Kontrol Yardımcıları
"""

from typing import Iterable, Optional
import discord
from config import Roles, MANAGEMENT_ROLES, STAFF_ROLES

def has_any_role(member: discord.Member, role_ids: Iterable[int]) -> bool:
    """Kullanıcının verilen rol ID'lerinden herhangi birine sahip olup olmadığını denetler."""
    if not isinstance(member, discord.Member):
        return False
    user_role_ids = {r.id for r in member.roles}
    return any(rid in user_role_ids for rid in role_ids)

def is_kurucu(member: discord.Member) -> bool:
    """Kullanıcının Kurucu rolüne sahip veya sunucu sahibi olup olmadığını denetler."""
    if not isinstance(member, discord.Member):
        return False
    if member.guild.owner_id == member.id:
        return True
    return any(r.id == Roles.KURUCU for r in member.roles)

def is_management(member: discord.Member) -> bool:
    """Kullanıcının Yönetim kadrosunda (Kurucu, Üst Yönetim, Yönetici vb.) olup olmadığını denetler."""
    if not isinstance(member, discord.Member):
        return False
    if is_kurucu(member) or member.guild_permissions.administrator:
        return True
    return has_any_role(member, MANAGEMENT_ROLES)

def is_staff(member: discord.Member) -> bool:
    """Kullanıcının herhangi bir yetkili rolüne sahip olup olmadığını denetler."""
    if not isinstance(member, discord.Member):
        return False
    if is_management(member):
        return True
    return has_any_role(member, STAFF_ROLES)

def get_member_highest_staff_role(member: discord.Member) -> Optional[discord.Role]:
    """Yetkilinin sahip olduğu en yüksek unvan rolünü döndürür."""
    if not isinstance(member, discord.Member):
        return None
    hierarchy = [
        Roles.KURUCU,
        Roles.UST_YONETIM,
        Roles.YONETICI,
        Roles.YONETIM_EKIBI,
        Roles.SENIOR_STAFF,
        Roles.STAFF,
        Roles.TRIAL_STAFF,
        Roles.MOD
    ]
    user_roles_by_id = {r.id: r for r in member.roles}
    for rid in hierarchy:
        if rid in user_roles_by_id:
            return user_roles_by_id[rid]
    return None
