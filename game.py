# game.py (GÜNCELLENMİŞ VE OPTİMİZE EDİLMİŞ HALİ)
import pygame
import sys
from scenes.menu_scene import MenuScene
from sound_manager import sound_manager

class Game:
    def __init__(self):
        pygame.init()
        
        # Ekran ayarları
        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Okul Öncesi Eğitici Oyun")
        self.clock = pygame.time.Clock()
        
        # Ses yöneticisini başlat
        try:
            sound_manager.load_sounds()
            print("✅ Sesler başarıyla yüklendi.")
        except Exception as e:
            print(f"❌ Ses yükleme hatası: {e}")
            # Sesler yüklenemese bile oyun devam etsin
            sound_manager.enabled = False
        
        # Menü sesini 1 KERE çal (eğer sesler yüklendiyse)
        if sound_manager.enabled:
            sound_manager.play('menu', loops=0)
        
        # İlk sahneyi ayarla
        self.scene = MenuScene()
        self.last_scene_change = pygame.time.get_ticks()
        
        # Minimum sahne değişim süresi (ms)
        self.MIN_SCENE_CHANGE_DELAY = 500
    
    def run(self):
        running = True
        while running:
            current_time = pygame.time.get_ticks()
            events = pygame.event.get()
            
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    # ESC tuşu ile her zaman menüye dön
                    if event.key == pygame.K_ESCAPE:
                        from scenes.menu_scene import MenuScene
                        self.switch_to_scene(MenuScene())
                        if sound_manager.enabled:
                            sound_manager.play('click', force=True)
            
            # Sahne işlemleri
            self.scene.process_input(events)
            self.scene.update()
            self.scene.render(self.screen)
            
            # Sahne geçişi kontrolü
            if self.scene.next_scene != self.scene:
                # Minimum sahne değişim süresini kontrol et
                if current_time - self.last_scene_change > self.MIN_SCENE_CHANGE_DELAY:
                    self.switch_to_scene(self.scene.next_scene)
                    self.last_scene_change = current_time
            
            pygame.display.flip()
            self.clock.tick(60)  # 60 FPS
        
        pygame.quit()
        sys.exit()
    
    def switch_to_scene(self, new_scene):
        """Sahneyi güvenle değiştir"""
        if sound_manager.enabled:
            # Geçiş sesi (çakışma olmaması için force=False)
            sound_manager.play('transition', force=False)
            
            # Sesin çalması için kısa bir bekleme
            pygame.time.delay(200)
        
        # Eski sahneyi temizle
        if hasattr(self.scene, 'cleanup'):
            self.scene.cleanup()
        
        # Yeni sahneyi ayarla
        self.scene = new_scene
        print(f"🔀 Sahne değiştirildi: {type(new_scene).__name__}")