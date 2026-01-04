# scenes/shape_scene.py
import pygame
import math
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

class ShapeScene(BaseScene):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.SysFont("Comic Sans MS", 45, bold=True)
        self.big_font = pygame.font.SysFont("Comic Sans MS", 75, bold=True)
        
        sound_manager.play('level4')

        self.game_over = False
        self.timer_after_win = 0
        self.dragging_obj = None 
        self.obj_size = (180, 180) 
        self.shape_types = [
            {"type": "kare", "color": (255, 0, 0), "sound": "level4_kare"},
            {"type": "daire", "color": (0, 0, 255), "sound": "level4_daire"},
            {"type": "ucgen", "color": (0, 255, 0), "sound": "level4_ucgen"},
            {"type": "yildiz", "color": (255, 255, 0), "sound": "level4_yildiz"}
        ]
        self.objects = [] 
        self.load_assets_with_alignment()

    def load_assets_with_alignment(self):
        try:
            self.bg = pygame.transform.scale(pygame.image.load("assets/images/bolum4_bg.png"), (1280, 720))
        except:
            self.bg = pygame.Surface((1280, 720)); self.bg.fill((255, 228, 196))

        x_positions = [200, 493, 786, 1080] 
        shadow_order = list(range(4)); random.shuffle(shadow_order)
        shape_order = list(range(4)); random.shuffle(shape_order)

        for i, item in enumerate(self.shape_types):
            obj_data = {"type": item["type"], "is_locked": False, "sound": item["sound"]}
            target_pos = (x_positions[shadow_order[i]], 250)
            start_pos = (x_positions[shape_order[i]], 570)
            obj_data["target_pos"] = target_pos; obj_data["start_pos"] = start_pos

            try:
                raw_shadow = pygame.image.load(f"assets/images/golge_{item['type']}.png").convert_alpha()
                obj_data["shadow_img"] = pygame.transform.scale(raw_shadow, self.obj_size)
            except:
                s = pygame.Surface(self.obj_size, pygame.SRCALPHA); s.fill((100, 100, 100)); obj_data["shadow_img"] = s
            obj_data["shadow_rect"] = obj_data["shadow_img"].get_rect(center=target_pos)

            try:
                raw_shape = pygame.image.load(f"assets/images/sekil_{item['type']}.png").convert_alpha()
                obj_data["shape_img"] = pygame.transform.scale(raw_shape, self.obj_size)
            except:
                s = pygame.Surface(self.obj_size, pygame.SRCALPHA); s.fill(item["color"]); obj_data["shape_img"] = s
            obj_data["shape_rect"] = obj_data["shape_img"].get_rect(center=start_pos)
            self.objects.append(obj_data)

    def process_input(self, events):
        super().process_input(events)
        
        if self.game_over: return
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for obj in reversed(self.objects):
                    if not obj["is_locked"] and obj["shape_rect"].collidepoint(event.pos):
                        self.dragging_obj = obj
                        # Şeklin sesini çal
                        sound_manager.play(obj["sound"])
                        self.objects.remove(obj); self.objects.append(obj); break
            
            if event.type == pygame.MOUSEBUTTONUP and self.dragging_obj:
                dist = math.hypot(self.dragging_obj["shape_rect"].centerx - self.dragging_obj["shadow_rect"].centerx,
                                  self.dragging_obj["shape_rect"].centery - self.dragging_obj["shadow_rect"].centery)
                if dist < 80:
                    self.dragging_obj["shape_rect"].center = self.dragging_obj["shadow_rect"].center
                    self.dragging_obj["is_locked"] = True
                    sound_manager.play('correct')
                else:
                    self.dragging_obj["shape_rect"].center = self.dragging_obj["start_pos"]
                    sound_manager.play('wrong')
                self.dragging_obj = None

    def update(self):
        if all(obj["is_locked"] for obj in self.objects) and not self.game_over:
            self.game_over = True
            sound_manager.play('bravo')

        if self.game_over:
            self.timer_after_win += 1
            if self.timer_after_win > 150:
                self.complete_level(4)
                from scenes.menu_scene import MenuScene
                self.switch_to_scene(MenuScene())
            return
        
        if self.dragging_obj: self.dragging_obj["shape_rect"].center = pygame.mouse.get_pos()

    def render(self, screen):
        screen.blit(self.bg, (0, 0))
        
        txt = self.font.render("Gölgelerin yerini bul ve eşleştir!", True, (60, 60, 60))
        panel_w = txt.get_width() + 60
        panel_h = txt.get_height() + 30
        panel_surf = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
        pygame.draw.rect(panel_surf, (255, 255, 255, 230), panel_surf.get_rect(), border_radius=20)
        pygame.draw.rect(panel_surf, (100, 100, 100), panel_surf.get_rect(), 3, border_radius=20)
        
        screen.blit(panel_surf, (640 - panel_w//2, 20))
        screen.blit(txt, (640 - txt.get_width()//2, 35))
        
        for obj in self.objects: screen.blit(obj["shadow_img"], obj["shadow_rect"])
        for obj in self.objects: screen.blit(obj["shape_img"], obj["shape_rect"])
        
        if self.game_over:
            overlay = pygame.Surface((1280, 720), pygame.SRCALPHA); overlay.fill((0, 0, 0, 180)); screen.blit(overlay, (0, 0))
            msg = self.big_font.render("HARİKA İŞ ÇIKARDIN!", True, (255, 255, 255)); screen.blit(msg, (640 - msg.get_width()//2, 320))