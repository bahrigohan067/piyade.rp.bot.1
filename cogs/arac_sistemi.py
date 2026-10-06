# -*- coding: utf-8 -*-
"""
Piyade RP Bot 1 - Araç Sistemi & Araç Logları Modülü (Cog)
Kullanıcıların sahip olduğu araçları, plakaları, durumları ve araç işlem loglarını yönetir.
"""

import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional

from config import Roles, Colors, SUNUCU_ADI
from utils.permissions import is_management, has_any_role
from utils.arac_manager import (
    arac_ekle,
    arac_getir,
    plaka_ile_arac_getir,
    kullanici_araclarini_getir,
    arac_devret,
    arac_durum_guncelle,
    son_arac_loglarini_getir
)

# Araç ekleme ve yönetme yetkisine sahip roller
ARAC_YONETICI_ROLLER = [
    Roles.KURUCU,
    Roles.UST_YONETIM,
    Roles.YONETICI,
    Roles.YONETIM_EKIBI,
    Roles.GARAJ_CLASS_MANAGER,
    Roles.DRIVER_MANAGER
]

def arac_yetkilisi_mi(member: discord.Member) -> bool:
    if is_management(member):
        return True
    return has_any_role(member, ARAC_YONETICI_ROLLER)

class AracSistemiCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # ── 1. Araç Tanımlama / Ekleme ──
    @app_commands.command(name="arac-ekle", description="Bir kullanıcıya yeni bir araç tescil eder (Yetkililere Özel).")
    @app_commands.describe(
        kullanici="Aracın sahibi olacak Discord kullanıcısı",
        marka_model="Araç marka ve modeli (Örn: BMW M5 CS)",
        sinif="Araç sınıfı (Örn: Sedan, Spor, SUV, Süper, Klasik)",
        plaka="Benzersiz plaka (Örn: 34 PRP 101)",
        renk="Araç rengi (Varsayılan: Siyah)",
        fiyat="Araç değeri / fiyatı (Opsiyonel)",
        roblox_kullanici="Sahibin Roblox kullanıcı adı (Opsiyonel)"
    )
    async def arac_ekle_cmd(
        self,
        interaction: discord.Interaction,
        kullanici: discord.Member,
        marka_model: str,
        sinif: str,
        plaka: str,
        renk: str = "Siyah",
        fiyat: int = 0,
        roblox_kullanici: Optional[str] = None
    ):
        if not arac_yetkilisi_mi(interaction.user):
            return await interaction.response.send_message(
                "❌ Bu komutu yalnızca **Garaj / Araç Yetkilileri** kullanabilir.",
                ephemeral=True
            )

        await interaction.response.defer()

        sonuc = await arac_ekle(
            sahip_id=kullanici.id,
            marka_model=marka_model,
            sinif=sinif,
            plaka=plaka,
            renk=renk,
            fiyat=fiyat,
            roblox_kullanici=roblox_kullanici or "",
            ekleyen_yetkili_id=interaction.user.id
        )

        if not sonuc["success"]:
            return await interaction.followup.send(f"❌ {sonuc['message']}", ephemeral=True)

        arac = sonuc["arac"]
        embed = discord.Embed(
            title="🚗 Yeni Araç Tescil Edildi!",
            description=f"**{kullanici.mention}** kullanıcısının envanterine yeni araç başarıyla kaydedildi.",
            color=Colors.SUCCESS
        )
        embed.add_field(name="🆔 Araç ID", value=f"`{arac['arac_id']}`", inline=True)
        embed.add_field(name="🚘 Marka & Model", value=f"**{arac['marka_model']}**", inline=True)
        embed.add_field(name="🏷️ Sınıf", value=f"`{arac['sinif']}`", inline=True)
        embed.add_field(name="🔢 Plaka", value=f"**{arac['plaka']}**", inline=True)
        embed.add_field(name="🎨 Renk", value=f"`{arac['renk']}`", inline=True)
        embed.add_field(name="💰 Fiyat", value=f"`{arac['fiyat']:,} $`" if arac['fiyat'] else "`Belirtilmedi`", inline=True)
        if arac['roblox_kullanici']:
            embed.add_field(name="👤 Roblox Sahibi", value=f"`{arac['roblox_kullanici']}`", inline=True)
        embed.add_field(name="🛡️ Kaydeden Yetkili", value=interaction.user.mention, inline=True)
        embed.set_footer(text=f"{SUNUCU_ADI} • Araç Kayıt Sistemi")

        await interaction.followup.send(embed=embed)

    # ── 2. Araç Sorgulama ──
    @app_commands.command(name="arac-sorgula", description="Plaka veya Araç ID ile bir aracı ve sahibini sorgular.")
    @app_commands.describe(deger="Araç ID (Örn: ARC-1A2B3C) veya Plaka (Örn: 34 PRP 101)")
    async def arac_sorgula_cmd(self, interaction: discord.Interaction, deger: str):
        await interaction.response.defer()

        arac = await arac_getir(deger)
        if not arac:
            arac = await plaka_ile_arac_getir(deger)

        if not arac:
            return await interaction.followup.send(f"❌ `{deger}` bilgisine ait bir araç kaydı bulunamadı.", ephemeral=True)

        sahip = interaction.guild.get_member(arac["sahip_id"])
        sahip_text = sahip.mention if sahip else f"ID: `{arac['sahip_id']}` (Sunucuda Değil)"

        durum_renk = Colors.SUCCESS if arac["durum"] == "Aktif" else Colors.WARNING

        embed = discord.Embed(
            title=f"🚘 Araç Dosyası • {arac['marka_model']}",
            color=durum_renk
        )
        embed.add_field(name="🆔 Araç Kodu", value=f"`{arac['arac_id']}`", inline=True)
        embed.add_field(name="🔢 Plaka", value=f"**{arac['plaka']}**", inline=True)
        embed.add_field(name="👤 Sahip", value=sahip_text, inline=True)
        embed.add_field(name="🏷️ Sınıf", value=f"`{arac['sinif']}`", inline=True)
        embed.add_field(name="🎨 Renk", value=f"`{arac['renk']}`", inline=True)
        embed.add_field(name="📊 Durum", value=f"**{arac['durum']}**", inline=True)
        embed.add_field(name="📅 Tescil Tarihi", value=f"`{arac['satin_alma_tarihi']}`", inline=True)
        if arac.get("roblox_kullanici"):
            embed.add_field(name="🎮 Roblox İsim", value=f"`{arac['roblox_kullanici']}`", inline=True)

        embed.set_footer(text=f"{SUNUCU_ADI} • Araç Veri Tabanı")
        await interaction.followup.send(embed=embed)

    # ── 3. Kullanıcının Kendi Araçlarını Listeleme ──
    @app_commands.command(name="araclarim", description="Sahip olduğunuz tüm araçları ve durumlarını listeler.")
    @app_commands.describe(kullanici="Araçları görüntülenecek üye (Yalnızca yetkililer başkasını seçebilir)")
    async def araclarim_cmd(self, interaction: discord.Interaction, kullanici: Optional[discord.Member] = None):
        target = interaction.user
        if kullanici and kullanici != interaction.user:
            if not arac_yetkilisi_mi(interaction.user):
                return await interaction.response.send_message(
                    "❌ Başka kullanıcıların garajını yalnızca **Araç Yetkilileri** görüntüleyebilir.",
                    ephemeral=True
                )
            target = kullanici

        await interaction.response.defer(ephemeral=True)
        araclar = await kullanici_araclarini_getir(target.id)

        if not araclar:
            return await interaction.followup.send(
                f"ℹ️ {target.mention} adına kayıtlı herhangi bir araç bulunmuyor.",
                ephemeral=True
            )

        embed = discord.Embed(
            title=f"🏎️ {target.display_name} • Garaj Dökümü",
            description=f"Toplam **{len(araclar)}** adet tescilli araç listeleniyor:",
            color=Colors.PRIMARY
        )

        for i, arc in enumerate(araclar, start=1):
            durum_emoji = "🟢" if arc["durum"] == "Aktif" else "🔴"
            embed.add_field(
                name=f"{i}. {arc['marka_model']} ({arc['plaka']})",
                value=(
                    f"└ **ID:** `{arc['arac_id']}` | **Sınıf:** `{arc['sinif']}`\n"
                    f"└ **Renk:** `{arc['renk']}` | **Durum:** {durum_emoji} `{arc['durum']}`"
                ),
                inline=False
            )

        embed.set_footer(text=f"{SUNUCU_ADI} • Garaj Sistemi")
        await interaction.followup.send(embed=embed, ephemeral=True)

    # ── 4. Araç Devretme ──
    @app_commands.command(name="arac-devret", description="Bir aracı başka bir kullanıcıya devreder.")
    @app_commands.describe(
        arac_id="Devredilecek aracın ID'si (Örn: ARC-1A2B3C)",
        yeni_sahip="Aracın devredileceği yeni kullanıcı",
        sebep="Devir sebebi (Satış, hediye vb.)"
    )
    async def arac_devret_cmd(
        self,
        interaction: discord.Interaction,
        arac_id: str,
        yeni_sahip: discord.Member,
        sebep: Optional[str] = None
    ):
        await interaction.response.defer()

        # Yetkili değilse sadece kendi aracını devredebilir
        arac = await arac_getir(arac_id)
        if not arac:
            return await interaction.followup.send("❌ Belirtilen araç bulunamadı.", ephemeral=True)

        if arac["sahip_id"] != interaction.user.id and not arac_yetkilisi_mi(interaction.user):
            return await interaction.followup.send(
                "❌ Bu araç size ait değil ve devir yetkiniz bulunmuyor!",
                ephemeral=True
            )

        sonuc = await arac_devret(
            arac_id=arac_id,
            yeni_sahip_id=yeni_sahip.id,
            yetkili_id=interaction.user.id,
            sebep=sebep or "Kullanıcı içi devir"
        )

        if not sonuc["success"]:
            return await interaction.followup.send(f"❌ {sonuc['message']}", ephemeral=True)

        embed = discord.Embed(
            title="🔄 Araç Devir İşlemi Tamamlandı",
            description=f"**{arac['marka_model']}** (`{arac['plaka']}`) aracı başarıyla yeni sahibine aktarıldı.",
            color=Colors.SUCCESS
        )
        embed.add_field(name="Eski Sahip", value=f"<@{sonuc['log']['eski_sahip_id']}>", inline=True)
        embed.add_field(name="Yeni Sahip", value=yeni_sahip.mention, inline=True)
        embed.add_field(name="İşlemi Yapan", value=interaction.user.mention, inline=True)
        embed.add_field(name="Sebep", value=sebep or "Belirtilmedi", inline=False)
        embed.set_footer(text=f"{SUNUCU_ADI} • Araç Devir Logu")

        await interaction.followup.send(embed=embed)

    # ── 5. Araç Durumu Güncelleme (Çekildi / Garajda / Aktif) ──
    @app_commands.command(name="arac-durum", description="Aracın durumunu değiştirir (Yetkililere Özel).")
    @app_commands.describe(
        arac_id="Durumu güncellenecek aracın ID'si",
        yeni_durum="Aracın yeni durumu",
        sebep="Durum değişikliği sebebi"
    )
    @app_commands.choices(yeni_durum=[
        app_commands.Choice(name="🟢 Aktif (Yollarda)", value="Aktif"),
        app_commands.Choice(name="🅿️ Garajda (Park Halinde)", value="Garajda"),
        app_commands.Choice(name="🚨 Çekildi / Bağlandı (Ceza/Yediemin)", value="Bağlandı/Çekildi"),
        app_commands.Choice(name="💥 Hurda (Kullanılamaz)", value="Hurda")
    ])
    async def arac_durum_cmd(
        self,
        interaction: discord.Interaction,
        arac_id: str,
        yeni_durum: app_commands.Choice[str],
        sebep: Optional[str] = None
    ):
        if not arac_yetkilisi_mi(interaction.user):
            return await interaction.response.send_message(
                "❌ Bu komutu yalnızca **Garaj / Araç Yetkilileri** kullanabilir.",
                ephemeral=True
            )

        await interaction.response.defer()
        sonuc = await arac_durum_guncelle(
            arac_id=arac_id,
            yeni_durum=yeni_durum.value,
            yetkili_id=interaction.user.id,
            sebep=sebep or ""
        )

        if not sonuc["success"]:
            return await interaction.followup.send(f"❌ {sonuc['message']}", ephemeral=True)

        embed = discord.Embed(
            title="📋 Araç Durumu Güncellendi",
            description=f"`{arac_id.upper()}` plakalı/kodlu aracın yeni durumu kaydedildi.",
            color=Colors.WARNING
        )
        embed.add_field(name="Yeni Durum", value=f"**{yeni_durum.name}**", inline=True)
        embed.add_field(name="Yetkili", value=interaction.user.mention, inline=True)
        embed.add_field(name="Sebep", value=sebep or "Belirtilmedi", inline=False)
        embed.set_footer(text=f"{SUNUCU_ADI} • Durum Güncelleme Logu")

        await interaction.followup.send(embed=embed)

    # ── 6. Son Araç Logları ──
    @app_commands.command(name="arac-loglar", description="Son yapılan araç işlemlerini ve kayıt loglarını listeler.")
    @app_commands.describe(adet="Görüntülenecek log sayısı (Varsayılan: 10, En fazla: 25)")
    async def arac_loglar_cmd(self, interaction: discord.Interaction, adet: int = 10):
        if not arac_yetkilisi_mi(interaction.user):
            return await interaction.response.send_message(
                "❌ Bu komutu yalnızca **Garaj / Araç Yetkilileri** kullanabilir.",
                ephemeral=True
            )

        await interaction.response.defer(ephemeral=True)
        limit = max(1, min(adet, 25))
        loglar = await son_arac_loglarini_getir(limit=limit)

        if not loglar:
            return await interaction.followup.send("ℹ️ Henüz kaydedilmiş araç logu bulunmuyor.", ephemeral=True)

        embed = discord.Embed(
            title=f"📜 Son {len(loglar)} Araç İşlem Logu",
            color=Colors.DARK
        )

        for log in loglar:
            islem = log.get("islem", "ISLEM")
            tarih = log.get("tarih", "-")
            detay = log.get("detay", "-")
            yetkili_id = log.get("yetkili_id")
            yetkili_str = f"<@{yetkili_id}>" if yetkili_id else "Sistem"

            embed.add_field(
                name=f"🔹 [{islem}] • {tarih}",
                value=f"└ {detay}\n└ **İşlemi Yapan:** {yetkili_str}",
                inline=False
            )

        embed.set_footer(text=f"{SUNUCU_ADI} • Araç Log Takip Sistemi")
        await interaction.followup.send(embed=embed, ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(AracSistemiCog(bot))
