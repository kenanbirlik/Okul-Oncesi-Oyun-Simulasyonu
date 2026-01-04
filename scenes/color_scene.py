# scenes/color_scene.py
import pygame
import random
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from scenes.base_scene import BaseScene
import settings
from sound_manager import sound_manager

class ColorScene(BaseScene):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.SysFont("Comic Sans MS", 45, bold=True)
        self.big_font = pygame.font.SysFont("Comic Sans MS", 75, bold=True)
        
        # SES BAŞLATMA (Senin orijinal bolum2_talimat.wav dosyanı kullanır)
        sound_manager.play("level2", force=True) 
        
        try:
            self.bg = pygame.image.load("assets/images/bolum2_bg.png")
            self.bg = pygame.transform.scale(self.bg, (1280, 720))
        except:
            self.bg = pygame.Surface((1280, 720)); self.bg.fill((135, 206, 235))

        self.current_stage = 1
        self.max_stages = 3
        self.game_over = False
        self.loading_next_stage = False
        self.stage_transition_timer = 0
        self.dragging = None
        self.items = []
        self.timer_after_win = 0 
        self.splash_effects = []
        
        self.stage_data = {
            1: {"c1": "mavi", "c2": "yesil", "obj1": "kazak_mavi.png", "obj2": "pantolon_yesil.png", "rgb1": (0, 0, 255), "rgb2": (0, 255, 0)},
            2: {"c1": "kirmizi", "c2": "sari", "obj1": "top_kirmizi.png", "obj2": "top_sari.png", "rgb1": (255, 0, 0), "rgb2": (255, 255, 0)},
            3: {"c1": "turuncu", "c2": "mor", "obj1": "portakal.png", "obj2": "uzum.png", "rgb1": (255, 165, 0), "rgb2": (128, 0, 128)}
        }
        
        try:
            self.splash_img = pygame.transform.scale(pygame.image.load("assets/images/splash_efect.png").convert_alpha(), (120, 120))
        except:
            self.splash_img = None
        
        self.load_stage(self.current_stage)

    def load_stage(self, stage_num):
        self.items = []; self.dragging = None; data = self.stage_data[stage_num]
        self.bucket1_img = self.load_image_safe(f"kova_{data['c1']}.png", (220, 180), data['rgb1'])
        self.bucket2_img = self.load_image_safe(f"kova_{data['c2']}.png", (220, 180), data['rgb2'])
        obj1_img = self.load_image_safe(data['obj1'], (100, 100), data['rgb1'])
        obj2_img = self.load_image_safe(data['obj2'], (100, 100), data['rgb2'])
        self.b1_rect = self.bucket1_img.get_rect(center=(400, 600))
        self.b2_rect = self.bucket2_img.get_rect(center=(880, 600))
        for _ in range(3):
            self.items.append({"color": "c1", "img": obj1_img, "rect": obj1_img.get_rect(center=(random.randint(150, 1130), random.randint(100, 400)))})
            self.items.append({"color": "c2", "img": obj2_img, "rect": obj2_img.get_rect(center=(random.randint(150, 1130), random.randint(100, 400)))})

    def load_image_safe(self, filename, size, color):
        try:
            img = pygame.image.load(f"assets/images/{filename}").convert_alpha()
            return pygame.transform.scale(img, size)
        except:
            s = pygame.Surface(size); s.fill(color); return s
    
    def create_splash_effect(self, position, color_key):
        if self.splash_img:
            self.splash_effects.append({
                "pos": position, "timer": 0, "max_time": 60, "color_key": color_key, "alpha": 255
            })

    def process_input(self, events):
        super().process_input(events)
        if self.game_over or self.loading_next_stage: return
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for item in reversed(self.items):
                    if item["rect"].collidepoint(event.pos):
                        self.dragging = item; self.items.remove(item); self.items.append(item); break
            if event.type == pygame.MOUSEBUTTONUP and self.dragging:
                if self.dragging["rect"].colliderect(self.b1_rect) and self.dragging["color"] == "c1": 
                    self.create_splash_effect(self.b1_rect.center, "c1")
                    self.items.remove(self.dragging)
                elif self.dragging["rect"].colliderect(self.b2_rect) and self.dragging["color"] == "c2":
                    self.create_splash_effect(self.b2_rect.center, "c2")
                    self.items.remove(self.dragging)
                else: 
                    sound_manager.play('level2_hata')
                    self.dragging["rect"].topleft = (random.randint(150, 1130), random.randint(100, 350))
                self.dragging = None
                    
    def update(self):
        if self.game_over:
            self.timer_after_win += 1
            if self.timer_after_win > 180: # OTOMATİK KAPATMA
                settings.complete_level(2)
                from scenes.menu_scene import MenuScene
                self.switch_to_scene(MenuScene())
            return
            
        elif self.dragging: 
            self.dragging["rect"].center = pygame.mouse.get_pos()
        
        for effect in self.splash_effects[:]:
            effect["timer"] += 1
            effect["alpha"] = 255 - (effect["timer"] / effect["max_time"] * 255)
            if effect["timer"] >= effect["max_time"]:
                self.splash_effects.remove(effect)
        
        # AŞAMA KONTROLÜ
        if len(self.items) == 0 and not self.loading_next_stage:
            self.loading_next_stage = True; self.stage_transition_timer = 0
            
        if self.loading_next_stage:
            self.stage_transition_timer += 1
            if self.stage_transition_timer == 1:
                # SADECE AŞAMA SONUNDA TEBRİK
                if self.current_stage < self.max_stages:
                    sound_manager.play('bravo_short', force=True)
                else:
                    sound_manager.play('bravo', force=True)

            if self.stage_transition_timer > 120: # 2 saniye bekle
                if self.current_stage < self.max_stages: 
                    self.current_stage += 1; 
                    self.load_stage(self.current_stage); 
                    self.loading_next_stage = False
                else: 
                    self.game_over = True

    def render(self, screen):
        screen.blit(self.bg, (0, 0))
        
        txt_surf = self.font.render(f"Aşama {self.current_stage}: Renkleri Eşleştir!", True, (60, 60, 60))
        panel_w, panel_h = txt_surf.get_width() + 60, txt_surf.get_height() + 30
        panel_surf = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
        pygame.draw.rect(panel_surf, (255, 255, 255, 230), panel_surf.get_rect(), border_radius=20)
        pygame.draw.rect(panel_surf, (100, 100, 100), panel_surf.get_rect(), 3, border_radius=20)
        screen.blit(panel_surf, (640 - panel_w//2, 20))
        screen.blit(txt_surf, (640 - txt_surf.get_width()//2, 35))
        
        screen.blit(self.bucket1_img, self.b1_rect); screen.blit(self.bucket2_img, self.b2_rect)
        
        for effect in self.splash_effects:
            if self.splash_img and effect["alpha"] > 0:
                splash_copy = self.splash_img.copy()
                splash_copy.set_alpha(int(effect["alpha"]))
                screen.blit(splash_copy, splash_copy.get_rect(center=effect["pos"]))
        
        for item in self.items: 
            screen.blit(item["img"], item["rect"])
            
        if self.game_over:
            overlay = pygame.Surface((1280, 720), pygame.SRCALPHA); overlay.fill((0, 0, 0, 200)); screen.blit(overlay, (0,0))
            win_txt = self.big_font.render("TEBRİKLER!", True, (255, 215, 0)); screen.blit(win_txt, (640 - win_txt.get_width()//2, 300))