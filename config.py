# -*- coding: utf-8 -*-
"""
Piyade RP Bot 1 (Server Check / Sistem Botu) - Konfigürasyon Dosyası
Sunucu rollerini, kanallarını, kimlik bilgilerini ve ortam değişkenlerini yönetir.
"""

import os
from typing import Dict, List, Optional

# =====================================================================
# .ENV DOSYASI OKUYUCU (Lokal test ve esneklik için)
# =====================================================================
env_file = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(env_file):
    with open(env_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip("'\""))

# =====================================================================
# BOT TOKEN & TEMEL SUNUCU AYARLARI
# =====================================================================
# İsteğiniz doğrultusunda token SERVER_TOKEN değişkeninden çekilmektedir
TOKEN: Optional[str] = os.getenv("SERVER_TOKEN")
GUILD_ID: int = int(os.getenv("GUILD_ID", "1529545898294509589"))
SUNUCU_ADI: str = "Piyade RP | Los Angeles"

# =====================================================================
# ER:LC OYUN SUNUCUSU ENTEGRASYON AYARLARI
# =====================================================================
# Oyun sunucusuyla iletişim için ERLC_API_KEY kullanılır (Grup bağlantısı devre dışıdır)
ERLC_API_KEY: str = os.getenv("ERLC_API_KEY", "").strip()
ERLC_BASE_URL: str = "https://api.erlc.gg/v2"
ERLC_SUNUCU_KODU: str = os.getenv("ERLC_SUNUCU_KODU", "piyade")

# =====================================================================
# TEKİL VERİ DOSYASI (ARAÇ SİSTEMİ & ARAÇ LOGLARI)
# =====================================================================
BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))
DATA_DIR: str = os.path.join(BASE_DIR, "data")
ARAC_DATA_FILE: str = os.path.join(DATA_DIR, "arac_data.json")


