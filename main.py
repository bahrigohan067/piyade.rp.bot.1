# -*- coding: utf-8 -*-
"""
Piyade RP Bot 1 (Server Check / Sistem Botu) - Ana Giriş Noktası (Entrypoint)
Mimarisi: discord.py v2.x, dinamik Cog yükleyici, guild slash komut senkronizasyonu.
"""

import sys
import os

# Windows konsolunda Türkçe karakter ve emoji basarken çökmemesi için UTF-8 ayarı
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

import discord
from discord.ext import commands
from discord import app_commands

from config import TOKEN, GUILD_ID, SUNUCU_ADI, Roles
from utils.logger import setup_logger

logger = setup_logger("Main")

intents = discord.Intents.all()

class PiyadeBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!",
            intents=intents,
            help_command=None
        )

    async def setup_hook(self):
        # 1. Cogs (Modül) Klasörünü Dinamik Yükle
        cogs_dir = os.path.join(os.path.dirname(__file__), "cogs")
        if os.path.exists(cogs_dir):
            for filename in sorted(os.listdir(cogs_dir)):
                if filename.endswith(".py") and not filename.startswith("__"):
                    module_name = f"cogs.{filename[:-3]}"
                    try:
                        await self.load_extension(module_name)
                        logger.info(f"✅ Modül yüklendi: {filename}")
                    except Exception as e:
                        logger.error(f"❌ Modül yüklenemedi: {filename} → {e}", exc_info=True)

        # 2. Slash Komutlarını Doğrudan Hedef Sunucuya Senkronize Et
        try:
            guild_obj = discord.Object(id=GUILD_ID)
            self.tree.copy_global_to(guild=guild_obj)
            synced = await self.tree.sync(guild=guild_obj)
            logger.info(f"🚀 [SYNC] {len(synced)} adet slash komutu sunucuya (ID: {GUILD_ID}) senkronize edildi!")
        except Exception as e:
            logger.error(f"⚠️ [SYNC HATA] Komut senkronizasyonu başarısız: {e}")

bot = PiyadeBot()

@bot.event
async def on_ready():
    logger.info("=" * 60)
    logger.info(f"🤖 Bot Aktif: {bot.user} (ID: {bot.user.id})")
    logger.info(f"🏰 Hedef Sunucu ID: {GUILD_ID}")
    logger.info(f"📡 Discord Bağlantı Gecikmesi: {round(bot.latency * 1000)} ms")
    logger.info("=" * 60)

    # Bot Durum Mesajı
    activity = discord.Activity(
        type=discord.ActivityType.watching,
        name=f"{SUNUCU_ADI} • Sistem Denetimi"
    )
    await bot.change_presence(status=discord.Status.online, activity=activity)

@bot.command(name="sync")
async def sync_komutu(ctx: commands.Context):
    """Zorla Slash komut senkronizasyonu yapar (Yalnızca Yönetici ve Kurucular)."""
    is_admin = ctx.author.guild_permissions.administrator
    is_kurucu_role = any(r.id == Roles.KURUCU for r in getattr(ctx.author, "roles", []))
    
    if not (is_admin or is_kurucu_role):
        return await ctx.reply("❌ Bu komutu yalnızca **Kurucu** veya **Yöneticiler** kullanabilir.")

    msg = await ctx.reply("🔄 Komutlar senkronize ediliyor...")
    try:
        guild_obj = discord.Object(id=GUILD_ID)
        bot.tree.copy_global_to(guild=guild_obj)
        synced = await bot.tree.sync(guild=guild_obj)
        await msg.edit(content=f"✅ **{len(synced)} adet** slash komutu başarıyla senkronize edildi!")
    except Exception as e:
        await msg.edit(content=f"❌ Senkronizasyon hatası: `{e}`")

@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    """Slash komut hata yakalayıcısı."""
    logger.error(f"Komut Hatası: {error}", exc_info=error)
    
    if isinstance(error, app_commands.CommandOnCooldown):
        kalan = int(error.retry_after)
        msg = f"⏳ Bu komut beklemede. Lütfen **{kalan} saniye** sonra tekrar deneyin."
    elif isinstance(error, app_commands.MissingPermissions):
        msg = "❌ Bu komutu kullanmak için gerekli yetkiniz bulunmuyor."
    else:
        msg = "⚠️ Komut çalıştırılırken bir hata oluştu."

    try:
        if interaction.response.is_done():
            await interaction.followup.send(msg, ephemeral=True)
        else:
            await interaction.response.send_message(msg, ephemeral=True)
    except Exception:
        pass

if __name__ == "__main__":
    if not TOKEN:
        logger.critical("❌ HATA: SERVER_TOKEN ortam değişkeni bulunamadı!")
        logger.critical("Lütfen .env dosyasına veya barındırma paneline SERVER_TOKEN=<token> ekleyin.")
        sys.exit(1)

    bot.run(TOKEN)
