import pygame
import sys
import sys
import os
# Sahneler klasöründen bir üst dizine (ana dizine) çıkış yolunu ekler
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sound_manager import sound_manager 


class LevelSelectScene:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.width, self.height = self.screen.get_size()

        self.font_title = pygame.font.SysFont("arial", 48, bold=True)
        self.font_level = pygame.font.SysFont("arial", 16, bold=True)

        # Renkler
        self.bg_color = (240, 248, 255)      # açık mavi
        self.box_color = (100, 180, 255)     # açık bölüm
        self.locked_color = (180, 180, 180)  # kilitli bölüm
        self.text_color = (255, 255, 255)
        self.title_color = (40, 40, 80)

        self.unlocked_levels = 1  # sadece 1. bölüm açık
        self.level_boxes = []

        self.create_level_boxes()

    def create_level_boxes(self):
        cols = 5
        rows = 2
        box_w = 140
        box_h = 100
        gap = 30

        start_x = (self.width - (cols * box_w + (cols - 1) * gap)) // 2
        start_y = 180

        level = 1
        for row in range(rows):
            for col in range(cols):
                rect = pygame.Rect(
                    start_x + col * (box_w + gap),
                    start_y + row * (box_h + gap),
                    box_w,
                    box_h
                )
                self.level_boxes.append((level, rect))
                level += 1

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                for level, rect in self.level_boxes:
                    if rect.collidepoint(mouse_pos):
                        if level <= self.unlocked_levels:
                            print(f"{level}. bölüm seçildi")
                            # ileride buraya bölüm sahnesi bağlanacak

    def update(self):
        pass

    def draw(self):
        self.screen.fill(self.bg_color)

        # Başlık
        title = self.font_title.render("Bölüm Seç", True, self.title_color)
        self.screen.blit(
            title,
            title.get_rect(center=(self.width // 2, 80))
        )

        # Bölümler
        for level, rect in self.level_boxes:
            if level <= self.unlocked_levels:
                color = self.box_color
            else:
                color = self.locked_color

            pygame.draw.rect(self.screen, color, rect, border_radius=20)

            text = self.font_level.render(f"{level}. Bölüm", True, self.text_color)
            self.screen.blit(text, text.get_rect(center=rect.center))

            if level > self.unlocked_levels:
                self.draw_lock(rect.centerx, rect.centery + 22)

    def draw_lock(self, x, y):
        # Kilit gövdesi
        pygame.draw.rect(
            self.screen,
            (90, 90, 90),
            (x - 14, y, 28, 22),
            border_radius=6
        )

        # Kilit üstü
        pygame.draw.arc(
            self.screen,
            (90, 90, 90),
            (x - 18, y - 18, 36, 28),
            3.14,
            0,
            3
        )