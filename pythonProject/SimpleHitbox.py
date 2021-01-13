import math
import pygame
import pygame.gfxdraw

# Initially Define Variable
screen_size = (1600, 900)
circ_radius = int(screen_size[0] / 12)
circle_pos = [int(screen_size[0] / 2), int(screen_size[1] / 2)]
enemy_circle_radius = int(screen_size[0] / 12)
enemy_circle_pos = [450, 626]
enemy_circ_bounds = (100, 1500)
enemy_circ_bounds_y = (100, 800)
enemy_x_speed = 1
enemy_y_speed = 4

# Set Window and Tickrate
screen = pygame.display.set_mode(screen_size, pygame.DOUBLEBUF)
clock = pygame.time.Clock()

# Controls     Up    Down   Left  Right  SizeInc.W  SizeDec.S
key_states = [False, False, False, False, False, False]

# Main Game Loop
running = True

while running:
    screen.fill((0, 0, 0))
    # Comp Circle Movement
    enemy_circle_pos[0] += enemy_x_speed
    enemy_circle_pos[1] += enemy_y_speed
    if enemy_circle_pos[0] >= enemy_circ_bounds[1]:
        enemy_x_speed = -2
    elif enemy_circle_pos[0] <= enemy_circ_bounds[0]:
        enemy_x_speed = 2
    if enemy_circle_pos[1] >= enemy_circ_bounds_y[1]:
        enemy_y_speed = -2
    elif enemy_circle_pos[1] <= enemy_circ_bounds_y[0]:
        enemy_y_speed = 2
    # Key Hold/Release Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                key_states[4] = False
            if event.key == pygame.K_s:
                key_states[5] = False
            if event.key == pygame.K_UP:
                key_states[0] = False
            if event.key == pygame.K_DOWN:
                key_states[1] = False
            if event.key == pygame.K_LEFT:
                key_states[2] = False
            if event.key == pygame.K_RIGHT:
                key_states[3] = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                key_states[4] = True
            if event.key == pygame.K_s:
                key_states[5] = True
            if event.key == pygame.K_UP:
                key_states[0] = True
            if event.key == pygame.K_DOWN:
                key_states[1] = True
            if event.key == pygame.K_RIGHT:
                key_states[3] = True
            if event.key == pygame.K_LEFT:
                key_states[2] = True
            # Reset Size of Player Circle
            if event.key == pygame.K_SPACE:
                circle_pos = [int(screen_size[0] / 2), int(screen_size[1] / 2)]
                circ_radius = int(screen_size[0] / 8)
    # Controls Assignment
    if key_states[0]:
        circle_pos[1] -= 5
    if key_states[1]:
        circle_pos[1] += 5
    if key_states[2]:
        circle_pos[0] -= 5
    if key_states[3]:
        circle_pos[0] += 5
    if key_states[4]:
        circ_radius += 1
    if key_states[5]:
        circ_radius -= 1
        if circ_radius < 2:
            circ_radius = 2
    # Circle Hitbox Detection Based on Distance Between Radii
    distance = math.sqrt((enemy_circle_pos[0] - circle_pos[0])**2 + (enemy_circle_pos[1] - circle_pos[1])**2)
    if distance <= circ_radius + enemy_circle_radius:
        circle_color = (0, 255, 0)
    else:
        circle_color = (255, 0, 0)
    pygame.draw.circle(screen, (32, 164, 252), enemy_circle_pos, enemy_circle_radius)
    pygame.gfxdraw.filled_circle(screen, circle_pos[0], circle_pos[1], circ_radius, circle_color)
    # pygame.draw.circle(screen, (255, 0, 0), circle_pos, circ_radius)
    pygame.display.update()
    pygame.display.set_caption(str(clock.get_fps()))
    clock.tick(1000)