# settings.py (GÜNCELLENMİŞ)
import json
import os

# Ayarlar dosyası yolu
SETTINGS_FILE = "game_settings.json"

# Varsayılan ayarlar
DEFAULT_SETTINGS = {
    "theme": "Mavi",
    "sound_enabled": True,
    "music_volume": 0.4,
    "effects_volume": 0.6,
    "completed_levels": [],
    "player_name": "Çocuk"
}

# Tema ayarları
THEMES = [
    {"name": "Mavi", "file": "mavi_bg.png", "btn_color": (100, 150, 255)},
    {"name": "Turuncu", "file": "turuncu_bg.png", "btn_color": (255, 150, 50)},
    {"name": "Pembe", "file": "pembe_bg.png", "btn_color": (255, 150, 200)},
    {"name": "Beyaz", "file": "beyaz_bg.png", "btn_color": (220, 220, 220)}
]

# Geçerli ayarlar
CURRENT_THEME_IMG = "mavi_bg.png"
SOUND_ENABLED = True
MUSIC_VOLUME = 0.4
EFFECTS_VOLUME = 0.6
COMPLETED_LEVELS = set()
PLAYER_NAME = "Çocuk"

def load_settings():
    """Ayarları dosyadan yükle"""
    global CURRENT_THEME_IMG, SOUND_ENABLED, MUSIC_VOLUME, EFFECTS_VOLUME, COMPLETED_LEVELS, PLAYER_NAME
    
    try:
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                settings = json.load(f)
                
                # Tema
                theme_name = settings.get("theme", "Mavi")
                for theme in THEMES:
                    if theme["name"] == theme_name:
                        CURRENT_THEME_IMG = theme["file"]
                        break
                
                # Ses ayarları
                SOUND_ENABLED = settings.get("sound_enabled", True)
                MUSIC_VOLUME = settings.get("music_volume", 0.4)
                EFFECTS_VOLUME = settings.get("effects_volume", 0.6)
                
                # Tamamlanan bölümler
                COMPLETED_LEVELS = set(settings.get("completed_levels", []))
                
                # Oyuncu adı
                PLAYER_NAME = settings.get("player_name", "Çocuk")
                
                print("✅ Ayarlar yüklendi.")
                return True
        else:
            print("ℹ️ Ayarlar dosyası bulunamadı, varsayılan ayarlar kullanılıyor.")
            return False
    except Exception as e:
        print(f"❌ Ayarlar yüklenirken hata: {e}")
        return False

def save_settings():
    """Ayarları dosyaya kaydet"""
    try:
        settings = {
            "theme": next((t["name"] for t in THEMES if t["file"] == CURRENT_THEME_IMG), "Mavi"),
            "sound_enabled": SOUND_ENABLED,
            "music_volume": MUSIC_VOLUME,
            "effects_volume": EFFECTS_VOLUME,
            "completed_levels": list(COMPLETED_LEVELS),
            "player_name": PLAYER_NAME
        }
        
        with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
            json.dump(settings, f, indent=4, ensure_ascii=False)
        
        print("✅ Ayarlar kaydedildi.")
        return True
    except Exception as e:
        print(f"❌ Ayarlar kaydedilirken hata: {e}")
        return False

def complete_level(level_num):
    """Bölümü tamamla ve kaydet"""
    COMPLETED_LEVELS.add(level_num)
    print(f"✅ Bölüm {level_num} tamamlandı!")
    save_settings()

def is_level_completed(level_num):
    """Bölüm tamamlandı mı kontrol et"""
    return level_num in COMPLETED_LEVELS

def toggle_sound():
    """Sesleri aç/kapa"""
    global SOUND_ENABLED
    SOUND_ENABLED = not SOUND_ENABLED
    
    try:
        from sound_manager import sound_manager
        sound_manager.enabled = SOUND_ENABLED
        if not SOUND_ENABLED:
            sound_manager.stop_current()
    except ImportError:
        pass
    
    save_settings()
    print(f"🔊 Ses {'açıldı' if SOUND_ENABLED else 'kapandı'}.")

def set_volumes(music=None, effects=None):
    """Ses seviyelerini ayarla"""
    global MUSIC_VOLUME, EFFECTS_VOLUME
    
    if music is not None:
        MUSIC_VOLUME = max(0.0, min(1.0, music))
    
    if effects is not None:
        EFFECTS_VOLUME = max(0.0, min(1.0, effects))
    
    try:
        from sound_manager import sound_manager
        if music is not None:
            # Müzik ses seviyesi ayarı
            pass
        if effects is not None:
            sound_manager.set_volume(EFFECTS_VOLUME)
    except ImportError:
        pass
    
    save_settings()

def set_theme(theme_name):
    """Tema ayarla"""
    global CURRENT_THEME_IMG
    
    for theme in THEMES:
        if theme["name"] == theme_name:
            CURRENT_THEME_IMG = theme["file"]
            save_settings()
            print(f"🎨 Tema '{theme_name}' olarak ayarlandı.")
            return True
    
    print(f"❌ Tema '{theme_name}' bulunamadı.")
    return False

def set_player_name(name):
    """Oyuncu adını ayarla"""
    global PLAYER_NAME
    
    if name and len(name.strip()) > 0:
        PLAYER_NAME = name.strip()
        save_settings()
        print(f"👤 Oyuncu adı '{PLAYER_NAME}' olarak ayarlandı.")
        return True
    
    return False

# Oyun başlangıcında ayarları yükle
load_settings()
SHOW_TICK_ON_COMPLETE = False # Tik işaretini kapatan ayar (Eğer menüde kullanıyorsan)

def complete_level(level_num):
    """Bölümü tamamla ve kaydet"""
    COMPLETED_LEVELS.add(level_num)