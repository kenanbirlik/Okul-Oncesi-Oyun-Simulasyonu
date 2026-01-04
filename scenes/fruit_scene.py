import pygame
import random
from scenes.base_scene import BaseScene
import sys
import os
# Sahneler klasöründen bir üst dizine (ana dizine) çıkış yolunu ekler
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sound_manager import sound_manager 


class FruitScene(BaseScene):
    def __init__(self):
        super().__init__()
        # Yazı Tipi Ayarı
        self.font = pygame.font.SysFont("Comic Sans MS", 40)
        self.big_font = pygame.font.SysFont("Comic Sans MS", 70)
        
        # Görselleri Yükle (Hata payı bırakmıyoruz)
        try:
            self.bg = pygame.transform.scale(pygame.image.load("assets/images/bahce_bg.png"), (1280, 720))
            self.apple_img = pygame.transform.scale(pygame.image.load("assets/images/elma.png").convert_alpha(), (120, 120))
            self.banana_img = pygame.transform.scale(pygame.image.load("assets/images/muz.png").convert_alpha(), (120, 120))
            self.basket_img = pygame.image.load("assets/images/sepet.png").convert_alpha()
        except:
            # Görsel bulunamazsa düz renkli yüzeyler oluştur (Donmayı önler)
            self.bg = pygame.Surface((1280, 720)); self.bg.fill((144, 238, 144))
            self.apple_img = pygame.Surface((120, 120)); self.apple_img.fill((255, 0, 0))
            self.banana_img = pygame.Surface((120, 120)); self.banana_img.fill((255, 255, 0))
            self.basket_img = pygame.Surface((200, 150)); self.basket_img.fill((139, 69, 19))

        self.basket_rect = self.basket_img.get_rect(center=(640, 600))

        # Oyun Durum Değişkenleri
        self.target_count = 3
        self.collected_count = 0
        self.dragging = None
        self.fruits = []
        self.stars = []
        self.game_over = False
        self.timer_after_win = 0 # Donma yerine zamanlayıcı kullanıyoruz
        
        self.spawn_fruits()

    def spawn_fruits(self):
        for _ in range(5):
            # Elmalar
            self.fruits.append({
                "type": "apple", "img": self.apple_img, 
                "rect": pygame.Rect(random.randint(100, 1100), random.randint(100, 350), 120, 120)
            })
            # Muzlar
            self.fruits.append({
                "type": "banana", "img": self.banana_img, 
                "rect": pygame.Rect(random.randint(100, 1100), random.randint(100, 350), 120, 120)
            })

    def create_stars(self, pos):
        for _ in range(12):
            self.stars.append({
                "pos": list(pos),
                "vel": [random.uniform(-7, 7), random.uniform(-7, 7)],
                "life": 255
            })

    def process_input(self, events):
        if self.game_over: return # Oyun bittiyse girdi alma

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                # En üstteki meyveyi tutmak için listeyi tersten kontrol et
                for fruit in reversed(self.fruits):
                    if fruit["rect"].collidepoint(event.pos):
                        self.dragging = fruit
                        break
            
            if event.type == pygame.MOUSEBUTTONUP:
                if self.dragging:
                    if self.dragging["rect"].colliderect(self.basket_rect):
                        if self.dragging["type"] == "apple":
                            self.collected_count += 1
                            self.create_stars(self.dragging["rect"].center)
                            self.fruits.remove(self.dragging)
                        else:
                            # Yanlış meyveyi yukarı fırlat
                            self.dragging["rect"].y -= 200
                    self.dragging = None

    def update(self):
        if self.game_over:
            # Kazandıktan sonra 2 saniye (120 frame) bekle ve menüye dön
            self.timer_after_win += 1
            if self.timer_after_win > 120:
                from scenes.menu_scene import MenuScene
                self.switch_to_scene(MenuScene())
            return

        if self.dragging:
            self.dragging["rect"].center = pygame.mouse.get_pos()
        
        # Yıldızları güncelle
        for star in self.stars[:]:
            star["pos"][0] += star["vel"][0]
            star["pos"][1] += star["vel"][1]
            star["life"] -= 5
            if star["life"] <= 0:
                self.stars.remove(star)

        # Kazanma kontrolü
        if self.collected_count >= self.target_count:
            self.game_over = True

    def render(self, screen):
        # 1. Arka Plan
        screen.blit(self.bg, (0, 0))
        
        # 2. Soru Metni (Ekranda görünmesi için rengi siyah-beyaz konturlu yapalım)
        instruction = "Haydi, 3 tane elmayı sepete koy!"
        text_surf = self.font.render(instruction, True, (0, 0, 0))
        screen.blit(text_surf, (640 - text_surf.get_width()//2, 30))

        # 3. Sepet ve Meyveler
        screen.blit(self.basket_img, self.basket_rect)
        for fruit in self.fruits:
            screen.blit(fruit["img"], fruit["rect"])
            
        # 4. Yıldızlar
        for star in self.stars:
            s = pygame.Surface((12, 12))
            s.set_alpha(star["life"])
            s.fill((255, 215, 0))
            screen.blit(s, star["pos"])

        # 5. Tebrik Ekranı (Oyun bittiyse)
        if self.game_over:
            overlay = pygame.Surface((1280, 720), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150)) # Ekranı hafif karart
            screen.blit(overlay, (0,0))
            
            win_text = self.big_font.render("AFERİN! ÇOK İYİSİN!", True, (255, 255, 255))
            screen.blit(win_text, (640 - win_text.get_width()//2, 300))