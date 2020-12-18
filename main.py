import pygame, sys, random


def draw_floor():
    screen.blit(floor_surface, (floor_x_position, 450))
    screen.blit(floor_surface, (floor_x_position + 283, 450))


def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(350, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom=(350, random_pipe_pos-150))
    return bottom_pipe, top_pipe


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 3
    return pipes


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 512:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)  # first boolean is for x flip and second id for y
            screen.blit(flip_pipe, pipe)


def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            return False
    if bird_rect.top <= -50 or bird_rect.bottom >= 450:
        death_sound.play()
        return False
    return True


def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement*5, 1)  # rotozoom can rotate and zoom as well
    return new_bird


def score_display(game_state):
    if game_state == "main_game":
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))  # True enables Antialiasing
        score_rect = score_surface.get_rect(center=(144, 50))
        screen.blit(score_surface, score_rect)
    if game_state == "game_over":
        score_surface = game_font.render("Score: "+str(int(score)), True, (255, 255, 255))  # True enables Antialiasing
        score_rect = score_surface.get_rect(center=(144, 50))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render("High score: "+str(int(high_score)), True, (255, 255, 255))  # True enables Antialiasing
        high_score_rect = high_score_surface.get_rect(center=(144, 400))
        screen.blit(high_score_surface, high_score_rect)


pygame.mixer.pre_init(frequency=44100, size=16, channels=1, buffer=512)
pygame.init()
screen = pygame.display.set_mode((288, 512))  # this creates our game canvas
clock = pygame.time.Clock()
game_font = pygame.font.Font("04B_19.ttf", 30)

# Game variables
gravity = 0.25
bird_movement = 0
game_active = True
score = 0
high_score = 0

bg_surface = pygame.image.load("assets/background-day.png").convert()  # convert helps game run at consistent speed
# bg_surface = pygame.transform.scale2x(bg_surface) scales our surface to twice size

floor_surface = pygame.image.load("assets/base.png").convert()
floor_x_position = 0

bird_downflap = pygame.image.load("assets/bluebird-downflap.png").convert_alpha()  # convert_alpha preserves transparency
bird_downflap = pygame.transform.rotozoom(bird_downflap, 0, 0.75)

bird_midflap = pygame.image.load("assets/bluebird-midflap.png").convert_alpha()  # convert_alpha preserves transparency
bird_midflap = pygame.transform.rotozoom(bird_midflap, 0, 0.75)

bird_upflap = pygame.image.load("assets/bluebird-upflap.png").convert_alpha()  # convert_alpha preserves transparency
bird_upflap = pygame.transform.rotozoom(bird_upflap, 0, 0.75)

bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(50, 156))

BIRDFLAP = pygame.USEREVENT + 1  # new userevents have to be different
pygame.time .set_timer(BIRDFLAP, 200)


pipe_surface = pygame.image.load("assets/pipe-green.png").convert()
pipe_list = []
SPAWNPIPE = pygame.USEREVENT  # timer
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [200, 300, 400]

game_over_surface = pygame.image.load("assets/message.png").convert_alpha()
game_over_rect = game_over_surface.get_rect(center=(144, 226))

flap_sound = pygame.mixer.Sound("sound/sfx_wing.wav")
death_sound = pygame.mixer.Sound("sound/sfx_hit.wav")
score_sound = pygame.mixer.Sound("sound/sfx_point.wav")
score_sound_counter = 100

while True:  # game loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # quit logic
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement = -6
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active is False:
                game_active = True
                pipe_list = []
                bird_rect.center = (50, 156)
                bird_movement = 0
                score = 0
                score_sound_counter = 100

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())  # since we get back tuples we need to use extend to unpack them

        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
    screen.blit(bg_surface, (0, 0))  # we are using top left corner and placing at (0,0)

    if game_active:
        # Bird
        bird_movement += gravity
        bird_surface = bird_frames[bird_index]
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement  # centery can only move vertically
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list)

        # Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        score += 0.01
        score_sound_counter -= 1
        if score_sound_counter == 0:
            score_sound.play()
            score_sound_counter = 100
        if score >= high_score:
            high_score = score
        score_display("main_game")

    else:
        score_display("game_over")
        screen.blit(game_over_surface, game_over_rect)

    # Floor
    floor_x_position -= 3
    draw_floor()
    if floor_x_position <= -283:
        floor_x_position = 0


    pygame.display.update()
    clock.tick(120)  # fps limiter
