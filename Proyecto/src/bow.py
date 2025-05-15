import pygame
import math


class Bow:
    """Clase que representa el arco con gráficos mejorados"""

    def __init__(self, x, y):
        """Inicializa el arco en una posición específica"""
        self.x = x
        self.y = y
        self.angle = 45  # Ángulo inicial (grados)
        self.draw_strength = 50  # Velocidad inicial de la flecha

        # Cargar y escalar la imagen del arco
        try:
            self.original_image = pygame.image.load('assets/bow.png')
            self.image = pygame.transform.scale(self.original_image, (60, 120))
        except:
            # Crear una imagen del arco si no se puede cargar
            self.create_bow_image()

        self.rect = self.image.get_rect()

    def create_bow_image(self):
        """Crea una imagen suavizada del arco usando curvas"""
        self.original_image = pygame.Surface((60, 120), pygame.SRCALPHA)

        # Colores para el arco
        wood_color = (139, 69, 19)  # Marrón
        string_color = (220, 220, 220)  # Blanco apagado

        # Dibujar el arco con antialiasing
        pygame.draw.arc(self.original_image, wood_color, (5, 0, 50, 120),
                        math.pi / 2 - 0.5, math.pi / 2 + 0.5, 8)

        # Suavizar bordes del arco
        for i in range(2):
            pygame.draw.arc(self.original_image,
                            (139 + i * 20, 69 + i * 10, 19 + i * 10, 200),
                            (5 + i, 0, 50 - i * 2, 120),
                            math.pi / 2 - 0.5, math.pi / 2 + 0.5, 8 - i * 2)

        # Dibujar la cuerda del arco
        pygame.draw.line(self.original_image, string_color, (10, 10), (10, 110), 2)

        self.image = self.original_image

    def adjust_angle(self, delta):
        """Ajusta el ángulo de disparo"""
        self.angle += delta
        self.angle = max(0, min(90, self.angle))  # Limitar entre 0 y 90 grados

    def adjust_strength(self, delta):
        """Ajusta la fuerza de tensado (velocidad inicial)"""
        self.draw_strength += delta
        self.draw_strength = max(10, min(100, self.draw_strength))

    def set_angle(self, angle):
        """Establece un ángulo específico"""
        self.angle = max(0, min(90, angle))

    def set_strength(self, strength):
        """Establece una fuerza específica"""
        self.draw_strength = max(10, min(100, strength))

    def draw(self, screen, ground_y):
        """Dibuja el arco rotado según el ángulo"""
        # CORRECCIÓN: Cambiar el signo para que coincida con la dirección adecuada
        rotated_bow = pygame.transform.rotate(self.image, self.angle)
        bow_rect = rotated_bow.get_rect()
        bow_rect.center = (self.x, ground_y - self.y)
        screen.blit(rotated_bow, bow_rect)

        # Dibujar la cuerda tensada
        string_length = 40
        string_end_x = self.x + string_length * math.cos(math.radians(self.angle))
        string_end_y = ground_y - self.y - string_length * math.sin(math.radians(self.angle))
        pygame.draw.line(screen, (220, 220, 220), (self.x, ground_y - self.y),
                         (string_end_x, string_end_y), 2)