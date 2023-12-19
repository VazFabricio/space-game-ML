import pygame
import random
from Plataform import Platform  # Importa a classe Platform
from Ship import Ship  # Importa a classe Ship


def initialize_game():
    # Inicializa o Pygame e define as dimensões da janela do jogo
    pygame.init()
    display_width = 800
    display_height = 600
    game_display = pygame.display.set_mode((display_width, display_height))
    clock = pygame.time.Clock()
    return display_width, display_height, game_display, clock


def load_images():
    # Carrega as texturas para a nave, plataformas e fundo do jogo
    texture_ship = pygame.image.load("spaceship.png").convert_alpha()
    texture_ship = pygame.transform.scale(texture_ship, (50, 50))

    texture_platform = pygame.image.load("comet.png").convert_alpha()
    texture_platform = pygame.transform.scale(texture_platform, (30, 80))

    texture_background = pygame.image.load("fundo2.png").convert()
    texture_background = pygame.transform.scale(texture_background, (800, 600))

    return texture_ship, texture_platform, texture_background


def handle_events():
    # Lida com os eventos do jogo, como teclas pressionadas e fechamento da janela
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


def draw_collision_line(game_display, ship, platform):
    # Desenha a linha de colisão expandida entre a nave e a plataforma
    expanded_ship_rect = pygame.Rect(ship.x - 20, ship.y - 20, ship.width + 40, ship.height + 40)
    ship_center = (
        expanded_ship_rect.x + expanded_ship_rect.width // 2, expanded_ship_rect.y + expanded_ship_rect.height // 2)

    platform_center = (platform.rect.x + platform.rect.width // 2, platform.rect.y + platform.rect.height // 2)

    pygame.draw.line(game_display, (255, 0, 0), ship_center, platform_center, 2)


def main():
    global MOVING_LEFT, MOVING_RIGHT, MOVING_UP, MOVING_DOWN

    # Inicializa o jogo e carrega as texturas
    display_width, display_height, game_display, clock = initialize_game()
    texture_ship, texture_platform, texture_background = load_images()

    # Inicializa a nave e as variáveis do jogo
    ship = Ship(400, 300, 50, 50, 10, 10)
    NUMBER_OF_COLLISIONS = 0
    SPEED = 0
    platforms = []
    distances_to_platforms = []

    running = True
    while running:
        running = handle_events()  # Lida com os eventos do jogo

        # Move a nave de acordo com as teclas pressionadas
        if MOVING_LEFT:
            ship.move_left()
        if MOVING_RIGHT:
            ship.move_right(display_width)
        if MOVING_UP:
            ship.move_up()
        if MOVING_DOWN:
            ship.move_down(display_height)

        game_display.blit(texture_background, (0, 0))  # Define o fundo do jogo

        for platform in platforms:
            # Move e desenha as plataformas
            platform.move()
            platform.draw(game_display, texture_platform)

            # Verifica colisões entre a nave e as plataformas
            if platform.check_collision(pygame.Rect(ship.x, ship.y, ship.width, ship.height)):
                NUMBER_OF_COLLISIONS += 1
                SPEED += 0
                platform.speed = SPEED * 1.5
                platforms.remove(platform)
                break

            # Remove plataformas que saíram da tela
            if platform.rect.y > display_height:
                platforms.remove(platform)

            # Calcula a distância entre a nave e a plataforma
            distance = ship.calcular_distancia_visao(platform.rect)

            # Verifica se a distância atende ao critério desejado (por exemplo, distância < 200)
            if distance < 200:
                print(f"Distância para plataforma: {distance}")

            # Chama a função para desenhar a linha de colisão expandida
            draw_collision_line(game_display, ship, platform)

        # Cria novas plataformas quando necessário
        while len(platforms) < 5:
            new_platform = Platform(random.randrange(0, 800), -20, SPEED)
            platforms.append(new_platform)

        # Calcula a distância da nave em relação às bordas da tela
        distances_to_edges = ship.calcular_distancia_borda(display_width, display_height)

        ship.draw(game_display, texture_ship)  # Desenha a nave

        pygame.display.update()  # Atualiza a tela
        clock.tick(60)  # Controla a taxa de frames por segundo

        # Finaliza o jogo após 10 colisões
        if NUMBER_OF_COLLISIONS == 10:
            pygame.quit()
            quit()

    pygame.quit()
    quit()


if __name__ == "__main__":
    MOVING_LEFT = MOVING_RIGHT = MOVING_UP = MOVING_DOWN = False
    main()
