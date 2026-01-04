import pygame
import random
from scenes.base_scene import BaseScene
from sound_manager import sound_manager
import settings

class HeceScene(BaseScene):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.SysFont("Comic Sans MS", 30, bold=True)
        self.info_font = pygame.font.SysFont("Comic Sans MS", 20, bold=True)
        
        try: self.bg = pygame.transform.scale(pygame.image.load("assets/images/bolum7_bg.png"), (1280, 720))
        except: self.bg = pygame.Surface((1280, 720)); self.bg.fill((200, 200, 255))
        
        self.data_pool = [
            {"ad": "ELMA", "resim": "elma.png"}, {"ad": "MUZ", "resim": "muz.png"},
            {"ad": "AYI", "resim": "ayi_orta.png"}, {"ad": "ÜZÜM", "resim": "uzum.png"},
            {"ad": "PORTAKAL", "resim": "portakal.png"}, {"ad": "ÇİÇEK", "resim": "cicek.png"},
            {"ad": "KOLTUK", "resim": "koltuk.png"}, {"ad": "KIRMIZI BALIK", "resim": "kirmizi_balik.png"},
            {"ad": "SARI BALIK", "resim": "sari_balik.png"}, {"ad": "SEPET", "resim": "sepet.png"},
            {"ad": "KAZAK", "resim": "kazak_mavi.png"}, {"ad": "PANTOLON", "resim": "pantolon_yesil.png"}
        ]
        
        self.current_stage = 1; self.total_stages = 5
        self.setup_stage()

    def setup_stage(self):
        self.is_correct = False; self.timer_after_win = 0
        self.target = random.choice(self.data_pool)
        wrong = random.choice([x for x in self.data_pool if x != self.target])
        self.options = [self.target, wrong]; random.shuffle(self.options)
        
        try:
            self.img1 = pygame.transform.scale(pygame.image.load(f"assets/images/{self.options[0]['resim']}"), (300, 300))
            self.img2 = pygame.transform.scale(pygame.image.load(f"assets/images/{self.options[1]['resim']}"), (300, 300))
        except:
            self.img1 = pygame.Surface((300,300)); self.img1.fill((255,0,0))
            self.img2 = pygame.Surface((300,300)); self.img2.fill((0,0,255))
            
        self.rect1 = self.img1.get_rect(center=(400, 450))
        self.rect2 = self.img2.get_rect(center=(880, 450))
        
        # NESNE İSMİNİ OKU
        sound_key = f"bul_{self.target['ad']}"
        sound_manager.play(sound_key, force=True)

    def process_input(self, events):
        super().process_input(events)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and not self.is_correct:
                if self.rect1.collidepoint(event.pos):
                    if self.options[0] == self.target: self.is_correct = True; sound_manager.play('bravo_short', force=False)
                elif self.rect2.collidepoint(event.pos):
                    if self.options[1] == self.target: self.is_correct = True; sound_manager.play('bravo_short', force=False)

    def update(self):
        if self.is_correct:
            self.timer_after_win += 1
            if self.timer_after_win > 60:
                if self.current_stage < self.total_stages:
                    self.current_stage += 1; self.setup_stage()
                else:
                    settings.complete_level(7)
                    from scenes.menu_scene import MenuScene
                    self.switch_to_scene(MenuScene())

    def render(self, screen):
        screen.blit(self.bg, (0, 0))
        q_txt = f"Hangisi {self.target['ad']}?"
        
        pygame.draw.rect(screen, (255,255,255), (340, 40, 600, 100), border_radius=20)
        pygame.draw.rect(screen, (0,0,0), (340, 40, 600, 100), 4, border_radius=20)
        
        info = self.info_font.render(f"Aşama: {self.current_stage}/{self.total_stages}", True, (100,100,100))
        ques = self.font.render(q_txt, True, (0,0,0))
        screen.blit(info, (640-info.get_width()//2, 50))
        screen.blit(ques, (640-ques.get_width()//2, 85))

        for r, i in [(self.rect1, self.img1), (self.rect2, self.img2)]:
            pygame.draw.rect(screen, (255,255,255), r.inflate(20,20), border_radius=15)
            pygame.draw.rect(screen, (200,200,200), r.inflate(20,20), 3, border_radius=15)
            screen.blit(i, r)