import pygame
import random
import sys
import os

pygame.init()
pygame.mixer.init()

WIDTH = 800
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("State Lounge Ludo")
clock = pygame.time.Clock()

# ----------------------
# Helper to load files in EXE
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # PyInstaller temp folder
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# ----------------------
# Colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (220,50,50)
GREEN = (50,200,50)
BLUE = (50,120,255)
YELLOW = (255,230,50)

font = pygame.font.SysFont("arial", 28)
brand_font = pygame.font.SysFont("arial", 24, True)
watermark_font = pygame.font.SysFont("arial", 120, True)

# ----------------------
# Load assets
board = pygame.image.load(resource_path("assets/board.png"))
dice_sound = pygame.mixer.Sound(resource_path("dice.wav"))
pygame.mixer.music.load(resource_path("music.mp3"))
pygame.mixer.music.play(-1)

# ----------------------
# Game variables
dice_value = 1
players = ["RED","BLUE","GREEN","YELLOW"]
positions = {p: 0 for p in players}
turn_index = 0

# ----------------------
# Drawing functions
def draw_board():
    screen.fill(WHITE)
    screen.blit(board, (0,0))

def draw_dice(value):
    dice_text = font.render(f"Dice: {value}", True, BLACK)
    pygame.draw.rect(screen, WHITE, (350,720,100,50))
    pygame.draw.rect(screen, BLACK, (350,720,100,50), 2)
    screen.blit(dice_text, (360,725))

def draw_turn():
    current_player = players[turn_index]
    text = font.render(f"TURN: {current_player}", True, BLACK)
    screen.blit(text, (330,680))

def draw_branding():
    text = brand_font.render("STATE LOUNGE", True, (60,60,60))
    screen.blit(text,(10,10))
    screen.blit(text,(WIDTH-180,10))
    screen.blit(text,(10,HEIGHT-40))
    screen.blit(text,(WIDTH-180,HEIGHT-40))

def draw_watermark():
    watermark = watermark_font.render("STATE LOUNGE", True, (120,120,120))
    rect = watermark.get_rect(center=(WIDTH//2, HEIGHT//2))
    watermark.set_alpha(60)
    screen.blit(watermark, rect)

# ----------------------
# Game logic
def move_player():
    global turn_index
    player = players[turn_index]
    positions[player] += dice_value
    if positions[player] > 57:
        positions[player] = 57
    turn_index = (turn_index + 1) % 4

def roll_dice():
    global dice_value
    dice_value = random.randint(1,6)
    dice_sound.play()
    move_player()

# ----------------------
# Main loop
running = True
while running:
    draw_board()
    draw_watermark()
    draw_dice(dice_value)
    draw_turn()
    draw_branding()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                roll_dice()

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
