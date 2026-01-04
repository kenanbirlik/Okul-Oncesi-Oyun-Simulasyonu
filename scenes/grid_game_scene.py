# scenes/grid_game_scene.py
import pygame
import random
import os
from gtts import gTTS
from scenes.base_scene import BaseScene
from sound_manager import sound_manager
import settings

class GridGameScene(BaseScene):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.SysFont("Comic Sans MS", 30, bold=True)
        self.big_font = pygame.font.SysFont("Comic Sans MS", 50, bold=True)
        
        # Bölüm başladığında genel talimatı çal
        sound_manager.play('level10', force=True)
        
        self.current_stage = 1
        self.total_stages = 3
        self.move_count = 0
        self.game_over = False
        self.timer_after_win = 0
        self.sound_played = False
        self.is_correct = False
        
        self.setup_stage(self.current_stage)

    def setup_stage(self, stage):
        # Labirent boyutları: 4x4, 5x5, 6x6
        self.grid_size = 4 + stage 
        self.cell_size = 400 // self.grid_size
        self.offset_x = (1280 - 400) // 2
        self.offset_y = (720 - 400) // 2
        
        self.player_pos = [0, 0]
        self.target_pos = [self.grid_size - 1, self.grid_size - 1]
        self.move_count = 0
        self.is_correct = False
        self.sound_played = False
        self.timer_after_win = 0
        
        # ENGEL SİSTEMİ: 1. Aşama -> 1 engel, 2. Aşama -> 2 engel, 3. Aşama -> 3 engel
        self.walls = []
        num_walls = stage # İstediğin sabit sayı
        
        attempts = 0
        while len(self.walls) < num_walls and attempts < 100:
            attempts += 1
            w = [random.randint(0, self.grid_size-1), random.randint(0, self.grid_size-1)]
            
            # GÜVENLİK KURALLARI:
            # - Başlangıç (0,0) ve Bitiş noktası olamaz.
            # - Bitişin hemen yanındaki kareler olmasın ki kapı kapanmasın.
            if w == self.player_pos or w == self.target_pos:
                continue
            
            # Bitiş noktasının dibine engel koyma (Yolun kapanmaması için en kritik yer)
            if abs(w[0] - self.target_pos[0]) + abs(w[1] - self.target_pos[1]) <= 1:
                continue

            if w not in self.walls:
                self.walls.append(w)

    def speak_score(self, count):
        """Hamle sayısını yapay zeka sesiyle okur"""
        try:
            text = f"Harika! {count} hamlede hedefe ulaştın."
            tts = gTTS(text=text, lang='tr')
            filename = "assets/sounds/temp_move.wav"
            tts.save(filename)
            
            # Dosyayı yükle ve çal
            move_sound = pygame.mixer.Sound(filename)
            move_sound.play()
        except:
            print("Seslendirme oluşturulamadı, interneti kontrol edin.")

    def process_input(self, events):
        if self.is_correct or self.game_over: return
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                old_pos = list(self.player_pos)
                if event.key == pygame.K_UP and self.player_pos[1] > 0: self.player_pos[1] -= 1
                elif event.key == pygame.K_DOWN and self.player_pos[1] < self.grid_size - 1: self.player_pos[1] += 1
                elif event.key == pygame.K_LEFT and self.player_pos[0] > 0: self.player_pos[0] -= 1
                elif event.key == pygame.K_RIGHT and self.player_pos[0] < self.grid_size - 1: self.player_pos[0] += 1
                
                if old_pos != self.player_pos:
                    if self.player_pos in self.walls:
                        self.player_pos = old_pos # Duvara çarpınca hareketi iptal et
                    else:
                        self.move_count += 1 # Sadece başarılı harekette artır
                
                if self.player_pos == self.target_pos:
                    self.is_correct = True
                    if not self.sound_played:
                        self.speak_score(self.move_count)
                        self.sound_played = True

    def update(self):
        if self.is_correct:
            self.timer_after_win += 1
            # Sesin bitmesi ve çocuğun sonucu görmesi için yeterli bekleme
            if self.timer_after_win > 210: 
                if self.current_stage < self.total_stages:
                    self.current_stage += 1
                    self.setup_stage(self.current_stage)
                else:
                    self.game_over = True
                    
        if self.game_over:
            self.timer_after_win += 1
            if self.timer_after_win > 180:
                settings.complete_level(10)
                from scenes.menu_scene import MenuScene
                self.switch_to_scene(MenuScene())

    def render(self, screen):
        screen.fill((240, 245, 255)) # Çok açık mavi arka plan
        
        # Kareleri Çiz
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                rect = pygame.Rect(self.offset_x + c*self.cell_size, self.offset_y + r*self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(screen, (255,255,255), rect)
                pygame.draw.rect(screen, (220,220,220), rect, 1)
        
        # Engelleri Çiz (Koyu Gri)
        for w in self.walls:
            w_rect = pygame.Rect(self.offset_x + w[0]*self.cell_size, self.offset_y + w[1]*self.cell_size, self.cell_size, self.cell_size)
            pygame.draw.rect(screen, (80, 80, 80), w_rect.inflate(-4, -4), border_radius=5)
            
        # Oyuncu (Mavi Dairemsi Kare)
        p_rect = pygame.Rect(self.offset_x + self.player_pos[0]*self.cell_size, self.offset_y + self.player_pos[1]*self.cell_size, self.cell_size, self.cell_size)
        pygame.draw.rect(screen, (0, 120, 255), p_rect.inflate(-15, -15), border_radius=12)
        
        # Hedef (Kırmızı Parlak Kare)
        t_rect = pygame.Rect(self.offset_x + self.target_pos[0]*self.cell_size, self.offset_y + self.target_pos[1]*self.cell_size, self.cell_size, self.cell_size)
        pygame.draw.rect(screen, (255, 60, 60), t_rect.inflate(-15, -15), border_radius=12)

        # Hamle Sayacı
        m_txt = self.font.render(f"Hamle: {self.move_count}", True, (70, 70, 70))
        screen.blit(m_txt, (50, 50))

        if self.is_correct:
            overlay = pygame.Surface((1280, 720), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 130))
            screen.blit(overlay, (0,0))
            
            panel = pygame.Rect(415, 260, 450, 200)
            pygame.draw.rect(screen, (255,255,255), panel, border_radius=25)
            
            s1 = self.big_font.render("BİTTİ!", True, (0, 180, 0))
            s2 = self.font.render(f"{self.move_count} Hamle Yaptın", True, (50, 50, 50))
            
            screen.blit(s1, (640 - s1.get_width()//2, 290))
            screen.blit(s2, (640 - s2.get_width()//2, 370))