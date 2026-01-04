# scenes/size_scene.py
import pygame
import math
import random
from scenes.base_scene import BaseScene
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import settings
from sound_manager import sound_manager

class SizeScene(BaseScene):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.SysFont("Comic Sans MS", 50, bold=True)
        self.big_font = pygame.font.SysFont("Comic Sans MS", 80, bold=True)
        self.sign_font = pygame.font.SysFont("Comic Sans MS", 70, bold=True)
        
        self.current_stage = 1 
        self.game_over = False
        self.timer_after_win = 0
        self.dragging_obj = None
        self.confetti_particles = []
        self.show_confetti = False
        self.falling_items = []
        
        try:
            self.confetti_img = pygame.transform.scale(pygame.image.load("assets/images/konfeti.png").convert_alpha(), (80, 80))
            self.fish_img = pygame.transform.scale(pygame.image.load("assets/images/balik.png").convert_alpha(), (60, 40))
            self.honey_img = pygame.transform.scale(pygame.image.load("assets/images/bal.png").convert_alpha(), (50, 50))
        except:
            self.confetti_img, self.fish_img, self.honey_img = None, None, None
            
        self.slot_x = [320, 640, 960] 
        self.ground_y = 500
        self.sign_positions = [(480, 520), (800, 520)]
        self.sign_colors = [(255, 0, 0), (0, 0, 255)]
        
        self.objects = []
        self.load_stage(self.current_stage)

    def load_stage(self, stage_num):
        self.objects = []; self.confetti_particles = []; self.falling_items = []
        self.show_confetti = False; self.dragging_obj = None
        
        if stage_num == 1:
            self.instruction = "Ayıları küçükten büyüğe sırala!"
            self.targets = ["kucuk", "orta", "buyuk"]
            self.comparison_signs = ["<", "<"]
            sound_manager.play('level5_1', force=True) # TALİMAT SESİ
        else:
            self.instruction = "Şimdi ayıları büyükten küçüğe sırala!"
            self.targets = ["buyuk", "orta", "kucuk"]
            self.comparison_signs = [">", ">"]
            sound_manager.play('level5_2', force=True) # TALİMAT SESİ
            
        size_defs = {"kucuk": (120, 120), "orta": (200, 200), "buyuk": (280, 280)}
        starts = [(200, 650), (540, 620), (880, 650), (1080, 620)]; random.shuffle(starts)
        
        for i, t_type in enumerate(["kucuk", "orta", "buyuk"]):
            try:
                img = pygame.image.load(f"assets/images/ayi_{t_type}.png").convert_alpha()
                img = pygame.transform.scale(img, size_defs[t_type])
            except:
                img = pygame.Surface(size_defs[t_type]); img.fill((150,75,0))
                
            self.objects.append({
                "type": t_type, "img": img, "is_locked": False, 
                "target_x": self.slot_x[self.targets.index(t_type)],
                "rect": img.get_rect(midbottom=starts[i]),
                "original_size": size_defs[t_type], "is_dragging": False
            })
            
        try:
            self.bg = pygame.transform.scale(pygame.image.load("assets/images/bolum5_bg.png"), (1280, 720))
        except:
            self.bg = pygame.Surface((1280, 720)); self.bg.fill((220, 240, 255))
        self.ground_color = (139, 69, 19)

    def create_confetti(self):
        self.show_confetti = True
        for _ in range(40):
            self.confetti_particles.append({
                "pos": [random.randint(0, 1280), random.randint(-800, 0)], 
                "speed": random.uniform(4, 8), "angle": random.randint(0, 360), "rotate_speed": random.randint(3, 12)
            })
        # AŞAMA SONUNDA TEBRİK
        if self.current_stage < 2: sound_manager.play('bravo_short', force=True)
        else: sound_manager.play('bravo', force=True)
            
    def create_falling_items(self):
        for _ in range(30):
            item_type = random.choice(["fish", "honey"])
            img = self.fish_img if item_type == "fish" else self.honey_img
            if img:
                self.falling_items.append({
                    "type": item_type, "img": img, "pos": [random.randint(-100, 1380), random.randint(-200, -50)],
                    "speed": random.uniform(2, 5), "rotation": random.randint(0, 360), "rotate_speed": random.uniform(-3, 3),
                    "sway": random.uniform(-0.5, 0.5), "sway_speed": random.uniform(0.02, 0.05), "sway_offset": random.uniform(0, 6.28)
                })

    def process_input(self, events):
        if self.game_over or self.show_confetti: return
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for obj in reversed(self.objects):
                    if not obj["is_locked"] and obj["rect"].collidepoint(event.pos):
                        self.dragging_obj = obj; obj["is_dragging"] = True
                        self.objects.remove(obj); self.objects.append(obj); break
            if event.type == pygame.MOUSEBUTTONUP and self.dragging_obj:
                dist = math.hypot(self.dragging_obj["rect"].centerx - self.dragging_obj["target_x"], self.dragging_obj["rect"].bottom - self.ground_y)
                if dist < 120:
                    self.dragging_obj["rect"].midbottom = (self.dragging_obj["target_x"], self.ground_y)
                    self.dragging_obj["is_locked"] = True
                else:
                    self.dragging_obj["rect"].midbottom = (self.dragging_obj["rect"].centerx, self.ground_y + 180)
                self.dragging_obj["is_dragging"] = False; self.dragging_obj = None

    def update(self):
        for item in self.falling_items[:]:
            item["pos"][1] += item["speed"]; item["rotation"] += item["rotate_speed"]
            if item["pos"][1] > 800: self.falling_items.remove(item)
                
        if self.show_confetti:
            for p in self.confetti_particles: p["pos"][1] += p["speed"]; p["angle"] += p["rotate_speed"]
                
        if all(obj["is_locked"] for obj in self.objects) and not self.show_confetti: 
            self.create_confetti()
            if len(self.falling_items) == 0: self.create_falling_items()
                
        if self.show_confetti:
            self.timer_after_win += 1
            if self.timer_after_win > 180:
                if self.current_stage == 1:
                    self.current_stage = 2; self.timer_after_win = 0; self.load_stage(2)
                else:
                    self.game_over = True
                    
        if self.game_over:
            self.timer_after_win += 1
            if self.timer_after_win > 180: # OTOMATİK KAPATMA
                settings.complete_level(5)
                from scenes.menu_scene import MenuScene
                self.switch_to_scene(MenuScene())
            
        if self.dragging_obj:
            self.dragging_obj["rect"].center = pygame.mouse.get_pos()

    def render(self, screen):
        screen.blit(self.bg, (0, 0))
        pygame.draw.line(screen, self.ground_color, (200, self.ground_y), (1080, self.ground_y), 8)
        
        for i, x in enumerate(self.slot_x):
            slot_num = self.font.render(str(i+1), True, (100, 100, 100))
            screen.blit(slot_num, (x - slot_num.get_width()//2, self.ground_y - 40))
        
        for i, (sign, pos) in enumerate(zip(self.comparison_signs, self.sign_positions)):
            sign_surf = self.sign_font.render(sign, True, self.sign_colors[i])
            screen.blit(sign_surf, pos)
        
        txt_surf = self.font.render(self.instruction, True, (60, 60, 60))
        pygame.draw.rect(screen, (255, 255, 255, 230), (640-txt_surf.get_width()//2-20, 40, txt_surf.get_width()+40, 80), border_radius=20)
        screen.blit(txt_surf, (640 - txt_surf.get_width()//2, 55))

        for obj in self.objects:
            screen.blit(obj["img"], obj["rect"])
            if obj["is_locked"]: pygame.draw.rect(screen, (0, 200, 0), obj["rect"], 4, border_radius=15)
        
        for item in self.falling_items:
            rot_img = pygame.transform.rotate(item["img"], item["rotation"])
            screen.blit(rot_img, rot_img.get_rect(center=(item["pos"][0], item["pos"][1])))
        
        if self.show_confetti and self.confetti_img:
            for p in self.confetti_particles:
                rot_confetti = pygame.transform.rotate(self.confetti_img, p["angle"])
                screen.blit(rot_confetti, rot_confetti.get_rect(center=(p["pos"][0], p["pos"][1])))
        
        if self.game_over:
            overlay = pygame.Surface((1280, 720), pygame.SRCALPHA); overlay.fill((0, 0, 0, 180)); screen.blit(overlay, (0, 0))
            msg = self.big_font.render("HARİKASIN!", True, (255, 255, 255))
            screen.blit(msg, (640 - msg.get_width()//2, 250))