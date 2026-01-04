# sound_manager.py (GÜNCELLENMİŞ)
import pygame
import os
import sys
import settings

class SoundManager:
    def __init__(self):
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        self.sounds = {}
        self.enabled = settings.SOUND_ENABLED
        self.currently_playing = None
        self.load_sounds()
    
    def load_sounds(self):
        """Tüm ses dosyalarını yükle"""
        print("🔊 Ses dosyaları yükleniyor...")
        
        # Ses dosya eşleştirmeleri
        sound_files = {
            # Menü ve genel sesler
            'menu': 'menu.wav',
            'bravo': 'bravo.wav',
            'transition': 'transition.wav',
            'click': 'click.wav',
            'correct': 'correct.wav',
            'wrong': 'wrong.wav',
            
            # Bölüm talimat sesleri
            'level1': 'bolum1_talimat.wav',
            'level1_part2': 'level1_part2.wav',
            'level2': 'bolum2_talimat.wav',
            'level3': 'bolum3_talimat.wav',
            'level4': 'bolum4_talimat.wav',
            'level5_1': 'level5_1.wav',
            'level5_2': 'level5_2.wav',
            'level6_1': 'bolum6_1.wav',
            'level6_2': 'bolum6_2.wav',
            'level6_3': 'bolum6_3.wav',
            'level7': 'bolum7_talimat.wav',
            'level8': 'bolum8_talimat.wav',
            'level9': 'bolum9_talimat.wav',
            'level10': 'bolum10_talimat.wav',
            
            # Hata sesleri
            'level2_hata': 'bolum2hata_talimat.wav',
            'level3_hata': 'bolum3hata_talimat.wav',
            
            # Şekil sesleri
            'level4_kare': 'bolum4kare_talimat.wav',
            'level4_ucgen': 'bolum4ucgen_talimat.wav',
            'level4_yildiz': 'bolum4yildiz_talimat.wav',
            'level4_daire': 'level4_daire.wav'
        }
        
        sounds_dir = os.path.join("assets", "sounds")
        loaded_count = 0
        missing_count = 0
        
        for name, filename in sound_files.items():
            path = os.path.join(sounds_dir, filename)
            if os.path.exists(path):
                try:
                    self.sounds[name] = pygame.mixer.Sound(path)
                    self.sounds[name].set_volume(0.7)
                    loaded_count += 1
                    print(f"   ✓ {filename}")
                except Exception as e:
                    print(f"   ✗ {filename}: {e}")
                    missing_count += 1
            else:
                print(f"   ✗ {filename} (dosya bulunamadı)")
                missing_count += 1
        
        print(f"✅ {loaded_count} ses yüklendi, {missing_count} ses eksik.")
    
    def play(self, name, loops=0, force=False):
        """Sesi çal"""
        if not self.enabled or name not in self.sounds:
            return False
        
        # Talimat seslerinde üst üste binmeyi önle
        if name.startswith('level') and not force:
            # Halihazırda bir talimat sesi çalınıyorsa durdur
            if self.currently_playing and self.currently_playing.startswith('level'):
                self.stop_current()
            
            # Yeni sesi kaydet
            self.currently_playing = name
        
        # Ses çal
        self.sounds[name].play(loops=loops)
        return True
    
    def stop_current(self):
        """Şu anda çalan sesi durdur"""
        pygame.mixer.stop()
        self.currently_playing = None
    
    def stop_music(self):
        """Müziği durdur"""
        pygame.mixer.stop()
        self.currently_playing = None
    
    def toggle_sound(self):
        """Sesleri aç/kapa"""
        self.enabled = not self.enabled
        if not self.enabled:
            self.stop_current()
        print(f"🔊 Ses {'açıldı' if self.enabled else 'kapandı'}")
    
    def set_volume(self, volume):
        """Tüm seslerin seviyesini ayarla"""
        for sound in self.sounds.values():
            sound.set_volume(volume)

# Global ses yöneticisi
sound_manager = SoundManager()