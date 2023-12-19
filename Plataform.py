import pygame


class Platform:
    def __init__(self, x, y, speed):
        self.rect = pygame.Rect(x, y, 30, 80)
        self.speed = speed

    def move(self):
        self.rect.y += self.speed

    def draw(self, display, texture):
        # Desenha a hitbox (retângulo)
        # pygame.draw.rect(display, (255, 0, 0), self.rect, 2)  # 2 é a largura da linha
        display.blit(texture, self.rect)

    def check_collision(self, ship_rect):
        return self.rect.colliderect(ship_rect)

