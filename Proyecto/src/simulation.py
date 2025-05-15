import pygame
import sys
from physics import Physics
from bow import Bow
from arrow import Arrow
import pygame_textinput


class Simulation:
    """Clase principal que maneja la simulación y controles"""

    def __init__(self):
        """Inicializa la simulación y sus componentes"""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.running = True
        self.fps = 60
        self.dt = 1 / self.fps

        # Configuración física
        self.physics = Physics(gravity=9.8)

        # Configuración de la simulación
        self.ground_y = 500
        self.bow = Bow(50, 20)
        self.arrow = Arrow(50, 20, self.physics)
        # Ajustado para que el arco esté en (0,0) en la cuadrícula
        self.camera_offset_x = 50
        self.camera_offset_y = 0
        self.scale = 1.0

        # Estado de la simulación
        self.show_trajectory = True
        self.show_info = True
        self.show_grid = True
        self.active_input = None

        # Valores límite
        self.max_velocity = 100
        self.max_angle = 90
        self.min_angle = 0

        # Configuración de entrada de texto
        self.angle_input = pygame_textinput.TextInputVisualizer(
            font_color=(0, 0, 0),
            cursor_color=(0, 0, 0),
            font_object=pygame.font.SysFont('arial', 20)
        )
        self.velocity_input = pygame_textinput.TextInputVisualizer(
            font_color=(0, 0, 0),
            cursor_color=(0, 0, 0),
            font_object=pygame.font.SysFont('arial', 20)
        )

        # Ajustar valores iniciales
        self.angle_input.value = str(self.bow.angle)
        self.velocity_input.value = str(self.bow.draw_strength)

        # Distancia máxima registrada y estimación teórica
        self.max_distance = 0
        self.estimated_distance = self.physics.max_horizontal_distance(
            self.bow.draw_strength, self.bow.angle)
        # Calcular los márgenes de error (±2%)
        self.error_margin = 0.02 * self.estimated_distance
        self.min_expected = self.estimated_distance * (1 - 0.02)
        self.max_expected = self.estimated_distance * (1 + 0.02)
        self.last_arrow_x = 0

        # Para la sensibilidad reducida
        self.angle_sensitivity = 0.5  # Grados por pulsación
        self.velocity_sensitivity = 0.2  # Unidades por pulsación

        # Posición de la regla de altura
        self.height_ruler_x = 50

    def handle_events(self):
        """Procesa los eventos de entrada del usuario"""
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if self.active_input is None:  # Si no hay campo de texto activo
                    if event.key == pygame.K_SPACE:
                        if not self.arrow.is_flying:
                            self.arrow = Arrow(50, 20, self.physics)
                            self.arrow.shoot(self.bow.draw_strength, self.bow.angle)
                    elif event.key == pygame.K_r:
                        self.arrow = Arrow(50, 20, self.physics)
                        # No resetear camera_offset_x para mantener el origen fijo
                        self.max_distance = 0
                    elif event.key == pygame.K_g:
                        current_gravity = self.physics.gravity
                        if current_gravity == 9.8:  # Tierra
                            self.physics.set_gravity(1.62)  # Luna
                        elif current_gravity == 1.62:  # Luna
                            self.physics.set_gravity(3.7)  # Marte
                        else:
                            self.physics.set_gravity(9.8)  # Volver a Tierra
                        # Actualizar la estimación con la nueva gravedad
                        self.estimated_distance = self.physics.max_horizontal_distance(
                            self.bow.draw_strength, self.bow.angle)
                elif event.key == pygame.K_RETURN:
                    # Confirmar la edición
                    if self.active_input == "angle":
                        try:
                            angle = float(self.angle_input.value)
                            self.bow.set_angle(angle)
                            # Actualizar la estimación
                            self.estimated_distance = self.physics.max_horizontal_distance(
                                self.bow.draw_strength, self.bow.angle)
                        except ValueError:
                            # Restaurar valor anterior si es inválido
                            self.angle_input.value = str(round(self.bow.angle, 1))
                    elif self.active_input == "velocity":
                        try:
                            velocity = float(self.velocity_input.value)
                            self.bow.set_strength(velocity)
                            # Actualizar la estimación
                            self.estimated_distance = self.physics.max_horizontal_distance(
                                self.bow.draw_strength, self.bow.angle)
                        except ValueError:
                            # Restaurar valor anterior si es inválido
                            self.velocity_input.value = str(round(self.bow.draw_strength, 1))
                    self.active_input = None
                elif event.key == pygame.K_ESCAPE:
                    # Cancelar la edición
                    if self.active_input == "angle":
                        self.angle_input.value = str(round(self.bow.angle, 1))
                    elif self.active_input == "velocity":
                        self.velocity_input.value = str(round(self.bow.draw_strength, 1))
                    self.active_input = None

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Verificar si se hizo clic en los campos de entrada
                angle_rect = pygame.Rect(120, 20, 60, 30)
                velocity_rect = pygame.Rect(120, 60, 60, 30)

                if angle_rect.collidepoint(event.pos):
                    self.active_input = "angle"
                elif velocity_rect.collidepoint(event.pos):
                    self.active_input = "velocity"
                else:
                    self.active_input = None

        # Actualizar campos de texto activos
        if self.active_input == "angle":
            self.angle_input.update(events)
        elif self.active_input == "velocity":
            self.velocity_input.update(events)

        # Controles cuando no hay campos de texto activos
        if self.active_input is None:
            keys = pygame.key.get_pressed()

            if keys[pygame.K_UP]:
                self.bow.adjust_angle(self.angle_sensitivity)
                self.angle_input.value = str(round(self.bow.angle, 1))
                # Actualizar la estimación de distancia
                self.estimated_distance = self.physics.max_horizontal_distance(
                    self.bow.draw_strength, self.bow.angle)
                # Recalcular los márgenes
                self.update_error_margins()
            if keys[pygame.K_DOWN]:
                self.bow.adjust_angle(-self.angle_sensitivity)
                self.angle_input.value = str(round(self.bow.angle, 1))
                # Actualizar la estimación de distancia
                self.estimated_distance = self.physics.max_horizontal_distance(
                    self.bow.draw_strength, self.bow.angle)
                # Recalcular los márgenes
                self.update_error_margins()
            if keys[pygame.K_PLUS] or keys[pygame.K_KP_PLUS]:
                self.bow.adjust_strength(self.velocity_sensitivity)
                self.velocity_input.value = str(round(self.bow.draw_strength, 1))
                # Actualizar la estimación de distancia
                self.estimated_distance = self.physics.max_horizontal_distance(
                    self.bow.draw_strength, self.bow.angle)
                # Recalcular los márgenes
                self.update_error_margins()
            if keys[pygame.K_MINUS] or keys[pygame.K_KP_MINUS]:
                self.bow.adjust_strength(-self.velocity_sensitivity)
                self.velocity_input.value = str(round(self.bow.draw_strength, 1))
                # Actualizar la estimación de distancia
                self.estimated_distance = self.physics.max_horizontal_distance(
                    self.bow.draw_strength, self.bow.angle)
                # Recalcular los márgenes
                self.update_error_margins()

    def update_error_margins(self):
        """Actualiza los márgenes de error basados en la estimación actual"""
        self.error_margin = 0.02 * self.estimated_distance
        self.min_expected = self.estimated_distance * (1 - 0.02)
        self.max_expected = self.estimated_distance * (1 + 0.02)

    def update(self):
        """Actualiza el estado de la simulación"""
        self.arrow.update(self.dt)

        # Actualizar distancia máxima sin modificar la cámara
        if self.arrow.is_flying:
            self.last_arrow_x = self.arrow.x
            if self.last_arrow_x > self.max_distance:
                self.max_distance = self.last_arrow_x

    def run(self, renderer):
        """Ejecuta el bucle principal de la simulación"""
        while self.running:
            self.handle_events()
            self.update()

            # Dibujar todos los elementos
            renderer.clear_screen()

            # Dibujar cuadrícula si está habilitada
            if self.show_grid:
                renderer.draw_grid(self.scale, self.camera_offset_x, self.ground_y)

            # Dibujar regla de altura
            renderer.draw_height_ruler(self.height_ruler_x, self.scale, self.ground_y)

            renderer.draw_info_panel(self.bow.angle, self.bow.draw_strength,
                                     self.physics.gravity, self.arrow.is_flying,
                                     self.max_distance, self.estimated_distance,
                                     self.min_expected, self.max_expected)
            renderer.draw_formulas_panel(self.bow.angle, self.bow.draw_strength,
                                         self.physics.gravity, self.arrow.is_flying,
                                         self.max_distance)
            renderer.draw_distance_ruler(self.ground_y + 30, self.scale, self.camera_offset_x)
            renderer.draw_ground(self.ground_y, self.scale)
            self.bow.draw(renderer.screen, self.ground_y)
            self.arrow.draw(renderer.screen, self.camera_offset_x, self.camera_offset_y,
                            self.scale, self.ground_y)

            # Dibujar campos de entrada de texto
            if self.active_input == "angle":
                angle_surface = self.angle_input.surface
                renderer.screen.blit(angle_surface, (120, 20))
                pygame.draw.rect(renderer.screen, (0, 0, 255), (120, 20, 60, 30), 2)
            else:
                angle_text = pygame.font.SysFont('arial', 20).render(str(round(self.bow.angle, 1)), True, (0, 0, 0))
                renderer.screen.blit(angle_text, (120, 20))
                pygame.draw.rect(renderer.screen, (200, 200, 200), (120, 20, 60, 30), 1)

            if self.active_input == "velocity":
                velocity_surface = self.velocity_input.surface
                renderer.screen.blit(velocity_surface, (120, 60))
                pygame.draw.rect(renderer.screen, (0, 0, 255), (120, 60, 60, 30), 2)
            else:
                velocity_text = pygame.font.SysFont('arial', 20).render(str(round(self.bow.draw_strength, 1)), True,
                                                                        (0, 0, 0))
                renderer.screen.blit(velocity_text, (120, 60))
                pygame.draw.rect(renderer.screen, (200, 200, 200), (120, 60, 60, 30), 1)

            pygame.display.flip()
            self.clock.tick(self.fps)

        pygame.quit()
        sys.exit()