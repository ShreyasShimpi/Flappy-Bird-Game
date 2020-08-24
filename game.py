import pygame
import random

# Initialization
pygame.mixer.pre_init(channels=1, frequency=44100)
pygame.init()
window = pygame.display.set_mode((288, 512))
pygame.display.set_caption("Flappy Bird")
font = pygame.font.Font('04B_19__.ttf', 30)
clock = pygame.time.Clock()

# Variables
G = 0.25
BIRD_MOVE = 0
active = False
# FRAME = 60

BG = pygame.image.load('sprites/background-day.png').convert()

FLOOR = pygame.image.load('sprites/base.png').convert()
FLOOR_POS = 0

BIRD = [pygame.image.load('sprites/bluebird-upflap.png').convert_alpha(),
        pygame.image.load('sprites/bluebird-midflap.png').convert_alpha(),
        pygame.image.load('sprites/bluebird-downflap.png').convert_alpha()]
BIRD_INDEX = 0
BIRD_RECT = BIRD[BIRD_INDEX].get_rect(center=(100, 256))
FLAP = pygame.USEREVENT + 1
pygame.time.set_timer(FLAP, 200)


PIPE = pygame.image.load('sprites/pipe-green.png').convert()
PIPE_LIST = []
SPAWNPIPE = pygame.USEREVENT  # this to create object after timer runs out
pygame.time.set_timer(SPAWNPIPE, 1200)
PIPE_HEIGHT = [256, 280, 300, 320, 335, 350]
GAP = 150

SCORE = 0
HIGH_SCORE = 0
# OVER = pygame.image.load('sprites/gameover.png').convert_alpha()
# OVER_RECT = OVER.get_rect(center=(144, 256))

OVERLAY = pygame.image.load('sprites/message.png').convert_alpha()
OVERLAY_RECT = OVERLAY.get_rect(center=(144, 256))

# Sound Effects
FLAP_SOUND = pygame.mixer.Sound('audio/wing.wav')
HIT_SOUND = pygame.mixer.Sound('audio/hit.wav')
SCORE_SOUND = pygame.mixer.Sound('audio/point.wav')



# Draws Floor
def draw_floor():
    window.blit(FLOOR, (FLOOR_POS, 450))
    window.blit(FLOOR, (FLOOR_POS + 336, 450))


# Draws Pipes
def draw_pipes(pipelist):
    for pipe in pipelist:
        if pipe.bottom >= 512:
            window.blit(PIPE, pipe)
        else:
            window.blit(pygame.transform.flip(PIPE, False, True), pipe)


# Pipe Creation
def create_pipe():
    rand = random.choice(PIPE_HEIGHT)
    bottom_pipe = PIPE.get_rect(midtop=(300, rand))
    top_pipe = PIPE.get_rect(midbottom=(300, rand - GAP))
    return bottom_pipe, top_pipe


# Pipe Movement
def move_pipe(pipelist):
    for pipe in pipelist:
        pipe[0] -= 3
    return pipelist


# Collision
def collide(pipelist):
    for pipe in pipelist:
        if BIRD_RECT.colliderect(pipe):
            HIT_SOUND.play()
            return False

    if BIRD_RECT.top <= -100 or BIRD_RECT.bottom >= 450:
        HIT_SOUND.play()
        return False

    return True


# Rotation of the Bird
def rotate(bird):
    new_bird = pygame.transform.rotozoom(bird, BIRD_MOVE*-3, 1)
    return new_bird


# Show score on screen
def show_score(state):
    if state == "active":
        text = font.render("SCORE: " + str(int(SCORE)), True, (255, 255, 255))
        text_rect = text.get_rect(center=(144, 50))
        window.blit(text, text_rect)
    if state == "over":
        text = font.render("SCORE: " + str(int(SCORE)), True, (255, 255, 255))
        text_rect = text.get_rect(center=(144, 50))
        window.blit(text, text_rect)

        text_h = font.render("HIGH SCORE: " + str(int(HIGH_SCORE)), True, (255, 255, 255))
        text_rect_h = text_h.get_rect(center=(144, 430))
        window.blit(text_h, text_rect_h)


# update the high score
def update(score, high_score):
    if score > high_score:
        high_score = score
    return high_score


run = True
while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # Bird Movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and active:
                BIRD_MOVE = 0
                BIRD_MOVE -= 7
                FLAP_SOUND.play()
            if event.key == pygame.K_SPACE and not active:
                active = True
                PIPE_LIST.clear()
                BIRD_RECT.center = (100, 256)
                BIRD_MOVE = 0
                SCORE = 0
        # adding pipes to list
        if event.type == SPAWNPIPE:
            PIPE_LIST.extend(create_pipe())
        # Flapping Animation
        if event.type == FLAP:
            BIRD_INDEX += 1
            BIRD_INDEX = BIRD_INDEX % len(BIRD)

    # Background
    window.blit(BG, (0, 0))

    # collision check
    if active:
        # Bird Movement
        BIRD_MOVE += G  # this is actually giving an acceleration
        BIRD_ROTATED = rotate(BIRD[BIRD_INDEX])
        BIRD_RECT[1] += BIRD_MOVE
        window.blit(BIRD_ROTATED, BIRD_RECT)
        # pygame.draw.rect(window, (0, 0, 0), BIRD_RECT, 2)

        # Pipe Movement
        PIPE_LIST = move_pipe(PIPE_LIST)
        draw_pipes(PIPE_LIST)

        # collision
        active = collide(PIPE_LIST)

        # Show score
        SCORE += 0.0166
        show_score("active")
        # FRAME -= 1
        # if FRAME <= 0:
        #     SCORE_SOUND.play()
        #     FRAME = 60
    else:
        HIGH_SCORE = update(SCORE, HIGH_SCORE)
        window.blit(OVERLAY, OVERLAY_RECT)
        show_score("over")

    # Floor Movement
    FLOOR_POS -= 1
    draw_floor()
    if FLOOR_POS == -336:
        FLOOR_POS = 0

    # Update the display
    pygame.display.update()

    # FPS
    clock.tick(60)
