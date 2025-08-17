import pygame
import random
import sys

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Screen settings
WIDTH, HEIGHT = 400, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🐥 Flappy Bird Pro - by Manish Yadav")

# Load assets
BG = pygame.image.load("assets/background-night.png").convert()
BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))

GROUND = pygame.image.load("assets/base.png").convert()
GROUND = pygame.transform.scale(GROUND, (WIDTH, 100))

BIRD_FRAMES = [
    pygame.image.load("assets/redbird-downflap.png").convert_alpha(),
    pygame.image.load("assets/redbird-midflap.png").convert_alpha(),
    pygame.image.load("assets/redbird-upflap.png").convert_alpha(),
]
for i in range(len(BIRD_FRAMES)):
    BIRD_FRAMES[i] = pygame.transform.scale(BIRD_FRAMES[i], (40, 30))

PIPE_IMAGE = pygame.image.load("assets/pipe-red.png").convert_alpha()
PIPE_IMAGE = pygame.transform.scale(PIPE_IMAGE, (70, HEIGHT))

# Sounds
flap_sound = pygame.mixer.Sound("assets/wing.wav")
hit_sound = pygame.mixer.Sound("assets/hit.wav")
point_sound = pygame.mixer.Sound("assets/point.wav")

# Colors
WHITE = (255, 255, 255)
YELLOW = (255, 215, 0)
RED = (220, 20, 60)

# Game variables
gravity = 0.4
bird_movement = 0
game_active = False
menu_active = False  
splash_active = True  # Start from splash screen
score = 0
high_score = 0
passed_pipes = []

