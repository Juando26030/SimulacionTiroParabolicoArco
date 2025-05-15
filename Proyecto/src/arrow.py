import math
import pygame

class Arrow:
    """Clase que representa la flecha y su comportamiento"""

    def __init__(self, x, y, physics):
        """Inicializa la flecha en una posición con acceso a las fórmulas físicas"""
        self.x = x
        self.y = y
        self.physics = physics
        self.initial_velocity = 0
        self.angle = 0
        self.time = 0
        self.is_flying = False
        self.trajectory_points = []
        self.max_points = 200  # Aumentado para mostrar más puntos de la trayectoria

        # Posición inicial para la trayectoria (arco)
        self.initial_x = x
        self.initial_y = y

        # Cargar imagen de la flecha
        self.image = pygame.Surface((30, 5))
        self.image.fill((139, 69, 19))  # Color marrón para la flecha
        self.rect = self.image.get_rect()

    def shoot(self, initial_velocity, angle):
        """Dispara la flecha con una velocidad inicial y ángulo dados"""
        self.initial_velocity = initial_velocity
        self.angle = angle
        self.time = 0
        self.is_flying = True
        # Iniciar trayectoria desde la posición del arco
        self.trajectory_points = [(self.initial_x, self.initial_y)]

    def update(self, dt):
        """Actualiza la posición de la flecha según las ecuaciones de movimiento"""
        if not self.is_flying:
            return

        self.time += dt

        # Calcular la posición usando las fórmulas físicas
        self.x = self.physics.horizontal_position(self.initial_velocity, self.angle, self.time)
        # Ya no necesitamos restar 50m porque ahora la cuadrícula está ajustada
        self.y = self.physics.vertical_position(self.initial_velocity, self.angle, self.time)

        # Actualizar la trayectoria
        self.trajectory_points.append((self.x, self.y))

        # Calcular la rotación de la flecha basado en su velocidad actual
        vx = self.physics.current_velocity_x(self.initial_velocity, self.angle)
        vy = self.physics.current_velocity_y(self.initial_velocity, self.angle, self.time)

        # Calcular el ángulo de la flecha en radianes y convertir a grados
        self.rotation = math.degrees(math.atan2(vy, vx))

        # Verificar si la flecha ha tocado el suelo
        if self.y <= 0:
            self.is_flying = False


    def draw(self, screen, camera_offset_x, camera_offset_y, scale, ground_y):
        """Dibuja la flecha y su trayectoria"""
        # Convertir las posiciones físicas a coordenadas de pantalla
        screen_x = self.x * scale + camera_offset_x
        screen_y = ground_y - self.y * scale  # Invertir coordenada Y

        # Solo dibujar si está dentro de la pantalla
        if 0 <= screen_x < screen.get_width() and 0 <= screen_y < screen.get_height():
            # Dibujar la flecha según su estado
            if self.is_flying:
                # Calcular velocidades actuales
                vx = self.physics.current_velocity_x(self.initial_velocity, self.angle)
                vy = self.physics.current_velocity_y(self.initial_velocity, self.angle, self.time)

                # Calcular el ángulo de la flecha basado en su velocidad
                angle = math.degrees(math.atan2(-vy, vx))  # Negativo porque pygame Y aumenta hacia abajo

                # Dibujar flecha rotada
                arrow_length = 20  # longitud de la flecha en píxeles

                # Calcular puntas de flecha
                arrow_head_x = screen_x + arrow_length * math.cos(math.radians(angle))
                arrow_head_y = screen_y + arrow_length * math.sin(math.radians(angle))

                # Dibujar línea principal
                pygame.draw.line(screen, (0, 0, 0), (screen_x, screen_y), (arrow_head_x, arrow_head_y), 3)

                # Dibujar puntas triangulares (corregido)
                pygame.draw.polygon(screen, (0, 0, 0), [
                    (arrow_head_x, arrow_head_y),
                    (arrow_head_x - 10 * math.cos(math.radians(angle - 20)),
                     arrow_head_y - 10 * math.sin(math.radians(angle - 20))),
                    (arrow_head_x - 5 * math.cos(math.radians(angle)),
                     arrow_head_y - 5 * math.sin(math.radians(angle))),
                    (arrow_head_x - 10 * math.cos(math.radians(angle + 20)),
                     arrow_head_y - 10 * math.sin(math.radians(angle + 20)))
                ])
            else:
                # Dibujar flecha en reposo
                pygame.draw.circle(screen, (100, 100, 100), (int(screen_x), int(screen_y)), 5)

            # Dibujar trayectoria - modificado para eliminar la línea inicial
            if len(self.trajectory_points) > 2:  # Aseguramos que haya suficientes puntos
                # Omitir el primer punto (posición del arco) para evitar la línea diagonal
                puntos_trayectoria = self.trajectory_points[1:]

                # Dividir la trayectoria en ascendente y descendente
                max_height_idx = 0
                max_height = puntos_trayectoria[0][1]

                for i in range(len(puntos_trayectoria)):
                    if puntos_trayectoria[i][1] > max_height:
                        max_height = puntos_trayectoria[i][1]
                        max_height_idx = i

                # Convertir puntos de trayectoria a coordenadas de pantalla
                screen_points = []
                for point in puntos_trayectoria:
                    px = point[0] * scale + camera_offset_x
                    py = ground_y - point[1] * scale  # Invertir coordenada Y
                    screen_points.append((px, py))

                # Dibujar parte ascendente (rojo)
                if max_height_idx > 0:
                    pygame.draw.lines(screen, (255, 0, 0), False, screen_points[:max_height_idx + 1], 2)

                # Dibujar parte descendente (azul)
                if max_height_idx < len(screen_points) - 1:
                    pygame.draw.lines(screen, (0, 0, 255), False, screen_points[max_height_idx:], 2)