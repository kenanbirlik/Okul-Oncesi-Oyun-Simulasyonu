# scenes/base_scene.py (GÜNCELLENMİŞ)
import pygame
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

import settings

class BaseScene:
    def __init__(self):
        self.next_scene = self
        self.animation_manager = None  # Alt sınıflar kullanabilir
    
    def process_input(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    from scenes.menu_scene import MenuScene
                    self.switch_to_scene(MenuScene())
    
    def update(self):
        if self.animation_manager:
            self.animation_manager.update()
    
    def render(self, screen):
        if self.animation_manager:
            self.animation_manager.draw(screen)
    
    def switch_to_scene(self, next_scene):
        self.next_scene = next_scene
    
    def complete_level(self, level_num):
        settings.complete_level(level_num)
        print(f"✅ Bölüm {level_num} tamamlandı!")
    
    def cleanup(self):
        """Sahne değişiminde kaynakları temizle"""
        pass
    
    def load_image(self, path, size=None, convert_alpha=True):
        """Görsel yükleme yardımcı fonksiyonu"""
        try:
            if convert_alpha:
                img = pygame.image.load(path).convert_alpha()
            else:
                img = pygame.image.load(path).convert()
            
            if size:
                img = pygame.transform.scale(img, size)
            
            return img
        except Exception as e:
            print(f"❌ Görsel yüklenemedi: {path}")
            print(f"   Hata: {e}")
            # Hata durumunda basit bir yüzey döndür
            if size:
                surface = pygame.Surface(size, pygame.SRCALPHA)
            else:
                surface = pygame.Surface((100, 100), pygame.SRCALPHA)
            
            surface.fill((255, 0, 255))  # Magenta renk (hata göstergesi)
            return surface
    
    def draw_text_with_outline(self, screen, text, font, color, outline_color, position, outline_width=2):
        """Dış çizgili metin çizimi"""
        x, y = position
        
        # Dış çizgiyi çiz
        for dx in range(-outline_width, outline_width + 1):
            for dy in range(-outline_width, outline_width + 1):
                if dx != 0 or dy != 0:
                    text_surface = font.render(text, True, outline_color)
                    screen.blit(text_surface, (x + dx, y + dy))
        
        # Ana metni çiz
        text_surface = font.render(text, True, color)
        screen.blit(text_surface, (x, y))
    
    def draw_panel(self, screen, rect, color=(255, 255, 255, 230), border_color=(100, 100, 100), border_width=3, radius=20):
        """Yuvarlak köşeli panel çizimi"""
        # Panel yüzeyi
        panel_surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        pygame.draw.rect(panel_surf, color, panel_surf.get_rect(), border_radius=radius)
        pygame.draw.rect(panel_surf, border_color, panel_surf.get_rect(), border_width, border_radius=radius)
        
        # Ekrana çiz
        screen.blit(panel_surf, rect.topleft)