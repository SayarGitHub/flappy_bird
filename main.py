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
            return False
    if bird_rect.top <= -50 or bird_rect.bottom >= 450:
        return False
    return True


pygame.init()
screen = pygame.display.set_mode((288, 512))  # this creates our game canvas
clock = pygame.time.Clock()

# Game variables
gravity = 0.25
bird_movement = 0
game_active = True

bg_surface = pygame.image.load("assets/background-day.png").convert()  # convert helps game run at consistent speed
# bg_surface = pygame.transform.scale2x(bg_surface) scales our surface to twice size

floor_surface = pygame.image.load("assets/base.png").convert()
floor_x_position = 0

bird_surface = pygame.image.load("assets/bluebird-midflap.png").convert()
bird_rect = bird_surface.get_rect(center=(50, 156))

pipe_surface = pygame.image.load("assets/pipe-green.png").convert()
pipe_list = []
SPAWNPIPE = pygame.USEREVENT  # timer
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [200, 300, 400]


while True:  # game loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # quit logic
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement = -6
            if event.key == pygame.K_SPACE and game_active is False:
                game_active = True
                pipe_list = []
                bird_rect.center = (50, 156)
                bird_movement = 0

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())  # since we get back tuples we need to use extend to unpack them

    screen.blit(bg_surface, (0, 0))  # we are using top left corner and placing at (0,0)

    if game_active:
        # Bird
        bird_movement += gravity
        bird_rect.centery += bird_movement  # centery can only move vertically
        screen.blit(bird_surface, bird_rect)
        game_active = check_collision(pipe_list)

        # Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

    # Floor
    floor_x_position -= 3
    draw_floor()
    if floor_x_position <= -283:
        floor_x_position = 0


    pygame.display.update()
    clock.tick(120)  # fps limiter
