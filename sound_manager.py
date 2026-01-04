# sound_manager.py
import pygame
import os
import settings
import time

class SoundManager:
    def __init__(self):
        # Yüksek kalite ses ayarları
        pygame.mixer.init(frequency=22050, size=-16, channels=8, buffer=1024)
        self.sounds = {}
        self.music_channel = None
        self.effect_channels = []
        
        # Ses seviyeleri - %70 
        self.music_volume = settings.MUSIC_VOLUME * 0.7
        self.effects_volume = settings.EFFECTS_VOLUME * 0.7
        
        self.enabled = settings.SOUND_ENABLED
        
        # Ses çakışma kontrolü için zamanlayıcılar
        self.last_play_time = {}
        self.min_interval = 0.5
        
        # Efekt kanallarını oluştur
        for i in range(8):
            self.effect_channels.append(pygame.mixer.Channel(i))
            
        self.load_sounds()
    
    def load_sounds(self):
        """TÜM SES DOSYALARINI (SENİN KAYITLARIN VE ÜRETİLENLER) YÜKLE"""
        print("🔊 Ses Kütüphanesi Detaylıca Yükleniyor...")
        
        # Ses haritası: Senin kayıtların (bolumX) ve üretilenler (levelX/l6/bul) bir arada
        s_map = {
            'menu': 'menu.wav', 
            'bravo': 'bravo.wav', 
            'bravo_short': 'bravo_short.wav',
            'level1': 'bolum1_talimat.wav', 
            'level1_part2': 'level1_part2.wav',
            'level2': 'bolum2_talimat.wav',   # SENİN KAYDIN
            'level2_hata': 'bolum2hata_talimat.wav',
            'level3': 'bolum3_talimat.wav',   # SENİN KAYDIN
            'level3_hata': 'bolum3hata_talimat.wav',
            'level4': 'bolum4_talimat.wav',   # SENİN KAYDIN
            'level4_kare': 'bolum4kare_talimat.wav',
            'level4_ucgen': 'bolum4ucgen_talimat.wav',
            'level4_yildiz': 'bolum4yildiz_talimat.wav',
            'level4_daire': 'level4_daire.wav',
            'level5_1': 'level5_1.wav', 
            'level5_2': 'level5_2.wav',
            'l6_total': 'l6_total.wav', 
            'l6_red': 'l6_red.wav', 
            'l6_yellow': 'l6_yellow.wav',
            'level7': 'bolum7_talimat.wav', 
            'level8': 'bolum8_talimat.wav',
            'level9': 'bolum9_talimat.wav', 
            'level10': 'bolum10_talimat.wav'
        }
        
        d = os.path.join("assets", "sounds")
        if os.path.exists(d):
            for k, f in s_map.items():
                p = os.path.join(d, f)
                if os.path.exists(p):
                    try:
                        self.sounds[k] = pygame.mixer.Sound(p)
                        self.sounds[k].set_volume(0.7)
                    except Exception as e:
                        print(f"Hata: {f} yüklenemedi - {e}")
        
            # Dinamik nesne seslerini (bul_ELMA vb.) otomatik yükle
            for f in os.listdir(d):
                if f.startswith("bul_") and f.endswith(".wav"):
                    name = os.path.splitext(f)[0]
                    try:
                        self.sounds[name] = pygame.mixer.Sound(os.path.join(d, f))
                        self.sounds[name].set_volume(0.7)
                    except:
                        pass

        # Eski isim uyumlulukları (Hata almamak için)
        if 'bravo' in self.sounds: self.sounds['correct'] = self.sounds['bravo']
        if 'transition' in self.sounds: self.sounds['click'] = self.sounds['transition']

    def play(self, name, loops=0, force=False):
        """SES ÇAKIŞMASINI ÖNLEYEN GELİŞMİŞ OYNATICI"""
        if not self.enabled: return
        clean_name = name.replace('.wav', '')
        if clean_name not in self.sounds: return
        
        # KRİTİK: Eğer bir ses zaten çalıyorsa ve bu bir talimatsa (force=True), eskisini durdur
        if force or clean_name.startswith('level') or clean_name.startswith('l6') or clean_name.startswith('bul'):
            pygame.mixer.stop() 
        
        # KRİTİK: Eğer bir ses zaten çalıyorsa ve zorunlu değilse, yeni ses araya girmesin
        elif pygame.mixer.get_busy():
            return 

        try:
            self.sounds[clean_name].play(loops=loops)
            self.last_play_time[clean_name] = time.time()
        except:
            pass

    def stop_all(self):
        pygame.mixer.stop()

    def toggle_sound(self):
        self.enabled = not self.enabled
        if not self.enabled: pygame.mixer.stop()

# --- IMPORT HATASINI ÇÖZEN SATIR ---
sound_manager = SoundManager()