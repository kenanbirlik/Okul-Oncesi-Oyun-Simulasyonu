# scenes/menu_scene.py
import pygame
import settings
from scenes.base_scene import BaseScene
from sound_manager import sound_manager

# Sahne importları
from scenes.collect_scene import CollectScene
from scenes.color_scene import ColorScene
from scenes.vowel_scene import VowelScene
from scenes.shape_scene import ShapeScene
from scenes.size_scene import SizeScene
from scenes.fish_scene import FishScene
from scenes.hece_scene import HeceScene
from scenes.memory_scene import MemoryScene
from scenes.puzzle_scene import PuzzleScene
from scenes.grid_game_scene import GridGameScene

class MenuScene(BaseScene):
    def __init__(self):
        super().__init__()
        # --- FONT AYARLARI ---
        self.font = pygame.font.SysFont("Comic Sans MS", 24, bold=True)
        self.title_font = pygame.font.SysFont("Comic Sans MS", 48, bold=True)
        self.level_font = pygame.font.SysFont("Comic Sans MS", 34, bold=True)
        self.theme_font = pygame.font.SysFont("Comic Sans MS", 18, bold=True)
        self.level_name_font = pygame.font.SysFont("Comic Sans MS", 20, bold=True)
        
        # --- ARKA PLAN VE DEKORASYON ---
        self.bg_image = None
        self.load_background(settings.CURRENT_THEME_IMG)
        self.load_decorations()
        
        # Başlık kutusu ayarları
        self.title_box_color = (255, 255, 255, 230)
        self.title_box_width = 800
        self.title_box_height = 100
        
        # Butonlar
        self.level_buttons = []
        self.theme_buttons = []
        self.setup_level_buttons()
        self.setup_theme_buttons()
        
        # Animasyon ve ESC ipucu
        self.confetti_angle = 0
        self.show_esc_hint = True
        self.esc_hint_timer = 0

    def load_decorations(self):
        """Dekorasyonları ve süsleri yükle"""
        try:
            self.confetti_img = pygame.transform.scale(pygame.image.load("assets/images/konfeti.png").convert_alpha(), (70, 70))
            self.flower_img = pygame.transform.scale(pygame.image.load("assets/images/cicek.png").convert_alpha(), (40, 40))
        except:
            self.confetti_img = None
            self.flower_img = None

    def load_background(self, filename):
        """Seçili temaya göre arkaplanı temizce yükler"""
        try:
            self.bg_image = pygame.transform.scale(pygame.image.load(f"assets/images/{filename}"), (1280, 720))
        except:
            # Görsel bulunamazsa güvenli bir renk çiz
            self.bg_image = pygame.Surface((1280, 720))
            self.bg_image.fill((100, 150, 255))

    def setup_level_buttons(self):
        """10 Bölüm için buton koordinatları ve renkleri"""
        level_names = {
            1: "MEYVE TOPLA", 2: "RENK EŞLEŞTİR", 3: "SESLİ HARF", 4: "ŞEKİL BUL", 5: "BÜYÜK-KÜÇÜK",
            6: "BALIK SAY", 7: "NESNE BUL", 8: "HAFIZA OYUNU", 9: "PUZZLE", 10: "HEDEF BUL"
        }
        level_colors = [
            (255, 100, 100), (100, 200, 100), (100, 150, 255), (255, 200, 50), (255, 150, 200),
            (100, 220, 220), (200, 100, 255), (255, 150, 100), (150, 255, 150), (255, 100, 255)
        ]
        
        button_w, button_h = 200, 120
        h_gap, v_gap = 30, 20
        start_x = (1280 - (5 * button_w + 4 * h_gap)) // 2
        
        for i in range(1, 11):
            row, col = (i - 1) // 5, (i - 1) % 5
            x = start_x + col * (button_w + h_gap)
            y = 150 + row * (button_h + v_gap)
            
            self.level_buttons.append({
                "level": i, "rect": pygame.Rect(x, y, button_w, button_h),
                "name": level_names.get(i), "color": level_colors[(i-1) % 10], "hover": False
            })

    def setup_theme_buttons(self):
        """Tema seçim butonları"""
        themes = [
            {"name": "MAVİ", "file": "mavi_bg.png", "color": (100, 150, 255)},
            {"name": "TURUNCU", "file": "turuncu_bg.png", "color": (255, 150, 50)},
            {"name": "PEMBE", "file": "pembe_bg.png", "color": (255, 150, 200)},
            {"name": "BEYAZ", "file": "beyaz_bg.png", "color": (220, 220, 220)}
        ]
        total_w = len(themes) * 160 - 20
        start_x = (1280 - total_w) // 2
        
        for i, theme in enumerate(themes):
            self.theme_buttons.append({
                "rect": pygame.Rect(start_x + i * 160, 500, 140, 60),
                "theme": theme, "name": theme["name"], "color": theme["color"], "hover": False
            })

    def create_beveled_box(self, width, height, color, border_radius=15):
        """Gölgeli ve profesyonel kutu çizimi"""
        box = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(box, color, (0, 0, width, height), border_radius=border_radius)
        # Işık ve gölge efektleri
        pygame.draw.rect(box, (255, 255, 255, 100), (0, 0, width, 5), border_radius=border_radius)
        pygame.draw.rect(box, (0, 0, 0, 60), (0, height - 5, width, 5), border_radius=border_radius)
        pygame.draw.rect(box, (100, 100, 100, 180), (0, 0, width, height), 3, border_radius=border_radius)
        return box

    def process_input(self, events):
        super().process_input(events)
        m_pos = pygame.mouse.get_pos()
        
        # Hover durumlarını güncelle
        for btn in self.level_buttons: btn["hover"] = btn["rect"].collidepoint(m_pos)
        for btn in self.theme_buttons: btn["hover"] = btn["rect"].collidepoint(m_pos)
            
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Tema butonuna tıklanırsa
                for btn in self.theme_buttons:
                    if btn["rect"].collidepoint(event.pos):
                        settings.CURRENT_THEME_IMG = btn["theme"]["file"]
                        self.load_background(settings.CURRENT_THEME_IMG)
                        return
                
                # Bölüm butonuna tıklanırsa (Kilitsiz - her zaman açılır)
                for btn in self.level_buttons:
                    if btn["rect"].collidepoint(event.pos):
                        self.load_level(btn["level"])

    def load_level(self, num):
        scenes = {
            1: CollectScene, 2: ColorScene, 3: VowelScene, 4: ShapeScene, 5: SizeScene,
            6: FishScene, 7: HeceScene, 8: MemoryScene, 9: PuzzleScene, 10: GridGameScene
        }
        if num in scenes:
            self.switch_to_scene(scenes[num]())

    def update(self):
        self.confetti_angle = (self.confetti_angle + 2) % 360
        self.esc_hint_timer += 1
        if self.esc_hint_timer > 300: self.show_esc_hint = False

    def render(self, screen):
        screen.blit(self.bg_image, (0, 0))
        is_white = settings.CURRENT_THEME_IMG == "beyaz_bg.png"
        
        # BAŞLIK
        tb = self.create_beveled_box(self.title_box_width, self.title_box_height, self.title_box_color, 20)
        screen.blit(tb, (640 - 400, 30))
        title_color = (40, 40, 100) if not is_white else (40, 40, 40)
        t_surf = self.title_font.render("MİNİK KAŞİF OYUNU", True, title_color)
        screen.blit(t_surf, (640 - t_surf.get_width() // 2, 65))
        
        # Konfeti Animasyonu
        if self.confetti_img:
            rot = pygame.transform.rotate(self.confetti_img, self.confetti_angle)
            screen.blit(rot, rot.get_rect(center=(280, 80)))
            screen.blit(rot, rot.get_rect(center=(1000, 80)))

        # BÖLÜM BUTONLARI (TİK İŞARETLERİ TAMAMEN KALDIRILDI)
        for btn in self.level_buttons:
            color = btn["color"]
            if btn["hover"]:
                color = tuple(min(c + 40, 255) for c in color)
            
            draw_rect = btn["rect"].inflate(10, 10) if btn["hover"] else btn["rect"]
            box = self.create_beveled_box(draw_rect.width, draw_rect.height, color, 12)
            screen.blit(box, draw_rect)
            
            num_s = self.level_font.render(str(btn["level"]), True, (255, 255, 255))
            name_s = self.level_name_font.render(btn["name"], True, (255, 255, 255))
            screen.blit(num_s, (draw_rect.centerx - num_s.get_width() // 2, draw_rect.y + 15))
            screen.blit(name_s, (draw_rect.centerx - name_s.get_width() // 2, draw_rect.y + 70))

        # TEMA BUTONLARI
        theme_title = self.theme_font.render("TEMALAR:", True, (60, 60, 60))
        screen.blit(theme_title, (640 - theme_title.get_width() // 2, 470))
        for btn in self.theme_buttons:
            box = self.create_beveled_box(btn["rect"].width, btn["rect"].height, btn["color"], 8)
            screen.blit(box, btn["rect"])
            if settings.CURRENT_THEME_IMG == btn["theme"]["file"]:
                pygame.draw.rect(screen, (0, 100, 200), btn["rect"], 3, border_radius=8)
            t_surf = self.theme_font.render(btn["name"], True, (40, 40, 40))
            screen.blit(t_surf, (btn["rect"].centerx - t_surf.get_width() // 2, btn["rect"].centery - t_surf.get_height() // 2))

        # ALT BİLGİ VE ÇİÇEKLER
        info_box = self.create_beveled_box(1100, 40, (255, 255, 255, 180), 8)
        screen.blit(info_box, (640 - 550, 590))
        info_txt = pygame.font.SysFont("Arial", 16).render("İstediğiniz bölüme tıklayın • ESC ile menüye dönebilirsiniz", True, (80, 80, 80))
        screen.blit(info_txt, (640 - info_txt.get_width() // 2, 600))
        
        if self.flower_img:
            screen.blit(self.flower_img, (640 - 550 - 20, 590))
            screen.blit(self.flower_img, (640 + 550 - 20, 590))