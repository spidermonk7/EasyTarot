import os
import random
import pygame
from pygame.locals import *
import json
import math
import time

# Directory containing your card images
IMAGE_DIR = '/Users/cuishaoyang/Desktop/KaiTeam/Mod_fixer/MCPs/myTarot/images'

# Enhanced visual configuration
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 800
CARD_WIDTH, CARD_HEIGHT = 180, 300
SPACING = 80
FPS = 60

# Enhanced color scheme
COLORS = {
    'bg_dark': (15, 10, 30),
    'bg_mid': (30, 20, 50),
    'accent_gold': (255, 215, 0),
    'accent_purple': (138, 43, 226),
    'text_light': (240, 240, 240),
    'text_gold': (255, 215, 0),
    'shadow': (0, 0, 0, 100),
    'glow': (255, 255, 255, 50),
    'button_bg': (60, 40, 80),
    'button_hover': (80, 60, 120),
    'star': (255, 255, 200)
}

# Card name mapping (same as original)
NAME_MAP = {
    '01': 'The Magician', '02': 'The Popess', '03': 'The Empress', '04': 'The Emperor',
    '05': 'The Pope', '06': 'The Lover', '07': 'The Chariot', '08': 'Justice',
    '09': 'The Hermit', '10': 'The Wheel of Fortune', '11': 'Strength', '12': 'The Hanged Man',
    '13': 'Death', '14': 'Temperance', '15': 'The Devil', '16': 'The Tower',
    '17': 'The Star', '18': 'The Moon', '19': 'The Sun', '20': 'Judgement',
    '00': 'The Fool', '21': 'The World',
    'swki': 'King of Swords', 'swqu': 'Queen of Swords', 'swkn': 'Knight of Swords', 'swpa': 'Page of Swords',
    'sw01': 'Ace of Swords', 'sw02': 'Two of Swords', 'sw03': 'Three of Swords', 'sw04': 'Four of Swords',
    'sw05': 'Five of Swords', 'sw06': 'Six of Swords', 'sw07': 'Seven of Swords', 'sw08': 'Eight of Swords',
    'sw09': 'Nine of Swords', 'sw10': 'Ten of Swords',
    'peki': 'King of Coins', 'pequ': 'Queen of Coins', 'pekn': 'Knight of Coins', 'pepa': 'Page of Coins',
    'pe01': 'Ace of Coins', 'pe02': 'Two of Coins', 'pe03': 'Three of Coins', 'pe04': 'Four of Coins',
    'pe05': 'Five of Coins', 'pe06': 'Six of Coins', 'pe07': 'Seven of Coins', 'pe08': 'Eight of Coins',
    'pe09': 'Nine of Coins', 'pe10': 'Ten of Coins',
    'cuki': 'King of Cups', 'cuqu': 'Queen of Cups', 'cukn': 'Knight of Cups', 'cupa': 'Page of Cups',
    'cu01': 'Ace of Cups', 'cu02': 'Two of Cups', 'cu03': 'Three of Cups', 'cu04': 'Four of Cups',
    'cu05': 'Five of Cups', 'cu06': 'Six of Cups', 'cu07': 'Seven of Cups', 'cu08': 'Eight of Cups',
    'cu09': 'Nine of Cups', 'cu10': 'Ten of Cups',
    'waki': 'King of Clubs', 'waqu': 'Queen of Clubs', 'wakn': 'Knight of Clubs', 'wapa': 'Page of Clubs',
    'wa01': 'Ace of Clubs', 'wa02': 'Two of Clubs', 'wa03': 'Three of Clubs', 'wa04': 'Four of Clubs',
    'wa05': 'Five of Clubs', 'wa06': 'Six of Clubs', 'wa07': 'Seven of Clubs', 'wa08': 'Eight of Clubs',
    'wa09': 'Nine of Clubs', 'wa10': 'Ten of Clubs'
}

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel_x = random.uniform(-1, 1)
        self.vel_y = random.uniform(-2, -0.5)
        self.size = random.randint(1, 3)
        self.life = random.randint(60, 120)
        self.max_life = self.life
        
    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y
        self.life -= 1
        
    def draw(self, screen):
        if self.life > 0:
            alpha = int(255 * (self.life / self.max_life))
            color = (*COLORS['star'], alpha)
            star_surf = pygame.Surface((self.size*2, self.size*2), pygame.SRCALPHA)
            pygame.draw.circle(star_surf, color, (self.size, self.size), self.size)
            screen.blit(star_surf, (int(self.x), int(self.y)))

