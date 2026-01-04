# scenes/vowel_scene.py
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

class VowelScene(BaseScene):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.SysFont("Arial", 40, bold=True)
        self.letter_font = pygame.font.SysFont("Arial", 60, bold=True)
        self.big_font = pygame.font.SysFont("Comic Sans MS", 70)
        self.countdown_font = pygame.font.SysFont("Comic Sans MS", 120, bold=True)
        
        self.score = 0
        self.target_score = 15
        self.game_over = False
        self.timer_after_win = 0
        
        # Sadece başlangıç talimatı
        sound_manager.play('level3', force=True)

        self.countdown_active = True
        self.countdown_time = 3 
        self.countdown_timer = 0
        
        self.vowels = ['A', 'E', 'I', 'İ', 'O', 'Ö', 'U', 'Ü']
        self.consonants = ['B', 'C', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'R', 'S', 'T', 'V', 'Y', 'Z']
        
        self.falling_letters = []
        self.spawn_timer = 0
        
        try:
            self.bg = pygame.transform.scale(pygame.image.load("assets/images/bolum3_bg.png"), (1280, 720))
            self.basket_img = pygame.transform.scale(pygame.image.load("assets/images/sepet.png"), (150, 100))
        except:
            self.bg = pygame.Surface((1280, 720)); self.bg.fill((255, 200, 200))
            self.basket_img = pygame.Surface((150, 100)); self.basket_img.fill((139, 69, 19))
            
        self.basket_rect = self.basket_img.get_rect(midbottom=(640, 700))

    def spawn_letter(self):
        is_vowel = random.random() < 0.4
        char = random.choice(self.vowels) if is_vowel else random.choice(self.consonants)
        color = (random.randint(0,200), random.randint(0,200), random.randint(0,200))
        rect = pygame.Rect(random.randint(100, 1180), -50, 50, 50)
        self.falling_letters.append({"char": char, "rect": rect, "is_vowel": is_vowel, "color": color, "speed": random.randint(4, 7)})

    def process_input(self, events):
        super().process_input(events)
        if self.game_over or self.countdown_active: return
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.basket_rect.left > 0: self.basket_rect.x -= 10
        if keys[pygame.K_RIGHT] and self.basket_rect.right < 1280: self.basket_rect.x += 10
        
        # Fare ile kontrol desteği
        mouse_x = pygame.mouse.get_pos()[0]
        self.basket_rect.centerx = mouse_x

    def update(self):
        if self.game_over:
            self.timer_after_win += 1
            if self.timer_after_win == 1:
                # SADECE OYUN BİTİNCE BİR KERE TEBRİK ET
                sound_manager.play('bravo', force=True)
            
            if self.timer_after_win > 180: # Otomatik kapanma
                settings.complete_level(3)
                from scenes.menu_scene import MenuScene
                self.switch_to_scene(MenuScene())
            return

        if self.countdown_active:
            self.countdown_timer += 1
            if self.countdown_timer >= 60:
                self.countdown_timer = 0
                self.countdown_time -= 1
                if self.countdown_time <= 0:
                    self.countdown_active = False
            return

        self.spawn_timer += 1
        if self.spawn_timer > 40:
            self.spawn_letter(); self.spawn_timer = 0
            
        for letter in self.falling_letters[:]:
            letter["rect"].y += letter["speed"]
            if letter["rect"].colliderect(self.basket_rect):
                if letter["is_vowel"]:
                    self.score += 1
                    # Buradaki 'bravo_short' çalma komutu silindi! Sessizce topluyor.
                else:
                    sound_manager.play('level3_hata')
                    self.score = max(0, self.score - 1)
                self.falling_letters.remove(letter)
            elif letter["rect"].y > 720:
                self.falling_letters.remove(letter)
                
        if self.score >= self.target_score:
            self.game_over = True

    def render(self, screen):
        screen.blit(self.bg, (0, 0))
        if self.countdown_active:
            txt = self.countdown_font.render(str(self.countdown_time), True, (255, 255, 255))
            screen.blit(txt, (640 - txt.get_width()//2, 300))
            return

        screen.blit(self.basket_img, self.basket_rect)
        for letter in self.falling_letters:
            l_surf = self.letter_font.render(letter["char"], True, letter["color"])
            screen.blit(l_surf, letter["rect"])
            
        score_surf = self.font.render(f"Puan: {self.score} / {self.target_score}", True, (0, 0, 0))
        screen.blit(score_surf, (20, 20))
        
        if self.game_over:
            overlay = pygame.Surface((1280, 720), pygame.SRCALPHA); overlay.fill((0,0,0,180)); screen.blit(overlay, (0,0))
            msg = self.big_font.render("TEBRİKLER!", True, (255, 255, 255))
            screen.blit(msg, (640 - msg.get_width()//2, 300))