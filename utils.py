# utils.py (GÜNCELLENMİŞ)
import pygame
import textwrap

def render_text_with_wrap(font, text, color, max_width):
    """Yazıyı belirli bir genişliğe sığacak şekilde böler"""
    words = text.split(' ')
    lines = []
    current_line = []
    
    for word in words:
        test_line = ' '.join(current_line + [word])
        test_width, _ = font.size(test_line)
        
        if test_width <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
    
    if current_line:
        lines.append(' '.join(current_line))
    
    return lines

def draw_text_box(screen, font, text, color, bg_color, rect, padding=10, border_color=(100,100,100)):
    """Yazıyı kutu içinde çizer, otomatik sığdırır"""
    pygame.draw.rect(screen, bg_color, rect, border_radius=15)
    pygame.draw.rect(screen, border_color, rect, 3, border_radius=15)
    
    max_text_width = rect.width - padding * 2
    lines = render_text_with_wrap(font, text, color, max_text_width)
    
    line_height = font.get_height() + 5
    total_height = len(lines) * line_height
    start_y = rect.centery - total_height // 2
    
    for i, line in enumerate(lines):
        text_surf = font.render(line, True, color)
        text_rect = text_surf.get_rect(center=(rect.centerx, start_y + i * line_height))
        screen.blit(text_surf, text_rect)

def create_gradient_surface(width, height, start_color, end_color, vertical=True):
    """Gradyan yüzey oluştur"""
    surface = pygame.Surface((width, height))
    
    if vertical:
        for y in range(height):
            ratio = y / height
            r = int(start_color[0] + (end_color[0] - start_color[0]) * ratio)
            g = int(start_color[1] + (end_color[1] - start_color[1]) * ratio)
            b = int(start_color[2] + (end_color[2] - start_color[2]) * ratio)
            pygame.draw.line(surface, (r, g, b), (0, y), (width, y))
    else:
        for x in range(width):
            ratio = x / width
            r = int(start_color[0] + (end_color[0] - start_color[0]) * ratio)
            g = int(start_color[1] + (end_color[1] - start_color[1]) * ratio)
            b = int(start_color[2] + (end_color[2] - start_color[2]) * ratio)
            pygame.draw.line(surface, (r, g, b), (x, 0), (x, height))
    
    return surface

def draw_button(screen, rect, text, font, text_color=(255, 255, 255), 
                bg_color=(100, 150, 255), hover_color=(80, 130, 235), 
                border_color=(60, 100, 200), border_width=3, radius=15):
    """Buton çizimi (hover efekti dahil)"""
    mouse_pos = pygame.mouse.get_pos()
    is_hover = rect.collidepoint(mouse_pos)
    
    # Buton rengi
    current_color = hover_color if is_hover else bg_color
    
    # Buton gövdesi
    pygame.draw.rect(screen, current_color, rect, border_radius=radius)
    
    # Buton kenarlığı
    pygame.draw.rect(screen, border_color, rect, border_width, border_radius=radius)
    
    # Buton metni
    text_surf = font.render(text, True, text_color)
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)
    
    return is_hover

def load_font(size=36, bold=False, italic=False):
    """Font yükleme yardımcı fonksiyonu"""
    try:
        # Öncelikle Comic Sans MS dene (çocuklar için uygun)
        font = pygame.font.SysFont("Comic Sans MS", size, bold, italic)
        return font
    except:
        try:
            # Sonra Arial dene
            font = pygame.font.SysFont("Arial", size, bold, italic)
            return font
        except:
            # Varsayılan font
            font = pygame.font.Font(None, size)
            return font