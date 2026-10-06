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

async def setup(bot: commands.Bot):
    await bot.add_cog(CoreCog(bot))
