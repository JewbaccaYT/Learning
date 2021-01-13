import pygame
import random
import math
# Previously was pygame.init() which caused issues with launching and only the font was needed
pygame.font.init()

# Defines Class of Moving Circles (Delay between one disappearing and another being created)
class Circle:
    def __init__(self, delay=40):
        self.speed = [random.randint(0, 20) / 10, random.randint(0, 20) / 10]
        self.color = (129, 7, 7)
        self.rad = random.randint(8, 26)
        self.pos = [random.randint(100, screen_size[0] - 100), random.randint(100, screen_size[1] - 100)]
        self.delay = delay
    def DrawCircle(self):
        if not self.delay == 0:
            self.delay -= 1
        if self.delay == 0:
            pygame.draw.circle(screen, self.color, (int(self.pos[0]), int(self.pos[1])), self.rad)
    def Movement(self):
        self.pos[0] += self.speed[0]
        self.pos[1] += self.speed[1]
        if self.pos[0] >= (screen_size[0] - self.rad) or self.pos[0] <= self.rad:
            self.speed[0] = -self.speed[0]
        if self.pos[1] >= (screen_size[1] - self.rad) or self.pos[1] <= self.rad:
            self.speed[1] = -self.speed[1]

# Function to determine hitbox
def Distance(circle_x, circle_y, circle_rad, mouse_x, mouse_y):
    return math.sqrt((circle_x - mouse_x)** 2 + (circle_y - mouse_y)** 2) <= circle_rad

# Defines Starting Variables
screen_size = (1600, 900)
points = 0
font = pygame.font.SysFont("Star Jedi", 36)
screen = pygame.display.set_mode(screen_size, pygame.DOUBLEBUF)
clock = pygame.time.Clock()
circles = []
remove_circs = []
circ_while = True
circ_number = random.randint(2, 8)
while circ_while:
    circles.append(Circle(0))
    if len(circles) > circ_number:
        circ_while = False

game_running = True
# Main Game Loop with immediate checks for mouse clicks
while game_running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for circle_click in circles:
                if Distance(circle_click.pos[0], circle_click.pos[1], circle_click.rad, event.pos[0], event.pos[1]):
                    remove_circs.append(circle_click)
    # Circle Removal and Respawn/Point Addition. Constantly removes circles in remove_circle list and adds new circle to
    # Circles list. Adds 10 to point counter for every circle clicked on.
    for needs_remove in remove_circs:
        if needs_remove in circles:
            circles.remove(needs_remove)
            points += 10
            circles.append(Circle())
    # Creates the circles added to the Circles list and calls the class functions.
    for circle_inlist in circles:
        circle_inlist.DrawCircle()
        circle_inlist.Movement()

    text = font.render(str(points), True, (226, 219, 14))
    screen.blit(text, text.get_rect(center = (800, 800)))
    pygame.display.update()
    pygame.display.set_caption(str(clock.get_fps()))
    clock.tick(150)