# =====================================================================
# ROLLER (Adları, ID'leri ve Gruplandırılmış Sabitleri)
# =====================================================================
class Roles:
    # ── Kurucu & Üst Yönetim ──
    SEMBOL = 1545525713032184039                # @| 𖣂
    KURUCU = 1529546007635824680                # @|👤KURUCU
    W = 1542271077206458489                     # @W
    UST_YONETIM = 1539167256246747186           # @|👤Üst Yönetim
    YONETICI = 1534798061845483694              # @|💎Yönetici
    YONETIM_EKIBI = 1537934087166369812         # @|🍁Yönetim Ekibi🍁
    MODERATOR_EKIBI = 1540082352703676516       # @| Moderatör Ekibi
    MOD = 1555628384166346752                   # @| !mod

    # ── Staff Kademeleri ──
    SENIOR_STAFF = 1551241753137254611          # @| Senior Staff
    STAFF = 1551241634094645288                 # @| Staff
    TRIAL_STAFF = 1551241468985737376           # @| Trial Staff

    # ── Özel Departman / Yetkili Rolleri ──
    GARAJ_CLASS_MANAGER = 1546884597311348777   # @| GarajClass Manager
    ILLEGAL_MANAGER = 1551545853141983232       # @| İllegal Manager
    ILLEGAL_SUPERVISOR = 1551546608305573989    # @| İllegal Supervisor
    WHITELIST_YETKILISI = 1551242344190189718   # @| Whitelist Yetkilisi
    TICKET_YETKILISI = 1553333289798869032      # @| 🎫Ticket Yetkilisi
    DESTEK_BEKLEME_YETKILISI = 1553473785527537765 # @| ⏳Destek Bekleme Yetkilisi
    KAPISMA_TALEP_YETKILISI = 1553427352044707840  # @| ⚔️ Kapışma Talep Yetkilisi
    ROBUX_YETKILISI = 1545685296539111494       # @| Robux Alım-Satım Yetkilisi
    ROL_YETKILISI = 1543074569034801244         # @| Rol Yetkilisi
    SES_YETKILISI = 1547526649459777556         # @| 🔉Ses Kanalı Yetkilisi
    ISIM_YETKILISI = 1543075759508164659        # @| İsim Yetkilisi
    MESAJ_DENETIMCISI = 1542249243702726796     # @| 💭Mesaj Denetimcisi
    MANHUNT_MANAGERS = 1540423283952976054      # @| Manhunt Managers
    MANHUNT_EKIBI = 1540417049518407751         # @| Manhunt Ekibi
    RULES_MANAGER = 1539170698344271882         # @|🧾Rules Manager
    DEVELOPER = 1534712195709927605             # @|💻DEVELOPER
    PVP_MANAGER = 1539169640326893589           # @| PVP Manager
    DRIVER_MANAGER = 1539169263124746350        # @| Driver Manager
    BUILDER_MANAGER = 1539170448548429885       # @| Builder Manager

    # ── Çete & Legal / İllegal Rolleri ──
    BOSS = 1551552841716334592                  # @| BOSS
    UNDERBOSS = 1551553107492601876             # @| Underboss
    LEGAL = 1539318613498929193                 # @| Legal
    ILLEGAL = 1539249508314259567               # @| İllegal

    # ── Üyelik & Kayıt Rolleri ──
    UYE = 1533919249985437706                   # @| Üye
    WHITELIST = 1533908873772273715             # @| Whitelist
    GRUP_ONAY_BEKLIYOR = 1556628657878081546    # @| ❔ Grup Onayı Bekliyor
    KAYITSIZ = 1542271426386591894              # @| Kayıtsız
    ONAYLANMIS_BIREY = 1534741499726663690      # @| Onaylanmış birey
    VIP = 1534717680676765867                   # @|👑VİP
    DESTEKCI = 1547559312501641338              # @| ❇️DESTEKÇİ
    DENEYIMLI = 1534724764948631703             # @| Deneyimli
    CANA_YAKIN = 1534757047919317172            # @|💓Cana Yakın
    YAS_18_USTU = 1539361424487481404           # @| 18 Yaş ve Üstü
    POLAT_ANAHTAR = 1534768485803102299         # @|🗝️Polat'ın Odasının Anahtarı
    OZEL_CIFT = 1541223489246076990             # @| Özel Çift
    MUZIK_IZNI = 1547589732937240627            # @| Müzik Açma İzni
    MUSLIM = 1541213549144317953                # @| Müslim
    DEAD_PLAYER = 1544777693030125720           # @| Dead Player
    ERKEK = 1534736940904218755                 # @| ERKEK
    CUTE = 1541213335012376678                  # @| CUTE
    KIZ = 1534736941600342016                   # @| KIZ
    AKTIF = 1534736941973504032                 # @| AKTİF
    WEB_SITE = 1542415011786526780              # @| WEB SİTE
    INSTAGRAM = 1544692476218974228             # @| İnstagram
    YOUTUBE = 1534957731499212900               # @| YOUTUBE
    PIYADE = 1556665122905395332                # @Piyade
    PIYADELER = 1554843177263956148             # @Piyadeler
    EVERYONE = 1529545898294509589              # @everyone

    # ── PvP Kademeleri & Sürücü / İnşaatçı ──
    WARRIOR_PVP = 1541213765410754640           # @| Warrior PvP (Kademe Temel)
    ELITE_PVP = 1541214087155810384             # @| Elite PvP
    MASTER_PVP = 1541215423301681252            # @| Master PvP
    GRAND_MASTER_PVP = 1541215599026372688      # @| Grand Master PvP
    EPIC_PVP = 1541216066532016310              # @| Epic PvP
    LEGEND_PVP = 1541216359541645312            # @| Legend PvP
    MYTHIC_PVP = 1541216610751221851            # @| Mythic PvP
    MYTHIC_GLORY_PVP = 1541216852905041980      # @| Mythic Glory PvP
    PVP = 1534736939675160637                   # @|🛡️PVP
    DRIVER = 1534736940279005326                # @|🏎️DRİVER
    BUILDER = 1534756885016871083               # @|🏗️BUİLDER

    # ── Ceza & Uyarı Rolleri ──
    UYARI_1 = 1534715251323572315               # @|❗UYARI 1 (3 puan)
    UYARI_2 = 1534715383507058749               # @|‼️UYARI 2 (6 puan)
    UYARI_3 = 1534715488716853278               # @|‼️UYARI 3 (9 puan)
    UYARI_4 = 1553054768388374620               # @| ‼️UYARI 4 (12 puan)
    UYARI_5 = 1553055210073497710               # @|‼️UYARI 5 (15 puan)
    JAIL = 1553053929087172768                  # @| Jail
    YASAKLI = 1534715583826759790               # @|🚫Yasaklı / Blacklist
    YETKILI_UYARI_1 = 1551287340444549191       # @| Yetkili Uyarı 1
    YETKILI_UYARI_2 = 1551287502667776130       # @| Yetkili Uyarı 2
    YETKILI_UYARI_3 = 1551287599983755405       # @| Yetkili Uyarı 3

    # ── Bot & Entegrasyon Rolleri ──
    SUNUCU_BOTU = 1544590583106895913           # @Sunucu Botu
    BOTS = 1542262938478575636                  # @BOTS
    ERLC_PIYADELERI = 1544152662784876627       # @🤖ER-LC PİYADELERİ
    ERLC_YAN_CAR = 1547579436361060465          # @| 🤖 ER-LC PİYADELERİ | [yan çar]
    SERVER_BOOSTER = 1534890486316138536        # @| Server Booster
    QUARK_LOGGER = 1533621555920371825          # @🤖Quark Logger
    SUNUCU_BOTLARI = 1534713383587418232        # @| SUNUCU BOTLARI
    MUSIC_BOT = 1557037486478467136             # @Piyade RP | Music Bot
    SERVER_CHECK_BOT = 1557030714518540301      # @Piyade RP | Server Check


