import os
import random
import pygame
from pygame.locals import QUIT, KEYDOWN, MOUSEBUTTONDOWN, K_ESCAPE, K_RETURN, K_KP_ENTER, K_BACKSPACE, K_SPACE, K_UP, K_DOWN
import json
import math
from dotenv import load_dotenv
from prompt_manager import prompt_manager

load_dotenv()

# Directory containing your card images (customized path)
IMAGE_DIR = '/Users/cuishaoyang/Desktop/KaiTeam/Mod_fixer/MCPs/myTarot/images'

# Map file base to display name
NAME_MAP = {
    '01': 'The Magician',
    '02': 'The Popess',
    '03': 'The Empress',
    '04': 'The Emperor',
    '05': 'The Pope',
    '06': 'The Lover',
    '07': 'The Chariot',
    '08': 'Justice',
    '09': 'The Hermit',
    '10': 'The Wheel of Fortune',
    '11': 'Strength',
    '12': 'The Hanged Man',
    '13': 'Death',
    '14': 'Temperance',
    '15': 'The Devil',
    '16': 'The Tower',
    '17': 'The Star',
    '18': 'The Moon',
    '19': 'The Sun',
    '20': 'Judgement',
    '00': 'The Fool',
    '21': 'The World',
    # Add court and minor suits
    'swki': 'King of Swords',
    'swqu': 'Queen of Swords',
    'swkn': 'Knight of Swords',
    'swpa': 'Page of Swords',
    'sw01': 'Ace of Swords',
    'sw02': 'Two of Swords',
    'sw03': 'Three of Swords',
    'sw04': 'Four of Swords',
    'sw05': 'Five of Swords',
    'sw06': 'Six of Swords',
    'sw07': 'Seven of Swords',
    'sw08': 'Eight of Swords',
    'sw09': 'Nine of Swords',
    'sw10': 'Ten of Swords',
    'peki': 'King of Coins',
    'pequ': 'Queen of Coins',
    'pekn': 'Knight of Coins',
    'pepa': 'Page of Coins',
    'pe01': 'Ace of Coins',
    'pe02': 'Two of Coins',
    'pe03': 'Three of Coins',
    'pe04': 'Four of Coins',
    'pe05': 'Five of Coins',
    'pe06': 'Six of Coins',
    'pe07': 'Seven of Coins',
    'pe08': 'Eight of Coins',
    'pe09': 'Nine of Coins',
    'pe10': 'Ten of Coins',
    'cuki': 'King of Cups',
    'cuqu': 'Queen of Cups',
    'cukn': 'Knight of Cups',
    'cupa': 'Page of Cups',
    'cu01': 'Ace of Cups',
    'cu02': 'Two of Cups',
    'cu03': 'Three of Cups',
    'cu04': 'Four of Cups',
    'cu05': 'Five of Cups',
    'cu06': 'Six of Cups',
    'cu07': 'Seven of Cups',
    'cu08': 'Eight of Cups',
    'cu09': 'Nine of Cups',
    'cu10': 'Ten of Cups',
    'waki': 'King of Clubs',
    'waqu': 'Queen of Clubs',
    'wakn': 'Knight of Clubs',
    'wapa': 'Page of Clubs',
    'wa01': 'Ace of Clubs',
    'wa02': 'Two of Clubs',
    'wa03': 'Three of Clubs',
    'wa04': 'Four of Clubs',
    'wa05': 'Five of Clubs',
    'wa06': 'Six of Clubs',
    'wa07': 'Seven of Clubs',
    'wa08': 'Eight of Clubs',
    'wa09': 'Nine of Clubs',
    'wa10': 'Ten of Clubs'
}


# Optimized Configuration for Better Performance
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 800
CARD_WIDTH, CARD_HEIGHT = 180, 300
SPACING = 80
FPS = 60  # Reduced from 120 to 60

# Simplified Color Palette
COLORS = {
    'void_black': (5, 0, 15),
    'deep_purple': (25, 10, 40),
    'mystic_blue': (15, 25, 60),
    'cosmic_gold': (255, 223, 100),
    'ethereal_silver': (220, 220, 255),
    'magic_violet': (148, 0, 211),
    'astral_cyan': (0, 255, 255),
    'divine_white': (255, 255, 255),
    'shadow_grey': (40, 40, 60)
}

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('🔮 MYSTICAL TAROT ORACLE 🔮')
clock = pygame.time.Clock()

# Enable text input for better Chinese IME support
pygame.key.set_repeat()  # Enable key repeat
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN, pygame.TEXTINPUT])  # Allow text input events

# Enhanced Typography with Chinese support
try:
    # Based on available fonts from debug output
    chinese_fonts = ['pingfang', 'hiraginosansgb', 'stheitimedium', 'arialunicode', 'arial']
    title_font = None
    selected_font = None
    
    for font_name in chinese_fonts:
        try:
            test_font = pygame.font.SysFont(font_name, 24)
            if test_font:
                selected_font = font_name
                print(f"Successfully using font: {font_name}")
                break
        except:
            continue
    
    if selected_font:
        title_font = pygame.font.SysFont(selected_font, 48, bold=True)
        subtitle_font = pygame.font.SysFont(selected_font, 24)
        card_font = pygame.font.SysFont(selected_font, 20, bold=True)
        ui_font = pygame.font.SysFont(selected_font, 16)
    else:
        print("No Chinese font found, using default")
        title_font = pygame.font.Font(None, 48)
        subtitle_font = pygame.font.Font(None, 24)
        card_font = pygame.font.Font(None, 20)
        ui_font = pygame.font.Font(None, 16)
        
except Exception as e:
    print(f"Font loading error: {e}")
    # Ultimate fallback to default fonts
    title_font = pygame.font.Font(None, 48)
    subtitle_font = pygame.font.Font(None, 24)
    card_font = pygame.font.Font(None, 20)
    ui_font = pygame.font.Font(None, 16)

