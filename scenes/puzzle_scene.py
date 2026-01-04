# scenes/puzzle_scene.py
import pygame
import random
import sys
import os

# BaseScene ve ayarları içe aktar
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from scenes.base_scene import BaseScene
import settings
from sound_manager import sound_manager

class PuzzleScene(BaseScene):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.SysFont("Comic Sans MS", 40, bold=True)
        self.big_font = pygame.font.SysFont("Comic Sans MS", 70, bold=True)
        
        self.current_stage = 1
        self.max_stages = 2
        self.game_over = False
        self.timer_after_win = 0
        self.dragging = None
        self.is_stage_cleared = False
        
        # İlk aşamayı başlat
        self.load_puzzle_stage(self.current_stage)
        sound_manager.play('level9', force=True)

    def load_puzzle_stage(self, stage):
        """Aşamaya göre parçaları böler (1. Aşama: 4 parça, 2. Aşama: 6 parça)"""
        self.pieces = [] 
        self.dragging = None
        self.is_stage_cleared = False
        self.timer_after_win = 0
        
        # Dinamik Bölünme Mantığı
        if stage == 1:
            self.rows, self.cols = 2, 2  # 4 Parça
        else:
            self.rows, self.cols = 2, 3  # 6 Parça (Senin istediğin)

        # Resim yükleme
        img_name = "foto.png" if stage == 1 else "foto2.png"
        img_path = os.path.join("assets", "images", img_name)
        
        try:
            if os.path.exists(img_path):
                full_img = pygame.image.load(img_path).convert_alpha()
            else:
                fallback_path = os.path.join("assets", "images", "foto.png")
                full_img = pygame.image.load(fallback_path).convert_alpha()
            full_img = pygame.transform.scale(full_img, (600, 450))
        except:
            full_img = pygame.Surface((600, 450))
            full_img.fill((150, 150, 150))
            
        # Parça boyutlarını hesapla
        pw, ph = 600 // self.cols, 450 // self.rows
        self.puzzle_x, self.puzzle_y = 150, 135
        
        # Resim parçalarını kes ve oluştur
        for r in range(self.rows):
            for c in range(self.cols):
                rect = pygame.Rect(c * pw, r * ph, pw, ph)
                piece_surface = full_img.subsurface(rect).copy()
                
                # Parçaları sağ tarafa (karışık alana) diz
                # Üst üste binmemeleri için biraz dağıtıyoruz
                start_x = random.randint(800, 1050)
                start_y = random.randint(100, 500)
                
                self.pieces.append({
                    "img": piece_surface,
                    "target_pos": (self.puzzle_x + c * pw, self.puzzle_y + r * ph),
                    "current_rect": piece_surface.get_rect(topleft=(start_x, start_y)),
                    "is_locked": False
                })
        
        try:
            self.bg = pygame.transform.scale(pygame.image.load("assets/images/bolum9_bg.png"), (1280, 720))
        except:
            self.bg = pygame.Surface((1280, 720)); self.bg.fill((240, 248, 255))

    def process_input(self, events):
        super().process_input(events)
        if self.game_over or self.is_stage_cleared: return
        
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for p in reversed(self.pieces):
                    if not p["is_locked"] and p["current_rect"].collidepoint(event.pos):
                        self.dragging = p
                        self.pieces.remove(p)
                        self.pieces.append(p)
                        break
            
            if event.type == pygame.MOUSEBUTTONUP and self.dragging:
                tx, ty = self.dragging["target_pos"]
                # Mıknatıs etkisi (6 parça daha küçük olduğu için hassasiyeti koruduk)
                if abs(self.dragging["current_rect"].x - tx) < 50 and abs(self.dragging["current_rect"].y - ty) < 50:
                    self.dragging["current_rect"].topleft = (tx, ty)
                    self.dragging["is_locked"] = True
                self.dragging = None

    def update(self):
        if self.game_over:
            self.timer_after_win += 1
            if self.timer_after_win > 180:
                settings.complete_level(9)
                from scenes.menu_scene import MenuScene
                self.switch_to_scene(MenuScene())
            return
            
        if self.dragging:
            self.dragging["current_rect"].center = pygame.mouse.get_pos()
            
        if not self.is_stage_cleared and all(p["is_locked"] for p in self.pieces):
            self.is_stage_cleared = True
            self.timer_after_win = 0
            if self.current_stage < self.max_stages:
                sound_manager.play('bravo_short', force=True)
            else:
                sound_manager.play('bravo', force=True)

        if self.is_stage_cleared:
            self.timer_after_win += 1
            if self.timer_after_win > 150:
                if self.current_stage < self.max_stages:
                    self.current_stage += 1
                    self.load_puzzle_stage(self.current_stage)
                else:
                    self.game_over = True

    def render(self, screen):
        screen.blit(self.bg, (0, 0))
        
        # Hedef alan ve Dinamik Izgara (Grid) Çizimi
        # Çocuk parçaları nereye koyacağını net görsün diye çizgileri de güncelledik
        pygame.draw.rect(screen, (200, 200, 200), (self.puzzle_x, self.puzzle_y, 600, 450))
        pw, ph = 600 // self.cols, 450 // self.rows
        for c in range(self.cols + 1):
            pygame.draw.line(screen, (100, 100, 100), (self.puzzle_x + c * pw, self.puzzle_y), (self.puzzle_x + c * pw, self.puzzle_y + 450), 2)
        for r in range(self.rows + 1):
            pygame.draw.line(screen, (100, 100, 100), (self.puzzle_x, self.puzzle_y + r * ph), (self.puzzle_x + 600, self.puzzle_y + r * ph), 2)
        
        # Parçaları çiz
        for p in self.pieces:
            screen.blit(p["img"], p["current_rect"])
            if p["is_locked"]:
                pygame.draw.rect(screen, (0, 200, 0), p["current_rect"], 2)
            
        # Bilgi ve Aşama Göstergesi
        txt = self.font.render(f"Bulmaca - Aşama {self.current_stage} ({len(self.pieces)} Parça)", True, (50, 50, 50))
        screen.blit(txt, (50, 30))
        
        if self.is_stage_cleared:
            overlay = pygame.Surface((1280, 720), pygame.SRCALPHA); overlay.fill((0, 0, 0, 120))
            screen.blit(overlay, (0,0))
            msg = self.big_font.render("AŞAMA TAMAM!", True, (255, 255, 255))
            screen.blit(msg, (640 - msg.get_width()//2, 320))