# Rol ID -> Orijinal İsim Sözlüğü (Tam Eşleme)
ROLE_NAMES: Dict[int, str] = {
    Roles.SEMBOL: "@| 𖣂",
    Roles.KURUCU: "@|👤KURUCU",
    Roles.W: "@W",
    Roles.SUNUCU_BOTU: "@Sunucu Botu",
    Roles.BOTS: "@BOTS",
    Roles.ERLC_PIYADELERI: "@🤖ER-LC PİYADELERİ",
    Roles.ERLC_YAN_CAR: "@| 🤖 ER-LC PİYADELERİ | [yan çar]",
    Roles.MODERATOR_EKIBI: "@| Moderatör Ekibi",
    Roles.UST_YONETIM: "@|👤Üst Yönetim",
    Roles.GARAJ_CLASS_MANAGER: "@| GarajClass Manager",
    Roles.YONETICI: "@|💎Yönetici",
    Roles.DESTEKCI: "@| ❇️DESTEKÇİ",
    Roles.YONETIM_EKIBI: "@|🍁Yönetim Ekibi🍁",
    Roles.SENIOR_STAFF: "@| Senior Staff",
    Roles.STAFF: "@| Staff",
    Roles.TRIAL_STAFF: "@| Trial Staff",
    Roles.ILLEGAL_MANAGER: "@| İllegal Manager",
    Roles.ILLEGAL_SUPERVISOR: "@| İllegal Supervisor",
    Roles.MOD: "@| !mod",
    Roles.WHITELIST_YETKILISI: "@| Whitelist Yetkilisi",
    Roles.TICKET_YETKILISI: "@| 🎫Ticket Yetkilisi",
    Roles.DESTEK_BEKLEME_YETKILISI: "@| ⏳Destek Bekleme Yetkilisi",
    Roles.KAPISMA_TALEP_YETKILISI: "@| ⚔️ Kapışma Talep Yetkilisi",
    Roles.ROBUX_YETKILISI: "@| Robux Alım-Satım Yetkilisi",
    Roles.ROL_YETKILISI: "@| Rol Yetkilisi",
    Roles.SES_YETKILISI: "@| 🔉Ses Kanalı Yetkilisi",
    Roles.ISIM_YETKILISI: "@| İsim Yetkilisi [ sunucu içerisindeki takma adları yönetir ]",
    Roles.MESAJ_DENETIMCISI: "@| 💭Mesaj Denetimcisi",
    Roles.LEGAL: "@| Legal",
    Roles.ILLEGAL: "@| İllegal",
    Roles.MANHUNT_MANAGERS: "@| Manhunt Managers",
    Roles.MANHUNT_EKIBI: "@| Manhunt Ekibi",
    Roles.RULES_MANAGER: "@|🧾Rules Manager",
    Roles.DEVELOPER: "@|💻DEVELOPER",
    Roles.VIP: "@|👑VİP",
    Roles.DENEYIMLI: "@| Deneyimli",
    Roles.BOSS: "@| BOSS",
    Roles.UNDERBOSS: "@| Underboss",
    Roles.UYE: "@| Üye",
    Roles.WHITELIST: "@| Whitelist",
    Roles.GRUP_ONAY_BEKLIYOR: "@| ❔ Grup Onayı Bekliyor",
    Roles.KAYITSIZ: "@| Kayıtsız",
    Roles.YETKILI_UYARI_1: "@| Yetkili Uyarı 1",
    Roles.YETKILI_UYARI_2: "@| Yetkili Uyarı 2",
    Roles.YETKILI_UYARI_3: "@| Yetkili UyARI 3",
    Roles.UYARI_1: "@|❗UYARI 1",
    Roles.UYARI_2: "@|‼️UYARI 2",
    Roles.UYARI_3: "@|‼️UYARI 3",
    Roles.UYARI_4: "@| ‼️UYARI 4",
    Roles.UYARI_5: "@|‼️UYARI 5",
    Roles.JAIL: "@| Jail",
    Roles.YASAKLI: "@|🚫Yasaklı / Blacklist",
    Roles.OZEL_CIFT: "@| Özel Çift",
    Roles.SERVER_BOOSTER: "@| Server Booster",
    Roles.PVP_MANAGER: "@| PVP Manager",
    Roles.MYTHIC_GLORY_PVP: "@| Mythic Glory PvP",
    Roles.MYTHIC_PVP: "@| Mythic PvP",
    Roles.LEGEND_PVP: "@| Legend PvP",
    Roles.EPIC_PVP: "@| Epic PvP",
    Roles.GRAND_MASTER_PVP: "@| Grand Master PvP",
    Roles.MASTER_PVP: "@| Master PvP",
    Roles.ELITE_PVP: "@| Elite PvP",
    Roles.WARRIOR_PVP: "@| Warrior PvP",
    Roles.PVP: "@|🛡️PVP",
    Roles.DRIVER_MANAGER: "@| Driver Manager",
    Roles.DRIVER: "@|🏎️DRİVER",
    Roles.BUILDER_MANAGER: "@| Builder Manager",
    Roles.BUILDER: "@|🏗️BUİLDER",
    Roles.MUZIK_IZNI: "@| Müzik Açma İzni",
    Roles.MUSLIM: "@| Müslim",
    Roles.DEAD_PLAYER: "@| Dead Player",
    Roles.ERKEK: "@| ERKEK",
    Roles.CUTE: "@| CUTE",
    Roles.KIZ: "@| KIZ",
    Roles.AKTIF: "@| AKTİF",
    Roles.WEB_SITE: "@| WEB SİTE",
    Roles.ONAYLANMIS_BIREY: "@| Onaylanmış birey",
    Roles.CANA_YAKIN: "@|💓Cana Yakın",
    Roles.YAS_18_USTU: "@| 18 Yaş ve Üstü",
    Roles.POLAT_ANAHTAR: "@|🗝️Polat'ın Odasının Anahtarı",
    Roles.INSTAGRAM: "@| İnstagram",
    Roles.YOUTUBE: "@| YOUTUBE",
    Roles.QUARK_LOGGER: "@🤖Quark Logger",
    Roles.SUNUCU_BOTLARI: "@| SUNUCU BOTLARI",
    Roles.MUSIC_BOT: "@Piyade RP | Music Bot",
    Roles.SERVER_CHECK_BOT: "@Piyade RP |  Server Check",
    Roles.PIYADE: "@Piyade",
    Roles.PIYADELER: "@Piyadeler",
    Roles.EVERYONE: "@everyone",
}

