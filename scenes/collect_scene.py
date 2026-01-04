import pygame
import random
import math
from scenes.base_scene import BaseScene
import settings
from sound_manager import sound_manager

class CollectScene(BaseScene):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.SysFont("Comic Sans MS", 45, bold=True)
        self.big_font = pygame.font.SysFont("Comic Sans MS", 70, bold=True)
        
        # SADECE 1 KERE ÇALAR
        sound_manager.play('level1', force=True)
        
        try: self.bg = pygame.transform.scale(pygame.image.load("assets/images/bolum1_bg.png"), (1280, 720))
        except: self.bg = pygame.Surface((1280, 720)); self.bg.fill((34, 139, 34))

        self.load_assets()
        self.setup_stage(1)

    def load_assets(self):
        self.images = {}
        try:
            self.basket_img = pygame.transform.scale(pygame.image.load("assets/images/sepet.png"), (200, 150))
            self.images["elma"] = pygame.transform.scale(pygame.image.load("assets/images/elma.png"), (80, 80))
            self.images["muz"] = pygame.transform.scale(pygame.image.load("assets/images/muz.png"), (80, 80))
        except: pass
        self.particles = []; self.collected_fruits = []
        self.basket_rect = pygame.Rect(540, 500, 200, 150)

    def setup_stage(self, stage):
        self.current_stage = stage; self.objects = []; self.collected_count = 0
        
        if stage == 1:
            self.instruction = "Sepete 5 tane ELMA koy!"
            self.target_type = "elma"; self.target_count = 5
            counts = {"elma": 6, "muz": 4}
        else:
            self.instruction = "Şimdi de 2 tane MUZ ekle!"
            self.target_type = "muz"; self.target_count = 2
            counts = {"elma": 4, "muz": 4}
            # 2. AŞAMA SESİ (KESİN ÇALACAK)
            sound_manager.play('level1_part2', force=True)

        total = []
        for k,v in counts.items(): total.extend([k]*v)
        random.shuffle(total)
        
        for t in total:
            x, y = random.randint(100, 1180), random.randint(100, 450)
            self.objects.append({"type": t, "rect": pygame.Rect(x,y,80,80), "start": (x,y), "img": self.images.get(t), "col": False})

    def process_input(self, events):
        super().process_input(events)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for obj in reversed(self.objects):
                    if not obj["col"] and obj["rect"].collidepoint(event.pos):
                        self.dragging = obj; self.objects.remove(obj); self.objects.append(obj); break
            elif event.type == pygame.MOUSEBUTTONUP and hasattr(self, 'dragging') and self.dragging:
                if self.dragging["rect"].colliderect(self.basket_rect) and self.dragging["type"] == self.target_type:
                    self.dragging["col"] = True; self.collected_count += 1
                    # GÖRSEL EFEKT VAR, SES YOK (Senin isteğin)
                    bx, by = random.randint(550, 650), random.randint(510, 600)
                    self.collected_fruits.append({"img": self.dragging["img"], "rect": pygame.Rect(bx,by,80,80)})
                else: self.dragging["rect"].topleft = self.dragging["start"]
                self.dragging = None

    def update(self):
        if hasattr(self, 'dragging') and self.dragging: self.dragging["rect"].center = pygame.mouse.get_pos()
        
        if self.collected_count >= self.target_count:
            if self.current_stage == 1: 
                self.setup_stage(2)
            else: 
                # SADECE BÖLÜM SONUNDA BRAVO
                self.timer_after_win = getattr(self, 'timer_after_win', 0) + 1
                if self.timer_after_win == 1: sound_manager.play('bravo')
                if self.timer_after_win > 180:
                    settings.complete_level(1)
                    from scenes.menu_scene import MenuScene
                    self.switch_to_scene(MenuScene())

    def render(self, screen):
        screen.blit(self.bg, (0, 0))
        font_s = self.font.render(self.instruction, True, (60,60,60))
        pygame.draw.rect(screen, (255,255,255,230), (640-font_s.get_width()//2-20, 20, font_s.get_width()+40, 70), border_radius=20)
        screen.blit(font_s, (640-font_s.get_width()//2, 30))
        screen.blit(self.basket_img, self.basket_rect)
        for f in self.collected_fruits: screen.blit(f["img"], f["rect"])
        for o in self.objects: 
            if not o["col"]: screen.blit(o["img"], o["rect"])
        sc = self.big_font.render(f"{self.collected_count}/{self.target_count}", True, (255,255,255))
        screen.blit(sc, (760, 550))