# Bird
bird_index = 0
bird = BIRD_FRAMES[bird_index]
bird_rect = bird.get_rect(center=(WIDTH // 4, HEIGHT // 2))
BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

# Pipes
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [250, 300, 350]
PIPE_GAP = 170

def create_pipe():
    height = random.choice(pipe_height)
    bottom = PIPE_IMAGE.get_rect(midtop=(WIDTH + 100, height))
    top = PIPE_IMAGE.get_rect(midbottom=(WIDTH + 100, height - PIPE_GAP))
    return bottom, top

def move_pipes(pipes):
    for p in pipes:
        p.centerx -= 4
    return [p for p in pipes if p.right > 0]

def draw_pipes(pipes):
    for p in pipes:
        if p.bottom >= HEIGHT:
            SCREEN.blit(PIPE_IMAGE, p)
        else:
            flip_pipe = pygame.transform.flip(PIPE_IMAGE, False, True)
            SCREEN.blit(flip_pipe, p)

def check_collision(pipes):
    for p in pipes:
        if bird_rect.colliderect(p):
            hit_sound.play()
            return False
    if bird_rect.top <= -50 or bird_rect.bottom >= HEIGHT - 100:
        hit_sound.play()
        return False
    return True

def display_score(game_state):
    font = pygame.font.Font("freesansbold.ttf", 32)
    if game_state == "main_game":
        score_surface = font.render(f"{int(score)}", True, WHITE)
        score_rect = score_surface.get_rect(center=(WIDTH // 2, 50))
        SCREEN.blit(score_surface, score_rect)
    if game_state == "game_over":
        score_surface = font.render(f"Score: {int(score)}", True, WHITE)
        score_rect = score_surface.get_rect(center=(WIDTH // 2, 100))
        SCREEN.blit(score_surface, score_rect)

        high_surface = font.render(f"Best: {int(high_score)}", True, WHITE)
        high_rect = high_surface.get_rect(center=(WIDTH // 2, 150))
        SCREEN.blit(high_surface, high_rect)

def rotate_bird(bird):
    return pygame.transform.rotozoom(bird, -bird_movement * 3, 1)

def bird_animation():
    new_bird = BIRD_FRAMES[bird_index]
    new_bird_rect = new_bird.get_rect(center=(WIDTH // 4, bird_rect.centery))
    return new_bird, new_bird_rect

def draw_button(text, x, y, w, h, color, hover_color):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x < mouse[0] < x + w and y < mouse[1] < y + h:
        pygame.draw.rect(SCREEN, hover_color, (x, y, w, h), border_radius=15)
        if click[0] == 1:  
            return True
    else:
        pygame.draw.rect(SCREEN, color, (x, y, w, h), border_radius=15)

    font = pygame.font.Font("freesansbold.ttf", 28)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=(x + w // 2, y + h // 2))
    SCREEN.blit(text_surface, text_rect)
    return False

def reset_game():
    global bird_movement, score, passed_pipes, pipe_list, bird_rect
    pipe_list.clear()
    bird_rect.center = (WIDTH // 4, HEIGHT // 2)
    bird_movement = 0
    score = 0
    passed_pipes = []

clock = pygame.time.Clock()
ground_x = 0

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if splash_active:  # Go to menu from splash
                    splash_active = False
                    menu_active = True
                elif menu_active:  # Start from menu
                    menu_active = False
                    game_active = True
                    reset_game()
                elif game_active:  # Flap
                    bird_movement = 0
                    bird_movement -= 6
                    flap_sound.play()
                else:  # Restart after game over
                    game_active = True
                    reset_game()

        if event.type == SPAWNPIPE and game_active:
            pipe_list.extend(create_pipe())

        if event.type == BIRDFLAP:
            bird_index = (bird_index + 1) % len(BIRD_FRAMES)
            bird, bird_rect = bird_animation()

    SCREEN.blit(BG, (0, 0))

    if splash_active:
        # Custom splash/intro
        font_big = pygame.font.Font("freesansbold.ttf", 40)
        font_small = pygame.font.Font("freesansbold.ttf", 22)

        title_surface = font_big.render("🐥 Flappy Bird Pro", True, YELLOW)
        title_rect = title_surface.get_rect(center=(WIDTH // 2, 150))
        SCREEN.blit(title_surface, title_rect)

        dev_surface = font_small.render("Created by Manish Yadav", True, WHITE)
        dev_rect = dev_surface.get_rect(center=(WIDTH // 2, 250))
        SCREEN.blit(dev_surface, dev_rect)

        tagline = font_small.render("Enjoy the game & beat the high score!", True, WHITE)
        tagline_rect = tagline.get_rect(center=(WIDTH // 2, 300))
        SCREEN.blit(tagline, tagline_rect)

        if draw_button("CONTINUE", 120, 400, 160, 60, RED, (255, 80, 80)):
            splash_active = False
            menu_active = True

    elif menu_active:
        font = pygame.font.Font("freesansbold.ttf", 48)
        title_surface = font.render("Main Menu", True, YELLOW)
        title_rect = title_surface.get_rect(center=(WIDTH // 2, 150))
        SCREEN.blit(title_surface, title_rect)

        if draw_button("PLAY", 120, 250, 160, 60, RED, (255, 80, 80)):
            menu_active = False
            game_active = True
            reset_game()

        if draw_button("QUIT", 120, 350, 160, 60, RED, (255, 80, 80)):
            quit()
            
    elif game_active:
        # Bird
        bird_movement += gravity
        bird_rect.centery += int(bird_movement)
        rotated_bird = rotate_bird(bird)
        SCREEN.blit(rotated_bird, bird_rect)

        # Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        # Collision
        game_active = check_collision(pipe_list)

        # Score
        for p in pipe_list[::2]:
            if p.centerx < bird_rect.centerx and p not in passed_pipes:
                score += 1
                passed_pipes.append(p)
                point_sound.play()

        display_score("main_game")

    else:  # Game Over screen
        if score > high_score:
            high_score = score
        display_score("game_over")

        font = pygame.font.Font("freesansbold.ttf", 28)
        msg_surface = font.render("Press SPACE to Restart", True, WHITE)
        msg_rect = msg_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        SCREEN.blit(msg_surface, msg_rect)

        if draw_button("MENU", 120, 400, 160, 60, RED, (255, 80, 80)):
            menu_active = True
            game_active = False

    # Ground
    ground_x -= 2
    if ground_x <= -WIDTH:
        ground_x = 0
    SCREEN.blit(GROUND, (ground_x, HEIGHT - 100))
    SCREEN.blit(GROUND, (ground_x + WIDTH, HEIGHT - 100))

    pygame.display.update()
    clock.tick(60)