class EnhancedTarotGUI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('✨ Mystical Tarot Reading ✨')
        self.clock = pygame.time.Clock()
        
        # Load fonts
        try:
            self.title_font = pygame.font.SysFont('Cinzel', 48, bold=True)
            self.card_font = pygame.font.SysFont('Cinzel', 20, bold=True)
            self.button_font = pygame.font.SysFont('Cinzel', 24, bold=True)
            self.text_font = pygame.font.SysFont('Cinzel', 16)
        except:
            self.title_font = pygame.font.SysFont('serif', 42, bold=True)
            self.card_font = pygame.font.SysFont('serif', 18, bold=True)
            self.button_font = pygame.font.SysFont('serif', 20, bold=True)
            self.text_font = pygame.font.SysFont('serif', 14)
        
        self.particles = []
        self.animation_timer = 0
        
    def create_gradient_background(self):
        """Create a mystical gradient background"""
        bg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        for y in range(SCREEN_HEIGHT):
            ratio = y / SCREEN_HEIGHT
            r = int(COLORS['bg_dark'][0] + (COLORS['bg_mid'][0] - COLORS['bg_dark'][0]) * ratio)
            g = int(COLORS['bg_dark'][1] + (COLORS['bg_mid'][1] - COLORS['bg_dark'][1]) * ratio)
            b = int(COLORS['bg_dark'][2] + (COLORS['bg_mid'][2] - COLORS['bg_dark'][2]) * ratio)
            pygame.draw.line(bg, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        return bg
    
    def add_stars_to_background(self, surface):
        """Add twinkling stars to background"""
        for _ in range(50):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT // 2)
            brightness = random.randint(100, 255)
            size = random.randint(1, 2)
            star_color = (brightness, brightness, min(255, brightness + 50))
            pygame.draw.circle(surface, star_color, (x, y), size)
    
    def draw_glowing_text(self, text, font, color, x, y, glow_color=None):
        """Draw text with a subtle glow effect"""
        if glow_color is None:
            glow_color = COLORS['glow'][:3]
        
        # Draw glow effect
        for offset in [(2, 2), (-2, 2), (2, -2), (-2, -2), (0, 2), (2, 0), (0, -2), (-2, 0)]:
            glow_surf = font.render(text, True, glow_color)
            glow_surf.set_alpha(50)
            glow_rect = glow_surf.get_rect(center=(x + offset[0], y + offset[1]))
            self.screen.blit(glow_surf, glow_rect)
        
        # Draw main text
        text_surf = font.render(text, True, color)
        text_rect = text_surf.get_rect(center=(x, y))
        self.screen.blit(text_surf, text_rect)
        
        return text_rect
    
    def draw_card_with_shadow(self, card_img, x, y, hover=False):
        """Draw card with shadow and optional glow effect"""
        # Draw shadow
        shadow_offset = 8
        shadow_surf = pygame.Surface((CARD_WIDTH + 10, CARD_HEIGHT + 10), pygame.SRCALPHA)
        shadow_surf.fill((0, 0, 0, 80))
        self.screen.blit(shadow_surf, (x + shadow_offset - 5, y + shadow_offset - 5))
        
        # Draw glow if hovering
        if hover:
            glow_surf = pygame.Surface((CARD_WIDTH + 20, CARD_HEIGHT + 20), pygame.SRCALPHA)
            pygame.draw.rect(glow_surf, (*COLORS['accent_gold'], 60), glow_surf.get_rect(), border_radius=10)
            self.screen.blit(glow_surf, (x - 10, y - 10))
        
        # Draw card with rounded corners effect
        card_rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
        pygame.draw.rect(self.screen, (255, 255, 255), card_rect, border_radius=10)
        pygame.draw.rect(self.screen, COLORS['accent_gold'], card_rect, 3, border_radius=10)
        
        # Blit the actual card image
        self.screen.blit(card_img, (x, y))
    
    def draw_button(self, text, x, y, width, height, is_hovered=False):
        """Draw an elegant button with hover effects"""
        color = COLORS['button_hover'] if is_hovered else COLORS['button_bg']
        border_color = COLORS['accent_gold'] if is_hovered else COLORS['accent_purple']
        
        # Draw button background with gradient effect
        button_rect = pygame.Rect(x - width//2, y - height//2, width, height)
        pygame.draw.rect(self.screen, color, button_rect, border_radius=20)
        pygame.draw.rect(self.screen, border_color, button_rect, 3, border_radius=20)
        
        # Add inner highlight
        if is_hovered:
            inner_rect = button_rect.inflate(-6, -6)
            pygame.draw.rect(self.screen, (*COLORS['accent_gold'], 30), inner_rect, border_radius=17)
        
        # Draw button text
        text_color = COLORS['accent_gold'] if is_hovered else COLORS['text_light']
        self.draw_glowing_text(text, self.button_font, text_color, x, y)
        
        return button_rect
    
    def load_card_image(self, filename, reversed=False):
        """Load and process card image"""
        path = os.path.join(IMAGE_DIR, filename)
        try:
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.smoothscale(img, (CARD_WIDTH, CARD_HEIGHT))
            return pygame.transform.rotate(img, 180) if reversed else img
        except:
            # Create a placeholder card if image doesn't exist
            placeholder = pygame.Surface((CARD_WIDTH, CARD_HEIGHT))
            placeholder.fill(COLORS['bg_mid'])
            pygame.draw.rect(placeholder, COLORS['accent_purple'], placeholder.get_rect(), 5)
            return placeholder
    
    def get_card_name(self, filename):
        """Get display name for card"""
        base = os.path.splitext(filename)[0]
        short = base[-2:] if base[-2:].isdigit() else base[-4:]
        return NAME_MAP.get(short, base.replace('_', ' ').title())
    
    def update_particles(self):
        """Update and manage particle system"""
        # Add new particles occasionally
        if random.randint(1, 10) == 1:
            x = random.randint(0, SCREEN_WIDTH)
            y = SCREEN_HEIGHT
            self.particles.append(Particle(x, y))
        
        # Update existing particles
        self.particles = [p for p in self.particles if p.life > 0]
        for particle in self.particles:
            particle.update()
            particle.draw(self.screen)
    
    def draw_cards_with_animation(self, picks, orientations, animation_progress):
        """Draw cards with smooth animation"""
        total_width = 3 * CARD_WIDTH + 2 * SPACING
        start_x = (SCREEN_WIDTH - total_width) // 2
        target_y = (SCREEN_HEIGHT - CARD_HEIGHT) // 2 - 50
        
        for i, (filename, orientation) in enumerate(zip(picks, orientations)):
            x = start_x + i * (CARD_WIDTH + SPACING)
            
            # Animated entry from different directions
            if animation_progress < 1.0:
                # Each card enters from a different direction with delay
                delay = i * 0.3
                card_progress = max(0, min(1, (animation_progress - delay) / 0.7))
                
                if i == 0:  # Left card from left
                    current_x = x - 300 + (300 * card_progress)
                elif i == 1:  # Middle card from top
                    current_y = target_y - 400 + (400 * card_progress)
                    current_x = x
                else:  # Right card from right
                    current_x = x + 300 - (300 * card_progress)
                
                if i != 1:
                    current_y = target_y
                    
                # Smooth easing
                ease_progress = card_progress * card_progress * (3 - 2 * card_progress)
                if i == 0:
                    current_x = x - 300 + (300 * ease_progress)
                elif i == 2:
                    current_x = x + 300 - (300 * ease_progress)
                else:
                    current_y = target_y - 400 + (400 * ease_progress)
            else:
                current_x, current_y = x, target_y
            
            # Load and draw card
            card_img = self.load_card_image(filename, orientation)
            self.draw_card_with_shadow(card_img, int(current_x), int(current_y))
            
            # Draw card info if animation is complete
            if animation_progress >= 1.0:
                name = self.get_card_name(filename)
                orient_text = 'Reversed' if orientation else 'Upright'
                
                # Card name
                self.draw_glowing_text(name, self.card_font, COLORS['text_gold'], 
                                     current_x + CARD_WIDTH//2, current_y + CARD_HEIGHT + 30)
                
                # Orientation
                orient_color = COLORS['accent_purple'] if orientation else COLORS['text_light']
                self.draw_glowing_text(orient_text, self.text_font, orient_color, 
                                     current_x + CARD_WIDTH//2, current_y + CARD_HEIGHT + 55)
    
    def show_welcome_screen(self):
        """Enhanced welcome screen"""
        fade_in = 0
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    return None
                if event.type == KEYDOWN and event.key == K_ESCAPE:
                    pygame.quit()
                    return None
                if event.type in (KEYDOWN, MOUSEBUTTONDOWN):
                    if event.type != KEYDOWN or event.key == K_SPACE:
                        return "draw"
            
            # Create background
            bg = self.create_gradient_background()
            self.add_stars_to_background(bg)
            self.screen.blit(bg, (0, 0))
            
            # Update particles
            self.update_particles()
            
            # Fade in effect
            fade_in = min(255, fade_in + 3)
            
            # Draw title with animation
            title_y = SCREEN_HEIGHT // 2 - 100 + math.sin(self.animation_timer * 0.02) * 5
            self.draw_glowing_text("✨ MYSTICAL TAROT READING ✨", self.title_font, 
                                 COLORS['accent_gold'], SCREEN_WIDTH // 2, int(title_y))
            
            # Instructions
            instructions = [
                "Press SPACE or Click to Draw Your Cards",
                "Let the Universe Guide Your Path",
                "Press ESC to Exit"
            ]
            
            for i, instruction in enumerate(instructions):
                y = SCREEN_HEIGHT // 2 + 50 + i * 40
                alpha_offset = math.sin(self.animation_timer * 0.03 + i * 0.5) * 20
                color = (min(255, COLORS['text_light'][0] + alpha_offset),
                        min(255, COLORS['text_light'][1] + alpha_offset),
                        min(255, COLORS['text_light'][2] + alpha_offset))
                self.draw_glowing_text(instruction, self.text_font, color, SCREEN_WIDTH // 2, y)
            
            self.animation_timer += 1
            pygame.display.flip()
            self.clock.tick(FPS)
    
    def draw_cards(self):
        """Enhanced card drawing with better animations"""
        if not os.path.exists(IMAGE_DIR):
            print(f"Image directory not found: {IMAGE_DIR}")
            return None
            
        files = [f for f in os.listdir(IMAGE_DIR) if f.lower().endswith(('.jpeg', '.jpg', '.png'))]
        if not files:
            print("No card images found!")
            return None
            
        picks = random.sample(files, 3)
        orientations = [random.choice([False, True]) for _ in picks]
        
        # Animation phase
        animation_start_time = time.time()
        animation_duration = 3.0  # 3 seconds
        
        while True:
            current_time = time.time()
            animation_progress = min(1.0, (current_time - animation_start_time) / animation_duration)
            
            # Handle events
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    return None
                if event.type == KEYDOWN and event.key == K_ESCAPE:
                    pygame.quit()
                    return None
                if event.type == MOUSEBUTTONDOWN and animation_progress >= 1.0:
                    finish_rect = pygame.Rect(SCREEN_WIDTH//2 - 120, SCREEN_HEIGHT - 80, 100, 50)
                    redraw_rect = pygame.Rect(SCREEN_WIDTH//2 + 20, SCREEN_HEIGHT - 80, 100, 50)
                    
                    if finish_rect.collidepoint(event.pos):
                        return list(zip(picks, orientations))
                    if redraw_rect.collidepoint(event.pos):
                        return None
            
            # Create background
            bg = self.create_gradient_background()
            self.add_stars_to_background(bg)
            self.screen.blit(bg, (0, 0))
            
            # Update particles
            self.update_particles()
            
            # Draw title
            self.draw_glowing_text("Your Reading", self.title_font, COLORS['accent_gold'], 
                                 SCREEN_WIDTH // 2, 80)
            
            # Draw cards with animation
            self.draw_cards_with_animation(picks, orientations, animation_progress)
            
            # Draw buttons when animation is complete
            if animation_progress >= 1.0:
                finish_hover = pygame.Rect(SCREEN_WIDTH//2 - 120, SCREEN_HEIGHT - 80, 100, 50).collidepoint(mouse_pos)
                redraw_hover = pygame.Rect(SCREEN_WIDTH//2 + 20, SCREEN_HEIGHT - 80, 100, 50).collidepoint(mouse_pos)
                
                self.draw_button("Accept", SCREEN_WIDTH//2 - 70, SCREEN_HEIGHT - 55, 100, 50, finish_hover)
                self.draw_button("Redraw", SCREEN_WIDTH//2 + 70, SCREEN_HEIGHT - 55, 100, 50, redraw_hover)
            
            pygame.display.flip()
            self.clock.tick(FPS)
    
    def parse_results(self, results):
        """Parse results into the expected format"""
        output_results = {'card1': None, 'card2': None, 'card3': None}
        for i, (filename, orientation) in enumerate(results):
            output_results[f'card{i+1}'] = {
                'name': self.get_card_name(filename),
                'orientation': 'Reversed' if orientation else 'Upright'
            }
        return output_results
    
    def run(self):
        """Main game loop"""
        while True:
            action = self.show_welcome_screen()
            if action is None:
                break
                
            if action == "draw":
                result = self.draw_cards()
                if result:
                    pygame.quit()
                    return self.parse_results(result)

def draw():
    """Main entry point - matches the original API"""
    gui = EnhancedTarotGUI()
    return gui.run()

if __name__ == '__main__':
    results = draw()
    if results:
        print(json.dumps(results, indent=2))