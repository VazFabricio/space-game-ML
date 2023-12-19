import math
import pygame


class Ship:

    def __init__(self, x, y, width, height, sensor_length, max_vision_distance):
        self.angle = 0
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.sensor_length = sensor_length
        self.max_vision_distance = max_vision_distance

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
        # pygame.draw.rect(display, (0, 255, 0), ship_rect, 2) # 2 é a largura da linha
        display.blit(texture, (self.x, self.y))

    def calcular_distancia_visao(self, platform_rect):
        ship_center = (self.x + self.width // 2, self.y + self.height // 2)
        platform_center = (platform_rect.x + platform_rect.width // 2, platform_rect.y + platform_rect.height // 2)

        distance = math.sqrt((ship_center[0] - platform_center[0]) ** 2 + (ship_center[1] - platform_center[1]) ** 2)
        return distance

    def calcular_distancia_borda(self, display_width, display_height):
        # Calcula a distância da nave até as bordas da tela
        distancia_esquerda = self.x
        distancia_direita = display_width - (self.x + self.width)
        distancia_topo = self.y
        distancia_base = display_height - (self.y + self.height)

        # Retorna um vetor representando a distância até as bordas (esquerda, direita, topo, base)
        return [distancia_esquerda, distancia_direita, distancia_topo, distancia_base]