# Yetki Kontrol Grupları
MANAGEMENT_ROLES: List[int] = [
    Roles.KURUCU,
    Roles.UST_YONETIM,
    Roles.YONETICI,
    Roles.YONETIM_EKIBI
]

STAFF_ROLES: List[int] = [
    Roles.KURUCU,
    Roles.UST_YONETIM,
    Roles.YONETICI,
    Roles.YONETIM_EKIBI,
    Roles.SENIOR_STAFF,
    Roles.STAFF,
    Roles.TRIAL_STAFF,
    Roles.MOD
]

PVP_TIER_ORDER: List[int] = [
    Roles.WARRIOR_PVP,
    Roles.ELITE_PVP,
    Roles.MASTER_PVP,
    Roles.GRAND_MASTER_PVP,
    Roles.EPIC_PVP,
    Roles.LEGEND_PVP,
    Roles.MYTHIC_PVP,
    Roles.MYTHIC_GLORY_PVP
]

PUNISHMENT_ROLES_MAP: Dict[int, int] = {
    1: Roles.UYARI_1,
    2: Roles.UYARI_2,
    3: Roles.UYARI_3,
    4: Roles.UYARI_4,
    5: Roles.UYARI_5
}

# =====================================================================
# KANALLAR (Adları, ID'leri ve Direkt Discord Bağlantıları)
# =====================================================================
class Channels:
    GENEL_KURALLAR = 1532828330380890452      # Genel kurallar kanalı
    RP_TERIMLERI = 1554940447452037192        # RP terimleri kanalı
    DC_DUYURU = 1541355760829726760           # DC Sunucu Duyuru kanalı
    ETKINLIK_DUYURU = 1551312682924253204     # Etkinlik duyuru kanalı
    RP_DUYURU = 1554103929451581460           # RP Duyuru kanalı
    UYARILAR = 1532828434739368149            # Uyarılar kanalı
    ERLC_GLOBAL_DUYURU = 1541354459408629830  # ER:LC Global duyuru kanalı
    SOSYAL_MEDYA = 1532828546865696889        # Sosyal medya kanalı
    RP_OYLAMA = 1554037075563651182           # RP oylama kanalı
    ROBLOX_GRUP = 1554038042157654016         # Roblox Grup kanalı
    ISTEK_ONERI = 1545562405076209714         # İstek Öneri kanalı
    KAYIT = 1532831582753128530               # Kayıt kanalı
    SOHBET = 1554924057189941258              # Sohbet kanalı
    MEDYA = 1554924097723699270               # Medya kanalı
    PERM_AL = 1554924155927924776             # Perm al kanalı
    MUZIK = 1554924186684629175               # Müzik oynatma kanalı
    BOT_KOMUT = 1554924232897732789           # Bot komut kanalı
    TICKET = 1534770099179884564              # Ticket kanalı
    DESTEK_BEKLEME = 1532829788824404274      # Destek bekleme ses kanalı
    VS_TALEP = 1537136926287593503            # VS talep kanalı
    VS_SONUC = 1537142672953708685            # VS sonuç kanalı
    HOSGELDINIZ = 1532829955409449081         # Hoşgeldiniz kanalı