class EnhancedCardAnimation:
    def __init__(self, card_img, start_pos, end_pos, delay=0, card_index=0):
        self.card_img = card_img
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.current_pos = list(start_pos)
        self.delay = delay
        self.progress = 0
        self.card_index = card_index
        
        # Enhanced animation properties
        self.rotation = random.uniform(-15, 15)  # Initial rotation
        self.target_rotation = 0
        self.scale = 0.3
        self.bounce_height = 0
        self.glow_intensity = 0
        
        # Particle trail
        self.trail_particles = []
        
    def update(self, dt):
        if self.delay > 0:
            self.delay -= dt
            return False
            
        self.progress = min(1.0, self.progress + dt * 2.5)
        
        # Smooth easing with bounce
        if self.progress < 0.7:
            # Accelerating phase
            ease = self.progress / 0.7
            ease = ease * ease * (3 - 2 * ease)  # Smoothstep
        else:
            # Bounce phase
            bounce_progress = (self.progress - 0.7) / 0.3
            bounce = 1 - abs(math.sin(bounce_progress * math.pi * 2)) * 0.1
            ease = 0.7 / 0.7 + (bounce_progress * 0.3 * bounce)
        
        # Position interpolation
        self.current_pos[0] = self.start_pos[0] + (self.end_pos[0] - self.start_pos[0]) * ease
        self.current_pos[1] = self.start_pos[1] + (self.end_pos[1] - self.start_pos[1]) * ease
        
        # Add slight arc to the movement
        arc_height = 100 * math.sin(self.progress * math.pi)
        self.current_pos[1] -= arc_height
        
        # Rotation animation
        self.rotation = self.rotation * (1 - self.progress) + self.target_rotation * self.progress
        
        # Scale animation
        if self.progress < 0.8:
            self.scale = 0.3 + (1.0 - 0.3) * (self.progress / 0.8)
        else:
            # Small bounce in scale
            bounce_scale = 1 + math.sin((self.progress - 0.8) / 0.2 * math.pi) * 0.1
            self.scale = bounce_scale
        
        # Glow effect
        self.glow_intensity = math.sin(self.progress * math.pi) * 255
        
        # Add particle trail during movement
        if self.progress > 0.1 and self.progress < 0.9 and random.random() < 0.4:
            trail_x = self.current_pos[0] + CARD_WIDTH//2 + random.randint(-10, 10)
            trail_y = self.current_pos[1] + CARD_HEIGHT//2 + random.randint(-10, 10)
            self.trail_particles.append(OptimizedParticle(trail_x, trail_y))
        
        # Update trail particles
        self.trail_particles = [p for p in self.trail_particles if p.update() or True][-10:]  # Limit trail
        
        return self.progress >= 1.0
    
    def draw(self, screen):
        # Draw trail particles first
        for particle in self.trail_particles:
            particle.draw(screen)
        
        if self.delay > 0 or self.scale <= 0:
            return
        
        # Calculate transformed card
        scaled_width = int(CARD_WIDTH * self.scale)
        scaled_height = int(CARD_HEIGHT * self.scale)
        
        if scaled_width > 0 and scaled_height > 0:
            # Scale the card
            scaled_img = pygame.transform.scale(self.card_img, (scaled_width, scaled_height))
            
            # Rotate if needed
            if abs(self.rotation) > 1:
                scaled_img = pygame.transform.rotate(scaled_img, self.rotation)
            
            # Draw glow effect
            if self.glow_intensity > 10:
                glow_alpha = int(self.glow_intensity * 0.3)
                glow_size = int(20 * self.scale)
                glow_surf = pygame.Surface((scaled_width + glow_size*2, scaled_height + glow_size*2), pygame.SRCALPHA)
                
                # Multiple glow layers
                for i in range(3):
                    alpha = glow_alpha // (i + 1)
                    glow_color = (*COLORS['cosmic_gold'], alpha)
                    glow_rect = pygame.Rect(i*glow_size//3, i*glow_size//3, 
                                          scaled_width + (3-i)*glow_size*2//3, 
                                          scaled_height + (3-i)*glow_size*2//3)
                    pygame.draw.ellipse(glow_surf, glow_color, glow_rect)
                
                glow_rect = glow_surf.get_rect(center=(self.current_pos[0] + CARD_WIDTH//2, 
                                                     self.current_pos[1] + CARD_HEIGHT//2))
                screen.blit(glow_surf, glow_rect)
            
            # Draw the card
            card_rect = scaled_img.get_rect(center=(self.current_pos[0] + CARD_WIDTH//2, 
                                                  self.current_pos[1] + CARD_HEIGHT//2))
            screen.blit(scaled_img, card_rect)

class OptimizedParticle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel_x = random.uniform(-0.5, 0.5)
        self.vel_y = random.uniform(-1, -0.3)
        self.size = random.randint(1, 3)
        self.life = random.randint(60, 120)
        self.max_life = self.life
        self.color = random.choice([
            COLORS['cosmic_gold'],
            COLORS['ethereal_silver'],
            COLORS['astral_cyan']
        ])
        
    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y
        self.life -= 1
        
    def draw(self, screen):
        if self.life > 0:
            # Simple circle instead of complex shapes
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
        return self.life > 0

class CardAnimation:
    def __init__(self, card_img, start_pos, end_pos, delay=0):
        self.card_img = card_img
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.current_pos = list(start_pos)
        self.delay = delay
        self.progress = 0
        self.rotation = 0
        self.scale = 0.1
        self.particles = []
        
    def update(self, dt):
        if self.delay > 0:
            self.delay -= dt
            return
            
        self.progress = min(1.0, self.progress + dt * 1.2)
        
        # Smooth easing function
        ease = self.progress * self.progress * (3 - 2 * self.progress)
        
        # Position interpolation with overshoot
        overshoot = 1.0 + 0.1 * math.sin(ease * math.pi)
        self.current_pos[0] = self.start_pos[0] + (self.end_pos[0] - self.start_pos[0]) * ease * overshoot
        self.current_pos[1] = self.start_pos[1] + (self.end_pos[1] - self.start_pos[1]) * ease
        
        # Rotation and scale effects
        self.rotation = (1 - ease) * 720  # Two full spins
        self.scale = 0.1 + ease * 0.9
        
        # Add particle trail during movement
        if ease < 0.9 and random.random() < 0.3:
            particle_x = self.current_pos[0] + CARD_WIDTH//2 + random.randint(-20, 20)
            particle_y = self.current_pos[1] + CARD_HEIGHT//2 + random.randint(-20, 20)
            self.particles.append(OptimizedParticle(particle_x, particle_y))
        
        # Update particles
        self.particles = [p for p in self.particles if p.update() or True]
    
    def draw(self, screen):
        # Draw particles
        self.particles = [p for p in self.particles if p.draw(screen)]
        
        if self.delay > 0 or self.scale <= 0:
            return
            
        # Transform card
        scaled_img = pygame.transform.scale(self.card_img, 
                                          (int(CARD_WIDTH * self.scale), int(CARD_HEIGHT * self.scale)))
        if abs(self.rotation) > 1:
            scaled_img = pygame.transform.rotate(scaled_img, self.rotation)
        
        # Draw magical aura around card
        if self.progress < 1.0:
            aura_size = int(50 * (1 - self.progress))
            aura_surface = pygame.Surface((CARD_WIDTH + aura_size*2, CARD_HEIGHT + aura_size*2), pygame.SRCALPHA)
            for i in range(3):
                alpha = int(30 * (1 - self.progress))
                color = (*COLORS['cosmic_gold'], alpha)
                pygame.draw.ellipse(aura_surface, color, 
                                  (i*aura_size//3, i*aura_size//3, 
                                   CARD_WIDTH + (3-i)*aura_size*2//3, 
                                   CARD_HEIGHT + (3-i)*aura_size*2//3))
            screen.blit(aura_surface, (self.current_pos[0] - aura_size, self.current_pos[1] - aura_size))
        
        # Draw card
        card_rect = scaled_img.get_rect(center=(self.current_pos[0] + CARD_WIDTH//2, 
                                              self.current_pos[1] + CARD_HEIGHT//2))
        screen.blit(scaled_img, card_rect)
        
        return self.progress >= 1.0

def create_simple_background():
    """Create simple gradient background for better performance"""
    bg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    # Simple two-color gradient instead of complex cosmic effects
    for y in range(SCREEN_HEIGHT):
        ratio = y / SCREEN_HEIGHT
        r = int(COLORS['void_black'][0] + (COLORS['deep_purple'][0] - COLORS['void_black'][0]) * ratio)
        g = int(COLORS['void_black'][1] + (COLORS['deep_purple'][1] - COLORS['void_black'][1]) * ratio)
        b = int(COLORS['void_black'][2] + (COLORS['deep_purple'][2] - COLORS['void_black'][2]) * ratio)
        pygame.draw.line(bg, (r, g, b), (0, y), (SCREEN_WIDTH, y))
    
    # Add simple stars
    for _ in range(30):  # Reduced from 50
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT // 2)
        brightness = random.randint(150, 255)
        pygame.draw.circle(bg, (brightness, brightness, brightness), (x, y), 1)
    
    return bg

def draw_simple_text(surface, text, font, color, x, y):
    """Draw text with simple glow - much faster than complex version"""
    # Simple glow with just 2 layers instead of multiple
    for offset in [(-1, -1), (1, 1)]:
        glow_surf = font.render(text, True, (color[0]//3, color[1]//3, color[2]//3))
        surface.blit(glow_surf, (x + offset[0] - glow_surf.get_width()//2, 
                               y + offset[1] - glow_surf.get_height()//2))
    
    # Main text
    text_surf = font.render(text, True, color)
    text_rect = text_surf.get_rect(center=(x, y))
    surface.blit(text_surf, text_rect)
    return text_rect

def load_card_image(filename, reversed=False):
    """Simplified card loading for better performance"""
    path = os.path.join(IMAGE_DIR, filename)
    try:
        img = pygame.image.load(path).convert_alpha()
        img = pygame.transform.smoothscale(img, (CARD_WIDTH, CARD_HEIGHT))
        
        # Simple border instead of complex effects
        bordered = pygame.Surface((CARD_WIDTH + 4, CARD_HEIGHT + 4))
        bordered.fill(COLORS['cosmic_gold'])
        bordered.blit(img, (2, 2))
        
        return pygame.transform.rotate(bordered, 180) if reversed else bordered
    except:
        # Simple placeholder
        placeholder = pygame.Surface((CARD_WIDTH, CARD_HEIGHT))
        placeholder.fill(COLORS['shadow_grey'])
        pygame.draw.rect(placeholder, COLORS['magic_violet'], placeholder.get_rect(), 3)
        return placeholder

def get_ai_reading(question: str, card_results: list) -> str:
    """Generate AI-powered tarot reading"""
    try:
        # Format cards for the prompt
        cards = []
        for filename, orientation in card_results:
            card_name = get_card_name(filename)
            orientation_text = 'Reversed' if orientation else 'Upright'
            cards.append({
                'name': card_name,
                'orientation': orientation_text
            })
        
        # Get AI reading
        reading = prompt_manager.get_tarot_reading_sync(question, cards)
        # print(f"🤖: {reading}")
        return reading
        
    except Exception as e:
        print(f"Error generating AI reading: {e}")
        # Fallback reading
        return """Trust in your intuition and follow your heart. The cards have revealed their wisdom to guide you on your path.

相信你的直觉，跟随你的内心。卡牌已显露它们的智慧，指引你前行的道路。"""

def get_card_name(filename):
    """Get display name for card"""
    base = os.path.splitext(filename)[0]
    short = base[-2:] if base[-2:].isdigit() else base[-4:]
    return NAME_MAP.get(short, base.replace('_', ' ').title())

def enhanced_card_draw():
    """Enhanced card drawing with better animations while keeping performance"""
    if not os.path.exists(IMAGE_DIR):
        print(f"Card images not found at: {IMAGE_DIR}")
        return None
        
    files = [f for f in os.listdir(IMAGE_DIR) if f.lower().endswith(('.jpeg', '.jpg', '.png'))]
    if not files:
        print("No card images found!")
        return None
    
    # Select cards
    picks = random.sample(files, 3)
    orientations = [random.choice([False, True]) for _ in picks]
    
    # Pre-create background for better performance
    bg = create_simple_background()
    
    # Enhanced animation setup
    particles = []
    card_animations = []
    phase = 'intro'  # intro -> dealing -> revealing -> complete
    phase_timer = 0
    
    # Card positions
    total_width = 3 * CARD_WIDTH + 2 * SPACING
    start_x = (SCREEN_WIDTH - total_width) // 2
    card_y = SCREEN_HEIGHT // 2 - CARD_HEIGHT // 2
    
    # Deck position (cards fly from here)
    deck_x = SCREEN_WIDTH // 2 - CARD_WIDTH // 2
    deck_y = -CARD_HEIGHT - 50
    
    # Load card images once
    card_images = [load_card_image(filename, orientation) for filename, orientation in zip(picks, orientations)]
    
    while True:
        dt = clock.tick(FPS) / 1000.0
        phase_timer += dt
        
        # Handle events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return None
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                return None
            if event.type == MOUSEBUTTONDOWN and phase == 'complete':
                mouse_x, mouse_y = event.pos
                accept_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT - 80, 80, 40)
                redraw_rect = pygame.Rect(SCREEN_WIDTH//2 + 20, SCREEN_HEIGHT - 80, 80, 40)
                
                if accept_rect.collidepoint(mouse_x, mouse_y):
                    return list(zip(picks, orientations))
                if redraw_rect.collidepoint(mouse_x, mouse_y):
                    return None
        
        # Phase transitions
        if phase == 'intro' and phase_timer > 1.5:
            phase = 'dealing'
            phase_timer = 0
            
            # Create card animations with staggered delays
            for i, card_img in enumerate(card_images):
                start_pos = (deck_x, deck_y)
                end_pos = (start_x + i * (CARD_WIDTH + SPACING), card_y)
                delay = i * 0.4  # Stagger the cards
                card_animations.append(EnhancedCardAnimation(card_img, start_pos, end_pos, delay, i))
                
        elif phase == 'dealing' and len(card_animations) > 0 and all(anim.update(dt) for anim in card_animations):
            phase = 'revealing'
            phase_timer = 0
        elif phase == 'revealing' and phase_timer > 0.5:
            phase = 'complete'
            phase_timer = 0
        
        # Draw background
        screen.blit(bg, (0, 0))
        
        # Enhanced environmental particles
        if random.random() < 0.05:
            particles.append(OptimizedParticle(
                random.randint(0, SCREEN_WIDTH), 
                random.randint(0, SCREEN_HEIGHT)
            ))
        
        # Update and draw particles (limit count for performance)
        particles = [p for p in particles if p.update() or True][-15:]
        particles = [p for p in particles if p.draw(screen)]
        
        # Title with subtle animation
        title_y = 80 + math.sin(phase_timer * 2) * 5
        draw_simple_text(screen, "MYSTICAL TAROT ORACLE", title_font, COLORS['cosmic_gold'], SCREEN_WIDTH//2, int(title_y))
        
        # Phase-specific rendering
        if phase == 'intro':
            # Opening sequence with pulsing text
            subtitle_color = (COLORS['ethereal_silver'][0], COLORS['ethereal_silver'][1], COLORS['ethereal_silver'][2])
            draw_simple_text(screen, "Preparing your mystical reading...", subtitle_font, subtitle_color, SCREEN_WIDTH//2, 200)
            
            # Add some intro sparkles
            if random.random() < 0.3:
                spark_x = SCREEN_WIDTH//2 + random.randint(-200, 200)
                spark_y = 200 + random.randint(-50, 50)
                particles.append(OptimizedParticle(spark_x, spark_y))
                
        elif phase == 'dealing':
            # Card dealing animation with enhanced effects
            draw_simple_text(screen, "The cards reveal themselves...", subtitle_font, COLORS['astral_cyan'], SCREEN_WIDTH//2, 200)
            
            # Update and draw card animations
            for anim in card_animations:
                anim.update(dt)
                anim.draw(screen)
            
            # Add extra sparkles during dealing
            if random.random() < 0.15:
                particles.append(OptimizedParticle(
                    random.randint(SCREEN_WIDTH//4, 3*SCREEN_WIDTH//4), 
                    random.randint(SCREEN_HEIGHT//3, 2*SCREEN_HEIGHT//3)
                ))
        
        elif phase == 'revealing':
            # Revealing phase with glowing cards
            draw_simple_text(screen, "Your destiny unfolds...", subtitle_font, COLORS['magic_violet'], SCREEN_WIDTH//2, 200)
            
            # Draw cards with revealing glow
            for i, card_img in enumerate(card_images):
                x = start_x + i * (CARD_WIDTH + SPACING)
                
                # Pulsing glow effect during reveal
                glow_intensity = (math.sin(phase_timer * 6 + i) + 1) / 2
                if glow_intensity > 0.3:
                    glow_surf = pygame.Surface((CARD_WIDTH + 30, CARD_HEIGHT + 30), pygame.SRCALPHA)
                    glow_alpha = int(glow_intensity * 100)
                    glow_color = (*COLORS['cosmic_gold'], glow_alpha)
                    pygame.draw.ellipse(glow_surf, glow_color, glow_surf.get_rect())
                    screen.blit(glow_surf, (x - 15, card_y - 15))
                
                screen.blit(card_img, (x, card_y))
                
        else:  # complete
            # Final display with full interactivity
            draw_simple_text(screen, "Your reading is complete!", subtitle_font, COLORS['cosmic_gold'], SCREEN_WIDTH//2, 200)
            
            # Draw final cards with enhanced hover effects
            for i, (filename, orientation) in enumerate(zip(picks, orientations)):
                x = start_x + i * (CARD_WIDTH + SPACING)
                
                # Enhanced hover effect
                mouse_x, mouse_y = pygame.mouse.get_pos()
                card_rect = pygame.Rect(x, card_y, CARD_WIDTH, CARD_HEIGHT)
                is_hover = card_rect.collidepoint(mouse_x, mouse_y)
                
                if is_hover:
                    # Animated glow on hover
                    glow_pulse = (math.sin(phase_timer * 8) + 1) / 2
                    glow_size = int(15 + glow_pulse * 10)
                    glow_surf = pygame.Surface((CARD_WIDTH + glow_size*2, CARD_HEIGHT + glow_size*2), pygame.SRCALPHA)
                    glow_alpha = int(80 + glow_pulse * 40)
                    glow_color = (*COLORS['astral_cyan'], glow_alpha)
                    pygame.draw.ellipse(glow_surf, glow_color, glow_surf.get_rect())
                    screen.blit(glow_surf, (x - glow_size, card_y - glow_size))
                    
                    # Add hover particles
                    if random.random() < 0.2:
                        hover_x = x + random.randint(0, CARD_WIDTH)
                        hover_y = card_y + random.randint(0, CARD_HEIGHT)
                        particles.append(OptimizedParticle(hover_x, hover_y))
                
                screen.blit(card_images[i], (x, card_y))
                
                # Enhanced card information with floating effect
                name = get_card_name(filename)
                orient_text = 'Reversed' if orientation else 'Upright'
                
                # Floating text effect
                text_y_offset = math.sin(phase_timer * 3 + i) * 3
                name_y = card_y + CARD_HEIGHT + 25 + text_y_offset
                draw_simple_text(screen, name, card_font, COLORS['cosmic_gold'], 
                               x + CARD_WIDTH//2, int(name_y))
                
                orient_color = COLORS['magic_violet'] if orientation else COLORS['ethereal_silver']
                orient_y = card_y + CARD_HEIGHT + 50 + text_y_offset
                draw_simple_text(screen, orient_text, ui_font, orient_color,
                               x + CARD_WIDTH//2, int(orient_y))
            
            # Enhanced buttons with glow effects
            mouse_x, mouse_y = pygame.mouse.get_pos()
            
            # Accept button
            accept_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT - 80, 80, 40)
            accept_hover = accept_rect.collidepoint(mouse_x, mouse_y)
            
            if accept_hover:
                # Button glow
                button_glow = pygame.Surface((90, 50), pygame.SRCALPHA)
                pygame.draw.rect(button_glow, (*COLORS['cosmic_gold'], 60), button_glow.get_rect(), border_radius=5)
                screen.blit(button_glow, (accept_rect.x - 5, accept_rect.y - 5))
            
            accept_color = COLORS['cosmic_gold'] if accept_hover else COLORS['shadow_grey']
            pygame.draw.rect(screen, accept_color, accept_rect)
            pygame.draw.rect(screen, COLORS['divine_white'], accept_rect, 2)
            
            draw_simple_text(screen, "ACCEPT", ui_font, 
                           COLORS['void_black'] if accept_hover else COLORS['divine_white'], 
                           accept_rect.centerx, accept_rect.centery)
            
            # Redraw button
            redraw_rect = pygame.Rect(SCREEN_WIDTH//2 + 20, SCREEN_HEIGHT - 80, 80, 40)
            redraw_hover = redraw_rect.collidepoint(mouse_x, mouse_y)
            
            if redraw_hover:
                # Button glow
                button_glow = pygame.Surface((90, 50), pygame.SRCALPHA)
                pygame.draw.rect(button_glow, (*COLORS['magic_violet'], 60), button_glow.get_rect(), border_radius=5)
                screen.blit(button_glow, (redraw_rect.x - 5, redraw_rect.y - 5))
            
            redraw_color = COLORS['magic_violet'] if redraw_hover else COLORS['shadow_grey']
            pygame.draw.rect(screen, redraw_color, redraw_rect)
            pygame.draw.rect(screen, COLORS['divine_white'], redraw_rect, 2)
            
            draw_simple_text(screen, "REDRAW", ui_font, COLORS['divine_white'],
                           redraw_rect.centerx, redraw_rect.centery)
        
        pygame.display.flip()

def question_input_interface():
    """Question input interface where users can ask questions before drawing cards"""
    bg = create_simple_background()
    
    # Enable text input for IME support
    pygame.key.start_text_input()
    
    # Input state
    input_text = ""
    input_active = True
    cursor_visible = True
    cursor_timer = 0
    
    # Create input box rectangle
    input_box = pygame.Rect(SCREEN_WIDTH//2 - 300, SCREEN_HEIGHT//2, 600, 40)
    continue_button = pygame.Rect(SCREEN_WIDTH//2 - 60, SCREEN_HEIGHT//2 + 80, 120, 40)
    
    phase_timer = 0
    particles = []
    
    try:
        while True:
            dt = clock.tick(FPS) / 1000.0
            phase_timer += dt
            cursor_timer += dt
            
            # Toggle cursor visibility
            if cursor_timer > 0.5:
                cursor_visible = not cursor_visible
                cursor_timer = 0
            
            # Handle events
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.key.stop_text_input()
                    pygame.quit()
                    return None
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.key.stop_text_input()
                        pygame.quit()
                        return None
                    elif event.key == K_RETURN or event.key == K_KP_ENTER:
                        if input_text.strip():
                            pygame.key.stop_text_input()
                            return input_text.strip()
                    elif event.key == K_BACKSPACE:
                        input_text = input_text[:-1]
                    # Don't handle other key events here to avoid conflicts with TEXTINPUT
                elif event.type == pygame.TEXTINPUT:
                    # Handle text input (better support for Chinese IME)
                    if len(input_text) < 100:  # Limit input length
                        input_text += event.text
                
                if event.type == MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    
                    # Check continue button click
                    if continue_button.collidepoint(mouse_x, mouse_y) and input_text.strip():
                        pygame.key.stop_text_input()
                        return input_text.strip()
                    
                    # Check input box click
                    input_active = input_box.collidepoint(mouse_x, mouse_y)
            
            # Draw background
            screen.blit(bg, (0, 0))
            
            # Title with animation
            title_y = 100 + math.sin(phase_timer * 2) * 5
            draw_simple_text(screen, "ASK THE CARDS", title_font, COLORS['cosmic_gold'], SCREEN_WIDTH//2, int(title_y))
            
            # Subtitle
            draw_simple_text(screen, "What question burns in your heart?", subtitle_font, COLORS['ethereal_silver'], SCREEN_WIDTH//2, 200)
            draw_simple_text(screen, "你心中燃烧着什么问题？", subtitle_font, COLORS['ethereal_silver'], SCREEN_WIDTH//2, 230)
            
            # Input box
            box_color = COLORS['cosmic_gold'] if input_active else COLORS['shadow_grey']
            pygame.draw.rect(screen, COLORS['void_black'], input_box)
            pygame.draw.rect(screen, box_color, input_box, 3)
            
            # Render input text
            if input_text or input_active:
                text_surface = ui_font.render(input_text, True, COLORS['divine_white'])
                text_rect = text_surface.get_rect()
                text_rect.left = input_box.left + 10
                text_rect.centery = input_box.centery
                
                # Clip text if too long
                if text_rect.width > input_box.width - 30:
                    # Scroll text to show end
                    clip_rect = pygame.Rect(input_box.left + 10, input_box.top, input_box.width - 30, input_box.height)
                    screen.set_clip(clip_rect)
                    text_rect.right = input_box.right - 20
                
                screen.blit(text_surface, text_rect)
                screen.set_clip(None)
                
                # Draw cursor
                if input_active and cursor_visible:
                    cursor_x = min(text_rect.right + 2, input_box.right - 10)
                    cursor_y1 = input_box.centery - 10
                    cursor_y2 = input_box.centery + 10
                    pygame.draw.line(screen, COLORS['cosmic_gold'], (cursor_x, cursor_y1), (cursor_x, cursor_y2), 2)
            
            # Placeholder text
            if not input_text:
                placeholder_text = "Type your question here... 在此输入你的问题..."
                placeholder_surface = ui_font.render(placeholder_text, True, COLORS['shadow_grey'])
                placeholder_rect = placeholder_surface.get_rect()
                placeholder_rect.left = input_box.left + 10
                placeholder_rect.centery = input_box.centery
                screen.blit(placeholder_surface, placeholder_rect)
            
            # Continue button
            mouse_x, mouse_y = pygame.mouse.get_pos()
            continue_hover = continue_button.collidepoint(mouse_x, mouse_y)
            continue_active = input_text.strip() != ""
            
            if continue_hover and continue_active:
                # Button glow
                button_glow = pygame.Surface((130, 50), pygame.SRCALPHA)
                pygame.draw.rect(button_glow, (*COLORS['cosmic_gold'], 60), button_glow.get_rect(), border_radius=5)
                screen.blit(button_glow, (continue_button.x - 5, continue_button.y - 5))
            
            button_color = COLORS['cosmic_gold'] if continue_active else COLORS['shadow_grey']
            text_color = COLORS['void_black'] if continue_active else COLORS['divine_white']
            
            pygame.draw.rect(screen, button_color, continue_button)
            pygame.draw.rect(screen, COLORS['divine_white'], continue_button, 2)
            
            draw_simple_text(screen, "DRAW CARDS", ui_font, text_color, continue_button.centerx, continue_button.centery)
            
            # Add floating particles
            if random.random() < 0.03:
                particles.append(OptimizedParticle(
                    random.randint(0, SCREEN_WIDTH), 
                    random.randint(0, SCREEN_HEIGHT)
                ))
            
            # Update and draw particles
            particles = [p for p in particles if p.update() or True][-15:]
            particles = [p for p in particles if p.draw(screen)]
            
            pygame.display.flip()
    
    except Exception as e:
        pygame.key.stop_text_input()
        print(f"Error in question input: {e}")
        return None

def ai_reading_loading_screen(question: str, card_results: list) -> str:
    """Show loading screen while AI generates the reading"""
    bg = create_simple_background()
    particles = []
    phase_timer = 0
    loading_dots = 0
    loading_timer = 0
    ai_reading = None
    
    # Start AI reading generation in background (simulated)
    import threading
    reading_thread = None
    thread_started = False
    
    def generate_reading():
        nonlocal ai_reading
        ai_reading = get_ai_reading(question, card_results)
    
    while True:
        dt = clock.tick(FPS) / 1000.0
        phase_timer += dt
        loading_timer += dt
        
        # Start thread on first frame
        if not thread_started:
            reading_thread = threading.Thread(target=generate_reading)
            reading_thread.daemon = True
            reading_thread.start()
            thread_started = True
        
        # Update loading animation
        if loading_timer > 0.5:
            loading_dots = (loading_dots + 1) % 4
            loading_timer = 0
        
        # Check if reading is complete
        if ai_reading is not None:
            return ai_reading
        
        # Handle events (allow user to quit)
        for event in pygame.event.get():
            if event.type == QUIT:
                return None
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                return None
        
        # Draw background
        screen.blit(bg, (0, 0))
        
        # Title
        title_y = 150 + math.sin(phase_timer * 2) * 10
        draw_simple_text(screen, "MYSTICAL DIVINATION", title_font, COLORS['cosmic_gold'], 
                       SCREEN_WIDTH//2, int(title_y))
        
        # Loading messages with animation
        messages = [
            "The Oracle consults the ancient wisdom",
            "神谕师正在解读卡面的奥秘",
            "Interpreting the cosmic patterns", 
            "寻找命运的指引"
        ]
        
        # Cycle through messages
        message_index = int(phase_timer * 0.7) % len(messages)
        current_message = messages[message_index] + "." * loading_dots
        
        draw_simple_text(screen, current_message, subtitle_font, COLORS['ethereal_silver'], 
                       SCREEN_WIDTH//2, 250)
        
        # Draw small card previews
        preview_y = 350
        total_width = 3 * 60 + 2 * 30  # Smaller cards
        start_x = (SCREEN_WIDTH - total_width) // 2
        
        for i, (filename, orientation) in enumerate(card_results):
            x = start_x + i * 90
            
            try:
                card_img = load_card_image(filename, orientation)
                small_card = pygame.transform.scale(card_img, (60, 100))
                
                # Add mystical glow effect
                glow_intensity = (math.sin(phase_timer * 3 + i) + 1) / 2
                if glow_intensity > 0.3:
                    glow_surf = pygame.Surface((80, 120), pygame.SRCALPHA)
                    glow_alpha = int(glow_intensity * 60)
                    glow_color = (*COLORS['cosmic_gold'], glow_alpha)
                    pygame.draw.ellipse(glow_surf, glow_color, glow_surf.get_rect())
                    screen.blit(glow_surf, (x - 10, preview_y - 10))
                
                screen.blit(small_card, (x, preview_y))
            except:
                # Fallback rectangle
                rect = pygame.Rect(x, preview_y, 60, 100)
                pygame.draw.rect(screen, COLORS['shadow_grey'], rect)
                pygame.draw.rect(screen, COLORS['cosmic_gold'], rect, 2)
        
        # Mystical progress indicator
        progress_y = 500
        progress_width = 300
        progress_x = SCREEN_WIDTH//2 - progress_width//2
        
        # Background bar
        progress_bg = pygame.Rect(progress_x, progress_y, progress_width, 6)
        pygame.draw.rect(screen, COLORS['shadow_grey'], progress_bg)
        
        # Animated progress (fake but looks good)
        progress = (math.sin(phase_timer * 2) + 1) / 2 * 0.7 + 0.3
        progress_fill_width = int(progress_width * progress)
        progress_fill = pygame.Rect(progress_x, progress_y, progress_fill_width, 6)
        pygame.draw.rect(screen, COLORS['cosmic_gold'], progress_fill)
        
        # Add mystical particles
        if random.random() < 0.1:
            particles.append(OptimizedParticle(
                random.randint(0, SCREEN_WIDTH),
                random.randint(0, SCREEN_HEIGHT)
            ))
        
        # Update and draw particles
        particles = [p for p in particles if p.update() or True][-20:]
        particles = [p for p in particles if p.draw(screen)]
        
        # Instructions
        draw_simple_text(screen, "Please wait while the cards reveal their secrets...", 
                       ui_font, COLORS['shadow_grey'], SCREEN_WIDTH//2, SCREEN_HEIGHT - 50)
        
        pygame.display.flip()

def show_final_results(question, card_results, ai_reading):
    """Show final results with horizontal card layout and scrollable reading area"""
    bg = create_simple_background()
    particles = []
    phase_timer = 0
    scroll_offset = 0  # For scrolling functionality
    max_scroll = 0
    
    # Create buttons
    new_reading_button = pygame.Rect(SCREEN_WIDTH//2 - 120, SCREEN_HEIGHT - 60, 100, 40)
    exit_button = pygame.Rect(SCREEN_WIDTH//2 + 20, SCREEN_HEIGHT - 60, 100, 40)
    
    while True:
        dt = clock.tick(FPS) / 1000.0
        phase_timer += dt
        
        # Handle events
        for event in pygame.event.get():
            if event.type == QUIT:
                return 'exit'
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return 'exit'
                elif event.key == K_SPACE or event.key == K_RETURN:
                    return 'new'  # New reading
                elif event.key == K_UP:
                    scroll_offset = max(0, scroll_offset - 30)
                elif event.key == K_DOWN:
                    scroll_offset = min(max_scroll, scroll_offset + 30)
            if event.type == MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if new_reading_button.collidepoint(mouse_x, mouse_y):
                    return 'new'
                elif exit_button.collidepoint(mouse_x, mouse_y):
                    return 'exit'
                # Handle scroll wheel
                elif event.button == 4:  # Scroll up
                    scroll_offset = max(0, scroll_offset - 30)
                elif event.button == 5:  # Scroll down
                    scroll_offset = min(max_scroll, scroll_offset + 30)
        
        # Draw background
        screen.blit(bg, (0, 0))
        
        # Title
        title_y = 30 + math.sin(phase_timer * 2) * 3
        draw_simple_text(screen, "YOUR TAROT READING", title_font, COLORS['cosmic_gold'], SCREEN_WIDTH//2, int(title_y))
        
        # Show question (centered, compact)
        draw_simple_text(screen, "Your Question:", pygame.font.SysFont('pingfang', 14), COLORS['ethereal_silver'], SCREEN_WIDTH//2, 75)
        
        # Wrap and display question
        question_words = question.split()
        question_lines = []
        current_line = ""
        
        for word in question_words:
            test_line = current_line + " " + word if current_line else word
            if len(test_line) > 90:  # Longer line for compact layout
                if current_line:
                    question_lines.append(current_line)
                current_line = word
            else:
                current_line = test_line
        if current_line:
            question_lines.append(current_line)
        
        # Draw question lines
        for i, line in enumerate(question_lines[:2]):  # Max 2 lines to save space
            draw_simple_text(screen, line, pygame.font.SysFont('pingfang', 12), COLORS['astral_cyan'], SCREEN_WIDTH//2, 95 + i * 18)
        
        # Top section: Cards in horizontal layout (smaller)
        card_section_y = 140
        card_width_small = int(CARD_WIDTH * 0.4)  # Much smaller cards
        card_height_small = int(CARD_HEIGHT * 0.4)
        card_spacing = 50
        
        # Calculate total width and starting position for centering
        total_cards_width = 3 * card_width_small + 2 * card_spacing
        cards_start_x = (SCREEN_WIDTH - total_cards_width) // 2
        
        for i, (filename, orientation) in enumerate(card_results):
            card_x = cards_start_x + i * (card_width_small + card_spacing)
            
            # Load and draw actual card image
            try:
                card_img = load_card_image(filename, orientation)
                scaled_card = pygame.transform.scale(card_img, (card_width_small, card_height_small))
                screen.blit(scaled_card, (card_x, card_section_y))
                
                # Card info below image
                name = get_card_name(filename)
                orient_text = 'Reversed' if orientation else 'Upright'
                
                # Use Chinese-supporting font
                try:
                    info_font = pygame.font.SysFont('pingfang', 10)
                    if not info_font:
                        info_font = pygame.font.SysFont('hiraginosansgb', 10)
                    if not info_font:
                        info_font = pygame.font.Font(None, 10)
                except:
                    info_font = pygame.font.Font(None, 10)
                
                # Card name (truncate if too long)
                if len(name) > 15:
                    name = name[:12] + "..."
                    
                draw_simple_text(screen, name, info_font, COLORS['cosmic_gold'], 
                               card_x + card_width_small//2, card_section_y + card_height_small + 15)
                
                orient_color = COLORS['magic_violet'] if orientation else COLORS['ethereal_silver']
                draw_simple_text(screen, orient_text, info_font, orient_color,
                               card_x + card_width_small//2, card_section_y + card_height_small + 30)
                
            except:
                # Fallback rectangle
                card_rect = pygame.Rect(card_x, card_section_y, card_width_small, card_height_small)
                pygame.draw.rect(screen, COLORS['shadow_grey'], card_rect)
                pygame.draw.rect(screen, COLORS['cosmic_gold'], card_rect, 2)
        
        # Bottom section: Large scrollable reading area
        reading_area_y = card_section_y + card_height_small + 60
        reading_area_height = SCREEN_HEIGHT - reading_area_y - 100  # Leave space for buttons
        reading_area_width = SCREEN_WIDTH - 80
        reading_area_x = 40
        
        # Draw reading area background
        reading_surface = pygame.Surface((reading_area_width, reading_area_height), pygame.SRCALPHA)
        pygame.draw.rect(reading_surface, (*COLORS['void_black'], 200), reading_surface.get_rect())
        pygame.draw.rect(reading_surface, COLORS['cosmic_gold'], reading_surface.get_rect(), 3)
        screen.blit(reading_surface, (reading_area_x, reading_area_y))
        
        # Reading area title
        draw_simple_text(screen, "Oracle's Wisdom 神谕师的智慧", pygame.font.SysFont('pingfang', 18, bold=True), 
                       COLORS['cosmic_gold'], SCREEN_WIDTH//2, reading_area_y + 25)
        
        # Display AI reading with scrolling support
        if ai_reading:
            # Use Chinese-supporting font for the reading
            try:
                reading_font = pygame.font.SysFont('pingfang', 14)
                if not reading_font:
                    reading_font = pygame.font.SysFont('hiraginosansgb', 14)
                if not reading_font:
                    reading_font = ui_font
            except:
                reading_font = ui_font
            
            # Prepare text rendering with scrolling - FIXED boundaries
            text_area_width = reading_area_width - 80  # More conservative padding for scrollbar
            text_start_x = reading_area_x + 30
            text_start_y = reading_area_y + 50
            line_height = 20
            
            # Process the reading text and calculate all lines with better word wrapping
            all_lines = []
            reading_paragraphs = ai_reading.split('\n\n')
            
            for paragraph in reading_paragraphs:
                if not paragraph.strip():
                    all_lines.append("")  # Empty line for paragraph break
                    continue
                    
                # Better word wrap for each paragraph - handle long words
                words = paragraph.strip().split()
                current_line = ""
                
                for word in words:
                    # Test if adding this word would exceed the width
                    test_line = current_line + " " + word if current_line else word
                    test_surface = reading_font.render(test_line, True, COLORS['ethereal_silver'])
                    
                    # More conservative width check to prevent overflow
                    if test_surface.get_width() <= text_area_width - 20:  # Extra margin
                        current_line = test_line
                    else:
                        # Save the current line and start a new one
                        if current_line:
                            all_lines.append(current_line)
                            current_line = word
                        else:
                            # Handle very long single words by truncating
                            if len(word) > 50:  # Arbitrary long word threshold
                                # Split long word
                                while word:
                                    temp_word = word
                                    while temp_word and reading_font.render(temp_word, True, COLORS['ethereal_silver']).get_width() > text_area_width - 20:
                                        temp_word = temp_word[:-1]
                                    if temp_word:
                                        all_lines.append(temp_word)
                                        word = word[len(temp_word):]
                                    else:
                                        # Single character is still too wide, truncate
                                        all_lines.append(word[:1])
                                        word = word[1:]
                                current_line = ""
                            else:
                                current_line = word
                
                # Add the final line of the paragraph
                if current_line:
                    all_lines.append(current_line)
                all_lines.append("")  # Empty line between paragraphs
            
            # Calculate maximum scroll based on content height
            total_content_height = len(all_lines) * line_height
            visible_height = reading_area_height - 80  # Account for title and padding
            max_scroll = max(0, total_content_height - visible_height)
            
            # Render visible lines with scroll offset
            visible_lines = int(visible_height // line_height)
            start_line = min(len(all_lines), int(scroll_offset // line_height))
            end_line = min(len(all_lines), start_line + visible_lines + 2)
            
            # Set clipping area for the text - FIXED clipping boundaries
            clip_rect = pygame.Rect(reading_area_x + 15, text_start_y, text_area_width, visible_height)
            screen.set_clip(clip_rect)
            
            current_y = text_start_y - (scroll_offset % line_height)
            
            for i in range(start_line, end_line):
                if i < len(all_lines):
                    line = all_lines[i]
                    if line.strip():  # Don't render empty lines, just skip
                        # Double check width before rendering
                        text_surface = reading_font.render(line, True, COLORS['ethereal_silver'])
                        
                        # Ensure text doesn't exceed boundaries
                        if text_surface.get_width() <= text_area_width - 20:
                            screen.blit(text_surface, (text_start_x, current_y))
                        else:
                            # Emergency truncation if somehow a line is still too wide
                            truncated_line = line
                            while truncated_line and reading_font.render(truncated_line + "...", True, COLORS['ethereal_silver']).get_width() > text_area_width - 20:
                                truncated_line = truncated_line[:-1]
                            if truncated_line:
                                text_surface = reading_font.render(truncated_line + "...", True, COLORS['ethereal_silver'])
                                screen.blit(text_surface, (text_start_x, current_y))
                    current_y += line_height
            
            # Remove clipping
            screen.set_clip(None)
            
            # Draw scrollbar if content is scrollable
            if max_scroll > 0:
                scrollbar_x = reading_area_x + reading_area_width - 20  # Move scrollbar further left
                scrollbar_y = reading_area_y + 50
                scrollbar_height = visible_height
                scrollbar_width = 10
                
                # Scrollbar background
                pygame.draw.rect(screen, COLORS['shadow_grey'], 
                               (scrollbar_x, scrollbar_y, scrollbar_width, scrollbar_height))
                
                # Scrollbar thumb
                thumb_height = max(20, int(scrollbar_height * visible_height / total_content_height))
                thumb_y = scrollbar_y + int((scroll_offset / max_scroll) * (scrollbar_height - thumb_height))
                pygame.draw.rect(screen, COLORS['cosmic_gold'], 
                               (scrollbar_x, thumb_y, scrollbar_width, thumb_height))
        
        # Instructions for scrolling
        if max_scroll > 0:
            draw_simple_text(screen, "Use ↑↓ or scroll wheel to navigate • 使用上下箭头或滚轮导航", 
                           pygame.font.SysFont('pingfang', 10), COLORS['shadow_grey'], SCREEN_WIDTH//2, reading_area_y + reading_area_height + 10)
        
        # Draw buttons
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        # New Reading button
        new_hover = new_reading_button.collidepoint(mouse_x, mouse_y)
        if new_hover:
            button_glow = pygame.Surface((110, 50), pygame.SRCALPHA)
            pygame.draw.rect(button_glow, (*COLORS['cosmic_gold'], 60), button_glow.get_rect(), border_radius=5)
            screen.blit(button_glow, (new_reading_button.x - 5, new_reading_button.y - 5))
        
        button_color = COLORS['cosmic_gold'] if new_hover else COLORS['shadow_grey']
        text_color = COLORS['void_black'] if new_hover else COLORS['divine_white']
        pygame.draw.rect(screen, button_color, new_reading_button)
        pygame.draw.rect(screen, COLORS['divine_white'], new_reading_button, 2)
        draw_simple_text(screen, "NEW READING", pygame.font.SysFont('pingfang', 12), text_color, 
                       new_reading_button.centerx, new_reading_button.centery)
        
        # Exit button
        exit_hover = exit_button.collidepoint(mouse_x, mouse_y)
        if exit_hover:
            button_glow = pygame.Surface((110, 50), pygame.SRCALPHA)
            pygame.draw.rect(button_glow, (*COLORS['magic_violet'], 60), button_glow.get_rect(), border_radius=5)
            screen.blit(button_glow, (exit_button.x - 5, exit_button.y - 5))
        
        button_color = COLORS['magic_violet'] if exit_hover else COLORS['shadow_grey']
        pygame.draw.rect(screen, button_color, exit_button)
        pygame.draw.rect(screen, COLORS['divine_white'], exit_button, 2)
        draw_simple_text(screen, "EXIT", pygame.font.SysFont('pingfang', 12), COLORS['divine_white'], 
                       exit_button.centerx, exit_button.centery)
        
        # Add floating particles
        if random.random() < 0.02:
            particles.append(OptimizedParticle(
                random.randint(0, SCREEN_WIDTH), 
                random.randint(0, SCREEN_HEIGHT)
            ))
        
        # Update and draw particles
        particles = [p for p in particles if p.update() or True][-10:]
        particles = [p for p in particles if p.draw(screen)]
        
        pygame.display.flip()

def parse_results(results):
    """Parse results into expected format"""
    output_results = {'card1': None, 'card2': None, 'card3': None}
    for i, (filename, orientation) in enumerate(results):
        output_results[f'card{i+1}'] = {
            'name': get_card_name(filename),
            'orientation': 'Reversed' if orientation else 'Upright'
        }
    return output_results

def draw_TarotCards():
    """Main entry point with question input first"""
    while True:
        # Simple welcome screen
        bg = create_simple_background()
        
        while True:
            clock.tick(FPS)
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    return None
                if event.type == KEYDOWN and event.key == K_ESCAPE:
                    pygame.quit()
                    return None
                if event.type in (KEYDOWN, MOUSEBUTTONDOWN):
                    if event.type != KEYDOWN or event.key == K_SPACE:
                        break
            else:
                # Draw background
                screen.blit(bg, (0, 0))
                
                # Simple title
                draw_simple_text(screen, "MYSTICAL TAROT ORACLE", title_font, 
                               COLORS['cosmic_gold'], SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 100)
                
                # Simple instructions
                instructions = [
                    "Press SPACE or Click to Ask Your Question",
                    "Press ESC to Exit"
                ]
                
                for i, instruction in enumerate(instructions):
                    y = SCREEN_HEIGHT//2 + i * 40
                    draw_simple_text(screen, instruction, subtitle_font, COLORS['ethereal_silver'], SCREEN_WIDTH//2, y)
                
                pygame.display.flip()
                continue
            
            # Get user question first
            user_question = question_input_interface()
            if not user_question:
                pygame.quit()
                return None
            
            # Then start the enhanced card drawing
            result = enhanced_card_draw()
            if result:
                # Show AI loading screen and get reading
                ai_reading = ai_reading_loading_screen(user_question, result)
                if ai_reading is None:
                    # User quit during loading
                    pygame.quit()
                    return None
                
                # Show final results with AI reading
                user_choice = show_final_results(user_question, result, ai_reading)
                if user_choice == 'exit':
                    pygame.quit()
                    return parse_results(result)
                # If user_choice == 'new', continue to start a new reading
                continue
            else:
                # If no result (user cancelled), go back to welcome screen
                continue

def draw():
    """Main entry point for compatibility"""
    return draw_TarotCards()

  
if __name__ == '__main__':
    results = draw()
    if results:
        print(json.dumps(results, indent=2))