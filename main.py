import pygame
import random

class Platform:
    def __init__(self, x, y, speed):
        self.rect = pygame.Rect(x, y, 30, 80)
        self.speed = speed

    def move(self):
        self.rect.y += self.speed

    def draw(self, display, texture):
        # Desenha a hitbox (retângulo)
        #pygame.draw.rect(display, (255, 0, 0), self.rect, 2)  # 2 é a largura da linha
        display.blit(texture, self.rect)

    def check_collision(self, ship_rect):
        return self.rect.colliderect(ship_rect)

class Ship:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def move_left(self):
        if self.x > 0:
            self.x -= 5

    def move_right(self, display_width):
        if self.x < display_width - self.width:
            self.x += 5

    def move_up(self):
        if self.y > 0:
            self.y -= 5

    def move_down(self, display_height):
        if self.y < display_height - self.height:
            self.y += 5

    def draw(self, display, texture):
        ship_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        #pygame.draw.rect(display, (0, 255, 0), ship_rect, 2)  # 2 é a largura da linha
        display.blit(texture, (self.x, self.y))

def initialize_game():
    pygame.init()

    display_width = 800
    display_height = 600
    game_display = pygame.display.set_mode((display_width, display_height))
    clock = pygame.time.Clock()

    return display_width, display_height, game_display, clock

def load_images():
    texture_ship = pygame.image.load("spaceship.png").convert_alpha()
    texture_ship = pygame.transform.scale(texture_ship, (50, 50))

    texture_platform = pygame.image.load("comet.png").convert_alpha()
    texture_platform = pygame.transform.scale(texture_platform, (30, 80))

    texture_background = pygame.image.load("fundo2.png").convert()
    texture_background = pygame.transform.scale(texture_background, (800, 600))

    return texture_ship, texture_platform, texture_background

def handle_events():
    global MOVING_LEFT, MOVING_RIGHT, MOVING_UP, MOVING_DOWN

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                MOVING_LEFT = True
            elif event.key == pygame.K_RIGHT:
                MOVING_RIGHT = True
            elif event.key == pygame.K_UP:
                MOVING_UP = True
            elif event.key == pygame.K_DOWN:
                MOVING_DOWN = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                MOVING_LEFT = False
            elif event.key == pygame.K_RIGHT:
                MOVING_RIGHT = False
            elif event.key == pygame.K_UP:
                MOVING_UP = False
            elif event.key == pygame.K_DOWN:
                MOVING_DOWN = False

    return True

def main():
    global MOVING_LEFT, MOVING_RIGHT, MOVING_UP, MOVING_DOWN

    display_width, display_height, game_display, clock = initialize_game()
    texture_ship, texture_platform, texture_background = load_images()

    ship = Ship(0, 0, 50, 50)
    NUMBER_OF_COLLISIONS = 0
    SPEED = 1
    platforms = []

    running = True
    while running:
        running = handle_events()

        if MOVING_LEFT:
            ship.move_left()
        if MOVING_RIGHT:
            ship.move_right(display_width)
        if MOVING_UP:
            ship.move_up()
        if MOVING_DOWN:
            ship.move_down(display_height)

        game_display.blit(texture_background, (0, 0))

        for platform in platforms:
            platform.move()
            platform.draw(game_display, texture_platform)

            if platform.check_collision(pygame.Rect(ship.x, ship.y, ship.width, ship.height)):
                NUMBER_OF_COLLISIONS += 1
                SPEED += 1
                platform.speed = SPEED * 1.5
                platforms.remove(platform)
                break

            if platform.rect.y > display_height:
                platforms.remove(platform)

        while len(platforms) < 5:
            new_platform = Platform(random.randrange(100, 700), -20, SPEED)
            platforms.append(new_platform)

        ship.draw(game_display, texture_ship)

        pygame.display.update()
        clock.tick(60)

        if NUMBER_OF_COLLISIONS == 10:
            pygame.quit()
            quit()

    pygame.quit()
    quit()

if __name__ == "__main__":
    MOVING_LEFT = MOVING_RIGHT = MOVING_UP = MOVING_DOWN = False
    main()