CHANNEL_NAMES: Dict[int, str] = {
    Channels.GENEL_KURALLAR: "Genel Kurallar",
    Channels.RP_TERIMLERI: "RP Terimleri",
    Channels.DC_DUYURU: "DC Sunucu Duyuru",
    Channels.ETKINLIK_DUYURU: "Etkinlik Duyuru",
    Channels.RP_DUYURU: "RP Duyuru",
    Channels.UYARILAR: "Uyarılar",
    Channels.ERLC_GLOBAL_DUYURU: "ER:LC Global Duyuru",
    Channels.SOSYAL_MEDYA: "Sosyal Medya",
    Channels.RP_OYLAMA: "RP Oylama",
    Channels.ROBLOX_GRUP: "Roblox Grup",
    Channels.ISTEK_ONERI: "İstek Öneri",
    Channels.KAYIT: "Kayıt",
    Channels.SOHBET: "Sohbet",
    Channels.MEDYA: "Medya",
    Channels.PERM_AL: "Perm Al",
    Channels.MUZIK: "Müzik Oynatma",
    Channels.BOT_KOMUT: "Bot Komut",
    Channels.TICKET: "Ticket",
    Channels.DESTEK_BEKLEME: "Destek Bekleme (Ses)",
    Channels.VS_TALEP: "VS Talep",
    Channels.VS_SONUC: "VS Sonuç",
    Channels.HOSGELDINIZ: "Hoşgeldiniz",
}

def get_channel_link(channel_id: int) -> str:
    """Belirtilen kanal için doğrudan tıklanabilir Discord linki üretir."""
    return f"https://discord.com/channels/{GUILD_ID}/{channel_id}"

# =====================================================================
# RENK TEMALARI & GÖRSEL AYARLAR
# =====================================================================
class Colors:
    PRIMARY = 0x2B8CFF        # Canlı Piyade Mavisi
    SUCCESS = 0x2ECC71        # Yeşil (Başarı / Onay)
    WARNING = 0xF1C40F        # Altın Sarısı / Uyarı
    DANGER = 0xE74C3C         # Kırmızı (Hata / Ceza / Red)
    PURPLE = 0x9B59B6         # Mor (İllegal / Özel)
    DARK = 0x2F3136           # Koyu Tema Arkaplan
