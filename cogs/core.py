# -*- coding: utf-8 -*-
"""
Piyade RP Bot 1 - Temel Sistem Modülü (Core Cog)
Botun durumunu, gecikme süresini ve genel sistem sağlığını denetler.
"""

import time
import discord
from discord.ext import commands
from discord import app_commands

from config import Colors, SUNUCU_ADI, GUILD_ID
from utils.permissions import is_management

class CoreCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.start_time = time.time()

    @app_commands.command(name="ping", description="Botun Discord ile olan gecikme süresini (MS) ölçer.")
    async def ping_command(self, interaction: discord.Interaction):
        latency = round(self.bot.latency * 1000)
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"Gecikme Süresi: **{latency} ms**",
            color=Colors.SUCCESS
        )
        embed.set_footer(text=f"{SUNUCU_ADI} • Sistem Denetimi")
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="bot-durum", description="Botun çalışma süresini ve modül durumunu görüntüler.")
    async def bot_durum_command(self, interaction: discord.Interaction):
        uptime_seconds = int(time.time() - self.start_time)
        hours, remainder = divmod(uptime_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        uptime_str = f"{hours}s {minutes}d {seconds}sn"

        loaded_cogs = list(self.bot.cogs.keys())
        
        embed = discord.Embed(
            title="⚙️ Piyade RP Sistem Botu • Durum Raporu",
            color=Colors.PRIMARY
        )
        embed.add_field(name="🤖 Bot Adı", value=f"`{self.bot.user}`", inline=True)
        embed.add_field(name="⚡ Gecikme", value=f"`{round(self.bot.latency * 1000)} ms`", inline=True)
        embed.add_field(name="⏱️ Çalışma Süresi", value=f"`{uptime_str}`", inline=True)
        embed.add_field(name="📦 Yüklü Modüller (Cogs)", value=f"`{len(loaded_cogs)}` adet ({', '.join(loaded_cogs) if loaded_cogs else 'Yok'})", inline=False)
        embed.add_field(name="🌐 Sunucu", value=f"ID: `{GUILD_ID}`", inline=False)

        embed.set_footer(text=f"{SUNUCU_ADI} • Altyapı Aktif")
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="oyun-durum", description="ER:LC oyun sunucusunun anlık durumunu ve oyuncu sayısını sorgular.")
    async def oyun_durum_command(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        from utils.erlc import get_server_info

        info = await get_server_info()
        if not info:
            embed = discord.Embed(
                title="❌ ER:LC Sunucu Durumu",
                description="Oyun sunucusuna ulaşılamadı veya `ERLC_API_KEY` geçersiz/tanımsız.",
                color=Colors.DANGER
            )
            return await interaction.followup.send(embed=embed, ephemeral=True)

        current_players = info.get("CurrentPlayers", 0)
        max_players = info.get("MaxPlayers", 40)
        queue = info.get("Queue", [])
        queue_count = len(queue) if isinstance(queue, list) else int(queue or 0)
        server_name = info.get("Name", SUNUCU_ADI)

        embed = discord.Embed(
            title=f"🎮 ER:LC Sunucu Durumu • {server_name}",
            color=Colors.SUCCESS if current_players > 0 else Colors.PRIMARY
        )
        embed.add_field(name="👥 Aktif Oyuncu", value=f"`{current_players}` / `{max_players}`", inline=True)
        embed.add_field(name="⏳ Kuyrukta Bekleyen", value=f"`{queue_count}` kişi", inline=True)
        embed.add_field(name="🛡️ Durum", value="`🟢 Çevrimiçi (Aktif)`", inline=True)
        embed.set_footer(text=f"{SUNUCU_ADI} • ER:LC Canlı Entegrasyon")

        await interaction.followup.send(embed=embed, ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(CoreCog(bot))

