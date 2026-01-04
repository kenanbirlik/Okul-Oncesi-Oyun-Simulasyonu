import pygame
import random
from scenes.base_scene import BaseScene
from sound_manager import sound_manager
import settings

class FishScene(BaseScene):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.SysFont("Comic Sans MS", 60, bold=True)
        self.info_font = pygame.font.SysFont("Comic Sans MS", 40, bold=True)
        
        try: self.bg = pygame.transform.scale(pygame.image.load("assets/images/bolum6_bg.png"), (1280, 720))
        except: self.bg = pygame.Surface((1280, 720)); self.bg.fill((0, 105, 148))

        self.red_fish = self.load_img("kirmizi_balik.png", (100,70), (255,0,0))
        self.yellow_fish = self.load_img("sari_balik.png", (100,70), (255,255,0))
        self.setup_stage(1)

    def load_img(self, f, s, c):
        try: return pygame.transform.scale(pygame.image.load(f"assets/images/{f}"), s)
        except: surf = pygame.Surface(s); surf.fill(c); return surf

    def setup_stage(self, stage):
        self.current_stage = stage; self.user_input = ""; self.is_correct = False; self.fishes = []
        r, y = random.randint(2, 5), random.randint(2, 5)
        
        if stage == 1:
            self.q = "Toplam kaç balık var?"; self.target = r + y
            sound_manager.play('l6_total', force=True)
        elif stage == 2:
            self.q = "Kaç tane KIRMIZI balık var?"; self.target = r
            sound_manager.play('l6_red', force=True)
        else:
            self.q = "Kaç tane SARI balık var?"; self.target = y
            sound_manager.play('l6_yellow', force=True)

        for _ in range(r): self.add_fish("red", self.red_fish)
        for _ in range(y): self.add_fish("yellow", self.yellow_fish)

    def add_fish(self, t, img):
        pos = [random.randint(50, 1100), random.randint(100, 500)]
        speed = [random.choice([-1.5, -1, 1, 1.5]), random.choice([-0.8, 0.8])]
        self.fishes.append({"type": t, "img": img, "pos": pos, "speed": speed})

    def process_input(self, events):
        super().process_input(events)
        for event in events:
            if event.type == pygame.KEYDOWN:
                if self.is_correct:
                    if event.key == pygame.K_SPACE:
                        if self.current_stage < 3: self.setup_stage(self.current_stage + 1)
                        else:
                            settings.complete_level(6)
                            from scenes.menu_scene import MenuScene
                            self.switch_to_scene(MenuScene())
                else:
                    if event.key == pygame.K_RETURN:
                        if self.user_input == str(self.target):
                            self.is_correct = True; sound_manager.play('bravo_short', force=False)
                        else: self.user_input = ""
                    elif event.key == pygame.K_BACKSPACE: self.user_input = self.user_input[:-1]
                    elif event.unicode.isdigit(): self.user_input += event.unicode

    def update(self):
        for f in self.fishes:
            f["pos"][0] += f["speed"][0]; f["pos"][1] += f["speed"][1]
            if f["pos"][0] <= 0 or f["pos"][0] >= 1180: f["speed"][0] *= -1
            if f["pos"][1] <= 0 or f["pos"][1] >= 600: f["speed"][1] *= -1

    def render(self, screen):
        screen.blit(self.bg, (0, 0))
        for f in self.fishes:
            img = f["img"] if f["speed"][0] > 0 else pygame.transform.flip(f["img"], True, False)
            screen.blit(img, f["pos"])
            
        q_surf = self.info_font.render(self.q, True, (60, 60, 60))
        pygame.draw.rect(screen, (255,255,255,230), (640-q_surf.get_width()//2-20, 20, q_surf.get_width()+40, 70), border_radius=15)
        screen.blit(q_surf, (640-q_surf.get_width()//2, 30))

        box = pygame.Rect(580, 620, 120, 80)
        pygame.draw.rect(screen, (255,255,255), box, border_radius=15)
        pygame.draw.rect(screen, (0,0,0), box, 4, border_radius=15)
        txt = self.font.render(self.user_input, True, (0,0,0))
        screen.blit(txt, (box.centerx-txt.get_width()//2, box.centery-txt.get_height()//2))
        
        if self.is_correct:
            t = "DOĞRU! BOŞLUK'A BAS" if self.current_stage < 3 else "BİTTİ! BOŞLUK'A BAS"
            screen.blit(self.info_font.render(t, True, (0,200,0)), (450, 350))