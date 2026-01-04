# animation_manager.py (TAMAMLANMIŞ HALİ)
import pygame
import random
import math

class AnimationManager:
    def __init__(self):
        self.particles = []
        self.floating_texts = []
        self.transitions = []
    
    # ===== PARÇACIK SİSTEMİ =====
    def create_particle_explosion(self, position, color=(255, 255, 255), count=20, speed_range=(2, 6), size_range=(3, 8)):
        """Patlama efekti için parçacıklar oluştur"""
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(speed_range[0], speed_range[1])
            size = random.randint(size_range[0], size_range[1])
            
            self.particles.append({
                "type": "explosion",
                "pos": [position[0], position[1]],
                "vel": [math.cos(angle) * speed, math.sin(angle) * speed],
                "size": size,
                "color": color,
                "life": random.randint(40, 80),
                "max_life": 80,
                "gravity": 0.1,
                "fade": True
            })
    
    def create_particle_trail(self, position, color=(255, 255, 255), count=3, speed_factor=0.5):
        """İz efekti için parçacıklar oluştur"""
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(0.5, 1.5) * speed_factor
            
            self.particles.append({
                "type": "trail",
                "pos": [position[0] + random.randint(-5, 5), position[1] + random.randint(-5, 5)],
                "vel": [math.cos(angle) * speed, math.sin(angle) * speed],
                "size": random.randint(2, 4),
                "color": color,
                "life": random.randint(20, 40),
                "max_life": 40,
                "gravity": 0.05,
                "fade": True
            })
    
    def create_particle_sparkle(self, position, color=(255, 255, 0), count=8):
        """Parlama efekti için parçacıklar oluştur"""
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(0.3, 0.8)
            
            self.particles.append({
                "type": "sparkle",
                "pos": [position[0], position[1]],
                "vel": [math.cos(angle) * speed, math.sin(angle) * speed],
                "size": random.randint(4, 7),
                "color": color,
                "life": random.randint(30, 60),
                "max_life": 60,
                "gravity": 0,
                "fade": True
            })
    
    def create_particle_rain(self, position, width=200, color=(100, 150, 255), count=15):
        """Yağmur efekti için parçacıklar oluştur"""
        for _ in range(count):
            x_offset = random.randint(-width//2, width//2)
            
            self.particles.append({
                "type": "rain",
                "pos": [position[0] + x_offset, position[1] - 100],
                "vel": [random.uniform(-0.5, 0.5), random.uniform(3, 6)],
                "size": random.randint(8, 15),
                "color": color,
                "life": 100,
                "max_life": 100,
                "gravity": 0.2,
                "fade": False
            })
    
    # ===== YÜZEN METİN ANİMASYONU =====
    def create_floating_text(self, text, position, color=(255, 255, 255), font_size=30, duration=60):
        """Yüzen metin efekti oluştur"""
        font = pygame.font.SysFont("Arial", font_size, bold=True)
        
        self.floating_texts.append({
            "text": text,
            "pos": [position[0], position[1]],
            "color": color,
            "font": font,
            "life": 0,
            "max_life": duration,
            "velocity": [random.uniform(-0.5, 0.5), -1.5],  # Hafif yukarı hareket
            "alpha": 255
        })
    
    # ===== GEÇİŞ ANİMASYONLARI =====
    def create_fade_transition(self, start_alpha=0, end_alpha=255, duration=30, color=(0, 0, 0)):
        """Ekran kararma/açılma geçişi"""
        self.transitions.append({
            "type": "fade",
            "alpha": start_alpha,
            "start_alpha": start_alpha,
            "end_alpha": end_alpha,
            "duration": duration,
            "current_frame": 0,
            "color": color,
            "active": True
        })
    
    def create_slide_transition(self, direction="right", duration=30):
        """Kaydırma geçişi"""
        self.transitions.append({
            "type": "slide",
            "direction": direction,
            "duration": duration,
            "current_frame": 0,
            "offset": 1280 if direction in ["right", "left"] else 720,
            "active": True
        })
    
    # ===== GÜNCELLEME FONKSİYONLARI =====
    def update_particles(self):
        """Parçacıkları güncelle"""
        for particle in self.particles[:]:
            # Hareket
            particle["pos"][0] += particle["vel"][0]
            particle["pos"][1] += particle["vel"][1]
            
            # Yerçekimi
            particle["vel"][1] += particle["gravity"]
            
            # Ömür azaltma
            particle["life"] -= 1
            
            # Parlaklık azaltma (fade varsa)
            if particle["fade"]:
                # Renk fade işlemi
                if len(particle["color"]) == 4:
                    r, g, b, a = particle["color"]
                    alpha = int((particle["life"] / particle["max_life"]) * a)
                    particle["color"] = (r, g, b, max(0, alpha))
                else:
                    r, g, b = particle["color"]
                    alpha = int((particle["life"] / particle["max_life"]) * 255)
                    particle["color"] = (r, g, b, max(0, alpha))
            
            # Ölü parçacıkları kaldır
            if particle["life"] <= 0:
                self.particles.remove(particle)
    
    def update_floating_texts(self):
        """Yüzen metinleri güncelle"""
        for text in self.floating_texts[:]:
            # Hareket
            text["pos"][0] += text["velocity"][0]
            text["pos"][1] += text["velocity"][1]
            
            # Ömür ve saydamlık
            text["life"] += 1
            text["alpha"] = 255 - (text["life"] / text["max_life"] * 255)
            
            # Ölü metinleri kaldır
            if text["life"] >= text["max_life"]:
                self.floating_texts.remove(text)
    
    def update_transitions(self):
        """Geçiş animasyonlarını güncelle"""
        for transition in self.transitions[:]:
            if transition["active"]:
                transition["current_frame"] += 1
                
                if transition["type"] == "fade":
                    # Fade geçişi
                    progress = transition["current_frame"] / transition["duration"]
                    transition["alpha"] = transition["start_alpha"] + (
                        (transition["end_alpha"] - transition["start_alpha"]) * progress
                    )
                    
                    if transition["current_frame"] >= transition["duration"]:
                        transition["active"] = False
                        if transition["end_alpha"] == 0:
                            self.transitions.remove(transition)
                
                elif transition["type"] == "slide":
                    # Slide geçişi
                    progress = transition["current_frame"] / transition["duration"]
                    transition["offset"] = int((1 - progress) * (1280 if transition["direction"] in ["right", "left"] else 720))
                    
                    if transition["current_frame"] >= transition["duration"]:
                        transition["active"] = False
                        self.transitions.remove(transition)
    
    def update(self):
        """Tüm animasyonları güncelle"""
        self.update_particles()
        self.update_floating_texts()
        self.update_transitions()
    
    # ===== ÇİZİM FONKSİYONLARI =====
    def draw_particles(self, screen):
        """Parçacıkları çiz"""
        for particle in self.particles:
            if particle["life"] > 0:
                # Parçacık rengi ve saydamlığı
                color = particle["color"]
                alpha = min(255, int((particle["life"] / particle["max_life"]) * 255))
                
                # Parçacık tipine göre çizim
                if particle["type"] in ["explosion", "trail", "rain"]:
                    # Daire şeklinde parçacıklar
                    surface = pygame.Surface((particle["size"] * 2, particle["size"] * 2), pygame.SRCALPHA)
                    pygame.draw.circle(surface, (*color[:3], alpha), 
                                     (particle["size"], particle["size"]), 
                                     particle["size"])
                    screen.blit(surface, 
                              (particle["pos"][0] - particle["size"], 
                               particle["pos"][1] - particle["size"]))
                
                elif particle["type"] == "sparkle":
                    # Yıldız şeklinde parçacıklar
                    points = []
                    size = particle["size"]
                    for i in range(5):
                        angle = math.pi * 2 * i / 5 - math.pi / 2
                        outer_x = particle["pos"][0] + math.cos(angle) * size
                        outer_y = particle["pos"][1] + math.sin(angle) * size
                        inner_x = particle["pos"][0] + math.cos(angle + math.pi / 5) * (size / 2)
                        inner_y = particle["pos"][1] + math.sin(angle + math.pi / 5) * (size / 2)
                        points.append((outer_x, outer_y))
                        points.append((inner_x, inner_y))
                    
                    if len(points) > 2:
                        pygame.draw.polygon(screen, (*color[:3], alpha), points)
    
    def draw_floating_texts(self, screen):
        """Yüzen metinleri çiz"""
        for text in self.floating_texts:
            if text["alpha"] > 0:
                # Metin yüzeyi oluştur
                text_surface = text["font"].render(text["text"], True, text["color"])
                text_surface.set_alpha(int(text["alpha"]))
                
                # Gölge efekti
                shadow_surface = text["font"].render(text["text"], True, (0, 0, 0))
                shadow_surface.set_alpha(int(text["alpha"] * 0.5))
                
                # Çiz
                screen.blit(shadow_surface, (text["pos"][0] + 2, text["pos"][1] + 2))
                screen.blit(text_surface, text["pos"])
    
    def draw_transitions(self, screen):
        """Geçiş animasyonlarını çiz"""
        for transition in self.transitions:
            if transition["active"]:
                if transition["type"] == "fade":
                    # Fade geçişi
                    overlay = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
                    overlay.fill((*transition["color"][:3], int(transition["alpha"])))
                    screen.blit(overlay, (0, 0))
                
                elif transition["type"] == "slide":
                    # Slide geçişi
                    overlay = pygame.Surface((screen.get_width(), screen.get_height()))
                    overlay.fill((0, 0, 0))
                    
                    if transition["direction"] == "right":
                        screen.blit(overlay, (screen.get_width() - transition["offset"], 0))
                    elif transition["direction"] == "left":
                        screen.blit(overlay, (-screen.get_width() + transition["offset"], 0))
                    elif transition["direction"] == "down":
                        screen.blit(overlay, (0, screen.get_height() - transition["offset"]))
                    elif transition["direction"] == "up":
                        screen.blit(overlay, (0, -screen.get_height() + transition["offset"]))
    
    def draw(self, screen):
        """Tüm animasyonları çiz"""
        self.draw_particles(screen)
        self.draw_floating_texts(screen)
        self.draw_transitions(screen)
    
    # ===== YARDIMCI FONKSİYONLAR =====
    def clear_all(self):
        """Tüm animasyonları temizle"""
        self.particles.clear()
        self.floating_texts.clear()
        self.transitions.clear()
    
    def is_transition_active(self):
        """Aktif geçiş animasyonu var mı kontrol et"""
        for transition in self.transitions:
            if transition["active"]:
                return True
        return False


# Global animasyon yöneticisi örneği
animation_manager = AnimationManager()