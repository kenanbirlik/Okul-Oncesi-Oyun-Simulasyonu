# scenes/memory_scene.py
import pygame
import random
from scenes.base_scene import BaseScene
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import settings
from sound_manager import sound_manager

class MemoryScene(BaseScene):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.SysFont("Comic Sans MS", 40, bold=True)
        self.big_font = pygame.font.SysFont("Comic Sans MS", 70, bold=True)
        self.info_font = pygame.font.SysFont("Comic Sans MS", 30, bold=True)
        
        # SES BURADA ÇALIYOR
        sound_manager.play('level8')
        
        try: self.bg = pygame.transform.scale(pygame.image.load("assets/images/bolum8_bg.png"), (1280, 720))
        except: self.bg = pygame.Surface((1280, 720)); self.bg.fill((200, 230, 255))
        
        self.card_types = ["elma.png", "muz.png", "portakal.png", "uzum.png", "cicek.png", "sepet.png"]
        self.card_width = 150; self.card_height = 150; self.card_spacing = 20
        self.setup_game()
    
    def load_card_image(self, filename):
        try: return pygame.transform.scale(pygame.image.load(f"assets/images/{filename}"), (self.card_width-20, self.card_height-20))
        except: s = pygame.Surface((130,130)); s.fill((200,200,200)); return s
    
    def setup_game(self):
        self.cards = []; self.selected_cards = []; self.matched_pairs = 0; self.total_pairs = 6
        self.game_over = False; self.timer_after_win = 0; self.wait_time = 0; self.can_click = True
        
        pairs = []
        for i, ct in enumerate(self.card_types):
            img = self.load_card_image(ct)
            for _ in range(2): pairs.append({"id": i, "img": img, "flipped": False, "matched": False})
        random.shuffle(pairs)
        
        start_x = (1280 - (4 * 150 + 3 * 20)) // 2
        for i, card in enumerate(pairs):
            row, col = i // 4, i % 4
            card["rect"] = pygame.Rect(start_x + col*170, 150 + row*170, 150, 150)
            self.cards.append(card)
    
    def process_input(self, events):
        super().process_input(events)
        if self.game_over or not self.can_click: return
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for card in self.cards:
                    if not card["flipped"] and not card["matched"] and card["rect"].collidepoint(event.pos):
                        card["flipped"] = True
                        self.selected_cards.append(card)
                        if len(self.selected_cards) == 2:
                            self.can_click = False
                            self.wait_time = 40 # Bekleme süresi
                        break
    
    def update(self):
        if self.game_over:
            self.timer_after_win += 1
            if self.timer_after_win > 180:
                self.complete_level(8)
                from scenes.menu_scene import MenuScene
                self.switch_to_scene(MenuScene())
            return
        
        if self.wait_time > 0:
            self.wait_time -= 1
            if self.wait_time == 0:
                c1, c2 = self.selected_cards
                if c1["id"] == c2["id"]:
                    c1["matched"] = True; c2["matched"] = True
                    self.matched_pairs += 1
                    sound_manager.play('bravo')
                else:
                    c1["flipped"] = False; c2["flipped"] = False
                self.selected_cards = []
                self.can_click = True
        
        if self.matched_pairs >= self.total_pairs and not self.game_over:
            self.game_over = True
            sound_manager.play('bravo')
    
    def render(self, screen):
        screen.blit(self.bg, (0, 0))
        
        # Başlık ve Kartlar (Önceki kodun aynısı, sadece kısa tuttum)
        title = self.font.render("8. Bölüm: Hafıza Oyunu", True, (60,60,60))
        screen.blit(title, (640-title.get_width()//2, 35))
        
        for card in self.cards:
            if card["flipped"] or card["matched"]:
                pygame.draw.rect(screen, (255,255,255), card["rect"], border_radius=15)
                screen.blit(card["img"], card["img"].get_rect(center=card["rect"].center))
                if card["matched"]: pygame.draw.rect(screen, (0,200,0), card["rect"], 5, border_radius=15)
            else:
                pygame.draw.rect(screen, (100,100,150), card["rect"], border_radius=15)
                q = self.font.render("?", True, (255,255,255))
                screen.blit(q, (card["rect"].centerx-q.get_width()//2, card["rect"].centery-q.get_height()//2))

        if self.game_over:
            overlay = pygame.Surface((1280, 720), pygame.SRCALPHA); overlay.fill((0,0,0,150))
            screen.blit(overlay, (0,0))
            win = self.big_font.render("TEBRİKLER!", True, (255,255,255))
            screen.blit(win, (640-win.get_width()//2, 300))