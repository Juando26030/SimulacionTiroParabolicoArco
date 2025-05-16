import pygame
import math


class Renderer:
    """Clase para manejar la visualización de la simulación"""

    def __init__(self):
        """Inicializa el renderizador y configura la pantalla"""
        self.screen_width = 1200
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Simulación de Tiro con Arco - Física")

        # Colores
        self.bg_color = (135, 206, 235)  # Celeste
        self.ground_color = (34, 139, 34)  # Verde oscuro
        self.panel_color = (240, 240, 240)  # Gris claro
        self.text_color = (0, 0, 0)  # Negro
        self.formula_color = (10, 10, 80)  # Azul oscuro para fórmulas
        self.grid_color = (180, 180, 180)  # Gris para la cuadrícula

        # Fuente
        self.font = pygame.font.SysFont('arial', 16)
        self.title_font = pygame.font.SysFont('arial', 20, bold=True)
        self.formula_font = pygame.font.SysFont('arial', 14)  # Fuente para fórmulas

    def clear_screen(self):
        """Limpia la pantalla con el color de fondo"""
        self.screen.fill(self.bg_color)

    def draw_grid(self, scale, camera_offset_x, ground_y):
        """Dibuja una cuadrícula de fondo para ayudar a visualizar distancias"""
        # Definir color blanco para las líneas de la cuadrícula
        grid_color = (255, 255, 255)

        # Calcular el máximo valor X necesario para cubrir toda la pantalla
        max_x = int((self.screen_width - camera_offset_x) / scale) + 100  # Añadir margen

        # Dibujar líneas verticales cada 50 metros para todo el ancho visible
        for x in range(50, max_x + 50, 50):
            # Calcular posición con compensación de cámara
            screen_x = int(x * scale + camera_offset_x)  # Convertir a entero para evitar imprecisiones

            # Si está dentro de la pantalla
            if 0 <= screen_x < self.screen_width:
                pygame.draw.line(self.screen, grid_color,
                                 (screen_x, 0),
                                 (screen_x, ground_y), 1)

                # Añadir etiquetas en la parte inferior
                font = pygame.font.SysFont('Arial', 12)
                label = font.render(f"{x}m", True, (255, 255, 255))
                self.screen.blit(label, (screen_x - 15, ground_y - 20))

    def draw_ground(self, ground_y, scale):
        """Dibuja el suelo con textura mejorada y marcas de medición"""
        # Dibujar el suelo base
        pygame.draw.rect(self.screen, self.ground_color,
                         (0, ground_y, self.screen_width, self.screen_height - ground_y))

        # Añadir marcas de distancia en el suelo (cada 10 metros)
        for i in range(0, self.screen_width, 10):
            # Cada 10 metros una línea corta
            line_height = 5
            color = (45, 150, 45)  # Verde claro

            # Cada 50 metros una línea más larga
            if i % 50 == 0:
                line_height = 15
                color = (25, 100, 25)  # Verde más oscuro

                # ELIMINADA la parte que generaba las etiquetas

            # Cada 100 metros una línea aún más grande
            if i % 100 == 0:
                line_height = 25
                color = (20, 80, 20)  # Verde más oscuro

            pygame.draw.line(self.screen, color,
                             (i, ground_y),
                             (i, ground_y + line_height), 1)

    def draw_info_panel(self, angle, velocity, gravity, is_flying, max_distance, estimated_distance, min_expected, max_expected):
        """Dibuja el panel de información con los parámetros actuales"""
        # Panel ampliado para incluir la predicción y rango
        panel_rect = pygame.Rect(10, 10, 200, 240)
        pygame.draw.rect(self.screen, self.panel_color, panel_rect)
        pygame.draw.rect(self.screen, (100, 100, 100), panel_rect, 2)

        # Título del panel
        title = self.title_font.render("Parámetros", True, self.text_color)
        self.screen.blit(title, (15, 15))

        # Etiquetas
        angle_label = self.font.render("Ángulo:", True, self.text_color)
        self.screen.blit(angle_label, (15, 50))

        velocity_label = self.font.render("Velocidad:", True, self.text_color)
        self.screen.blit(velocity_label, (15, 80))

        gravity_label = self.font.render(f"Gravedad: {gravity} m/s²", True, self.text_color)
        self.screen.blit(gravity_label, (15, 110))

        status = "En vuelo" if is_flying else "Listo"
        status_label = self.font.render(f"Estado: {status}", True, self.text_color)
        self.screen.blit(status_label, (15, 140))

        # Mostrar predicción con rango
        prediction_label = self.font.render(f"Predicción: {estimated_distance:.2f} m", True, (0, 0, 255))
        self.screen.blit(prediction_label, (15, 170))

        # Nuevo - Mostrar rango de error esperado
        range_label = self.font.render(f"Rango: [{min_expected:.2f}-{max_expected:.2f}]", True, (0, 100, 0))
        self.screen.blit(range_label, (15, 200))

        # Mostrar distancia real alcanzada
        distance_label = self.font.render(f"Dist. máx: {max_distance:.2f} m", True, (255, 0, 0))
        self.screen.blit(distance_label, (15, 230))

        # Indicaciones de control
        controls = self.font.render("↑/↓: Ángulo | +/-: Velocidad | Espacio: Disparar", True, self.text_color)
        self.screen.blit(controls, (250, 15))

    def draw_formulas_panel(self, angle, velocity, gravity, is_flying, max_distance):
        // hola
        """Dibuja panel con fórmulas físicas y resultados calculados"""
        # Ubicar el panel a la derecha del panel de parámetros - EXTENDIDO
        panel_rect = pygame.Rect(220, 10, 950, 240)
        pygame.draw.rect(self.screen, self.panel_color, panel_rect)
        pygame.draw.rect(self.screen, (100, 100, 100), panel_rect, 2)

        # Título del panel
        title = self.title_font.render("Fórmulas Físicas", True, self.text_color)
        self.screen.blit(title, (230, 15))

        # Convertir valores para fórmulas
        v0 = velocity
        theta = angle
        g = gravity
        sin_theta = round(math.sin(math.radians(theta)), 3)
        cos_theta = round(math.cos(math.radians(theta)), 3)
        sin_2theta = round(math.sin(math.radians(2 * theta)), 3)

        # Calcular resultados
        vel_x = round(v0 * cos_theta, 3)
        vel_y = round(v0 * sin_theta, 3)
        tiempo_vuelo = round((2 * v0 * sin_theta) / g, 3)
        alcance = round((v0 ** 2 * sin_2theta) / g, 3)
        altura_max = round((v0 ** 2 * sin_theta ** 2) / (2 * g), 3)

        # Colores para variables y conclusiones
        variable_color = (0, 128, 0)  # Verde para variables
        formula_color = self.formula_color
        conclusion_color = (0, 0, 139)  # Azul rey para conclusiones

        # Posición y espaciado
        y = 50
        spacing = 30
        column_width = 260  # Ancho de columna

        # 1. DESCOMPOSICIÓN DE VELOCIDAD INICIAL - Fundamental
        # Velocidad horizontal
        formula_symbolic = self.formula_font.render("Velocidad horizontal: v_x = v0·cos(θ)", True, formula_color)
        self.screen.blit(formula_symbolic, (230, y))

        formula1 = self.formula_font.render("v_x = ", True, formula_color)
        formula2 = self.formula_font.render(f"{v0}", True, variable_color)
        formula3 = self.formula_font.render("·", True, formula_color)
        formula4 = self.formula_font.render(f"{cos_theta}", True, variable_color)
        formula5 = self.formula_font.render(" = ", True, formula_color)
        formula6 = self.formula_font.render(f"{vel_x}", True, variable_color)
        formula7 = self.formula_font.render(" m/s", True, formula_color)

        x_pos = 230 + column_width
        self.screen.blit(formula1, (x_pos, y))
        x_pos += formula1.get_width()
        self.screen.blit(formula2, (x_pos, y))
        x_pos += formula2.get_width()
        self.screen.blit(formula3, (x_pos, y))
        x_pos += formula3.get_width()
        self.screen.blit(formula4, (x_pos, y))
        x_pos += formula4.get_width()
        self.screen.blit(formula5, (x_pos, y))
        x_pos += formula5.get_width()
        self.screen.blit(formula6, (x_pos, y))
        x_pos += formula6.get_width()
        self.screen.blit(formula7, (x_pos, y))

        conclusion = self.formula_font.render(f"Componente constante durante todo el movimiento", True,
                                              conclusion_color)
        self.screen.blit(conclusion, (230 + 2 * column_width, y))
        y += spacing

        # Velocidad vertical
        formula_symbolic = self.formula_font.render("Velocidad vertical: v_y = v0·sin(θ)", True, formula_color)
        self.screen.blit(formula_symbolic, (230, y))

        formula1 = self.formula_font.render("v_y = ", True, formula_color)
        formula2 = self.formula_font.render(f"{v0}", True, variable_color)
        formula3 = self.formula_font.render("·", True, formula_color)
        formula4 = self.formula_font.render(f"{sin_theta}", True, variable_color)
        formula5 = self.formula_font.render(" = ", True, formula_color)
        formula6 = self.formula_font.render(f"{vel_y}", True, variable_color)
        formula7 = self.formula_font.render(" m/s", True, formula_color)

        x_pos = 230 + column_width
        self.screen.blit(formula1, (x_pos, y))
        x_pos += formula1.get_width()
        self.screen.blit(formula2, (x_pos, y))
        x_pos += formula2.get_width()
        self.screen.blit(formula3, (x_pos, y))
        x_pos += formula3.get_width()
        self.screen.blit(formula4, (x_pos, y))
        x_pos += formula4.get_width()
        self.screen.blit(formula5, (x_pos, y))
        x_pos += formula5.get_width()
        self.screen.blit(formula6, (x_pos, y))
        x_pos += formula6.get_width()
        self.screen.blit(formula7, (x_pos, y))

        conclusion = self.formula_font.render(f"Disminuye con el tiempo debido a la gravedad", True, conclusion_color)
        self.screen.blit(conclusion, (230 + 2 * column_width, y))
        y += spacing

        # 2. ECUACIONES DE MOVIMIENTO - Usando las componentes de velocidad
        formula_symbolic = self.formula_font.render("Posición x(t): x = v_x·t = v0·cos(θ)·t", True, formula_color)
        self.screen.blit(formula_symbolic, (230, y))

        formula1 = self.formula_font.render("x = ", True, formula_color)
        formula2 = self.formula_font.render(f"{vel_x}", True, variable_color)
        formula3 = self.formula_font.render("·t = ", True, formula_color)
        formula4 = self.formula_font.render(f"{v0}", True, variable_color)
        formula5 = self.formula_font.render("·", True, formula_color)
        formula6 = self.formula_font.render(f"{cos_theta}", True, variable_color)
        formula7 = self.formula_font.render("·t", True, formula_color)

        x_pos = 230 + column_width
        self.screen.blit(formula1, (x_pos, y))
        x_pos += formula1.get_width()
        self.screen.blit(formula2, (x_pos, y))
        x_pos += formula2.get_width()
        self.screen.blit(formula3, (x_pos, y))
        x_pos += formula3.get_width()
        self.screen.blit(formula4, (x_pos, y))
        x_pos += formula4.get_width()
        self.screen.blit(formula5, (x_pos, y))
        x_pos += formula5.get_width()
        self.screen.blit(formula6, (x_pos, y))
        x_pos += formula6.get_width()
        self.screen.blit(formula7, (x_pos, y))

        conclusion = self.formula_font.render(f"Movimiento horizontal uniforme", True, conclusion_color)
        self.screen.blit(conclusion, (230 + 2 * column_width, y))
        y += spacing

        formula_symbolic = self.formula_font.render("Posición y(t): y = v_y·t - ½g·t² = v0·sin(θ)·t - ½g·t²", True,
                                                    formula_color)
        self.screen.blit(formula_symbolic, (230, y))

        formula1 = self.formula_font.render("y = ", True, formula_color)
        formula2 = self.formula_font.render(f"{vel_y}", True, variable_color)
        formula3 = self.formula_font.render("·t - 0.5·", True, formula_color)
        formula4 = self.formula_font.render(f"{g}", True, variable_color)
        formula5 = self.formula_font.render("·t²", True, formula_color)

        x_pos = 230 + column_width
        self.screen.blit(formula1, (x_pos, y))
        x_pos += formula1.get_width()
        self.screen.blit(formula2, (x_pos, y))
        x_pos += formula2.get_width()
        self.screen.blit(formula3, (x_pos, y))
        x_pos += formula3.get_width()
        self.screen.blit(formula4, (x_pos, y))
        x_pos += formula4.get_width()
        self.screen.blit(formula5, (x_pos, y))

        conclusion = self.formula_font.render(f"Caída libre afectada por la gravedad", True, conclusion_color)
        self.screen.blit(conclusion, (230 + 2 * column_width, y))
        y += spacing

        # 3. TIEMPO DE VUELO - A partir de y(t) cuando y=0
        formula_symbolic = self.formula_font.render("Tiempo vuelo T = (2·v_y)/g = (2·v0·sin(θ))/g", True, formula_color)
        self.screen.blit(formula_symbolic, (230, y))

        formula1 = self.formula_font.render("T = (2·", True, formula_color)
        formula2 = self.formula_font.render(f"{vel_y}", True, variable_color)
        formula3 = self.formula_font.render(")/", True, formula_color)
        formula4 = self.formula_font.render(f"{g}", True, variable_color)
        formula5 = self.formula_font.render(" = ", True, formula_color)
        formula6 = self.formula_font.render(f"{tiempo_vuelo}", True, variable_color)
        formula7 = self.formula_font.render(" s", True, formula_color)

        x_pos = 230 + column_width
        self.screen.blit(formula1, (x_pos, y))
        x_pos += formula1.get_width()
        self.screen.blit(formula2, (x_pos, y))
        x_pos += formula2.get_width()
        self.screen.blit(formula3, (x_pos, y))
        x_pos += formula3.get_width()
        self.screen.blit(formula4, (x_pos, y))
        x_pos += formula4.get_width()
        self.screen.blit(formula5, (x_pos, y))
        x_pos += formula5.get_width()
        self.screen.blit(formula6, (x_pos, y))
        x_pos += formula6.get_width()
        self.screen.blit(formula7, (x_pos, y))

        conclusion = self.formula_font.render(f"Tiempo total en el aire: {tiempo_vuelo} s", True, conclusion_color)
        self.screen.blit(conclusion, (230 + 2 * column_width, y))
        y += spacing

        # 4. ALCANCE HORIZONTAL - Usando x(T)
        formula_symbolic = self.formula_font.render("Alcance R = v_x·T = (v0²·sin(2θ))/g", True, formula_color)
        self.screen.blit(formula_symbolic, (230, y))

        formula1 = self.formula_font.render("R = ", True, formula_color)
        formula2 = self.formula_font.render(f"{vel_x}", True, variable_color)
        formula3 = self.formula_font.render("·", True, formula_color)
        formula4 = self.formula_font.render(f"{tiempo_vuelo}", True, variable_color)
        formula5 = self.formula_font.render(" = ", True, formula_color)
        formula6 = self.formula_font.render(f"{alcance}", True, variable_color)
        formula7 = self.formula_font.render(" m", True, formula_color)

        x_pos = 230 + column_width
        self.screen.blit(formula1, (x_pos, y))
        x_pos += formula1.get_width()
        self.screen.blit(formula2, (x_pos, y))
        x_pos += formula2.get_width()
        self.screen.blit(formula3, (x_pos, y))
        x_pos += formula3.get_width()
        self.screen.blit(formula4, (x_pos, y))
        x_pos += formula4.get_width()
        self.screen.blit(formula5, (x_pos, y))
        x_pos += formula5.get_width()
        self.screen.blit(formula6, (x_pos, y))
        x_pos += formula6.get_width()
        self.screen.blit(formula7, (x_pos, y))

        conclusion = self.formula_font.render(f"Distancia horizontal máxima: {alcance} m", True, conclusion_color)
        self.screen.blit(conclusion, (230 + 2 * column_width, y))
        y += spacing

        # 5. ALTURA MÁXIMA - Cuando v_y = 0
        formula_symbolic = self.formula_font.render("Altura máx. H = v_y²/(2g) = (v0²·sin²(θ))/(2g)", True,
                                                    formula_color)
        self.screen.blit(formula_symbolic, (230, y))

        formula1 = self.formula_font.render("H = ", True, formula_color)
        formula2 = self.formula_font.render(f"{vel_y}", True, variable_color)
        formula3 = self.formula_font.render("²/(2·", True, formula_color)
        formula4 = self.formula_font.render(f"{g}", True, variable_color)
        formula5 = self.formula_font.render(") = ", True, formula_color)
        formula6 = self.formula_font.render(f"{altura_max}", True, variable_color)
        formula7 = self.formula_font.render(" m", True, formula_color)

        x_pos = 230 + column_width
        self.screen.blit(formula1, (x_pos, y))
        x_pos += formula1.get_width()
        self.screen.blit(formula2, (x_pos, y))
        x_pos += formula2.get_width()
        self.screen.blit(formula3, (x_pos, y))
        x_pos += formula3.get_width()
        self.screen.blit(formula4, (x_pos, y))
        x_pos += formula4.get_width()
        self.screen.blit(formula5, (x_pos, y))
        x_pos += formula5.get_width()
        self.screen.blit(formula6, (x_pos, y))
        x_pos += formula6.get_width()
        self.screen.blit(formula7, (x_pos, y))

        conclusion = self.formula_font.render(f"Punto más alto de la trayectoria: {altura_max} m", True,
                                              conclusion_color)
        self.screen.blit(conclusion, (230 + 2 * column_width, y))
        y += spacing

        # Explicación sobre margen de error
        y += 10
        explain = self.formula_font.render("La diferencia entre predicción y distancia real se debe a:", True,
                                           (100, 0, 0))
        self.screen.blit(explain, (230, y))
        y += 25

        reasons = [
            "• Discretización del tiempo (Δt = 1/60 s)",
            "• Acumulación de errores de redondeo",
            "• Limitaciones en la representación gráfica"
        ]

        for reason in reasons:
            self.screen.blit(self.formula_font.render(reason, True, (100, 0, 0)), (240, y))
            y += 20

    def draw_distance_ruler(self, y_pos, scale, camera_offset_x):
        """Dibuja una regla en la parte inferior para mostrar la distancia"""
        ruler_height = 20
        tick_height = 10
        offset = 50  # Desplazamiento de 50m

        # Dibujar la línea base de la regla
        pygame.draw.rect(self.screen, (50, 50, 50),
                         (0, y_pos, self.screen_width, ruler_height))

        # Dibujar las marcas de la regla
        for i in range(0, 1001, 10):  # Marcas cada 10 metros, hasta 1000m
            # Calcular posición con compensación de cámara
            x_pos = i * scale + camera_offset_x

            # Si está dentro de la pantalla
            if 0 <= x_pos < self.screen_width:
                # Marca principal cada 100 metros
                if i % 100 == 0:
                    pygame.draw.line(self.screen, (255, 255, 255),
                                     (x_pos, y_pos),
                                     (x_pos, y_pos + tick_height * 2), 2)
                    # Se elimina la etiqueta de distancia
                # Marca secundaria cada 50 metros
                elif i % 50 == 0:
                    pygame.draw.line(self.screen, (255, 255, 255),
                                     (x_pos, y_pos),
                                     (x_pos, y_pos + int(tick_height * 1.5)), 1)
                # Marcas pequeñas cada 10 metros
                else:
                    pygame.draw.line(self.screen, (200, 200, 200),
                                     (x_pos, y_pos),
                                     (x_pos, y_pos + tick_height), 1)


    def draw_height_ruler(self, x_pos, scale, ground_y):
        """Dibuja una regla vertical para mostrar la altura"""
        ruler_width = 20
        tick_width = 10

        # Dibujar la línea base de la regla
        pygame.draw.rect(self.screen, (50, 50, 50),
                         (x_pos, 0, ruler_width, ground_y))

        # Dibujar las marcas de la regla cada 10 metros
        for i in range(0, ground_y, 10):
            # Si está dentro de la pantalla
            if i < ground_y:
                # Marca principal cada 50 metros
                if i % 50 == 0:
                    pygame.draw.line(self.screen, (255, 255, 255),
                                     (x_pos, ground_y - i),
                                     (x_pos + tick_width * 2, ground_y - i), 2)

                    # Etiqueta de altura
                    height_text = self.font.render(f"{i}m", True, (255, 255, 255))
                    self.screen.blit(height_text, (x_pos + tick_width * 2 + 5, ground_y - i - 10))
                else:
                    # Marcas intermedias
                    pygame.draw.line(self.screen, (200, 200, 200),
                                     (x_pos, ground_y - i),
                                     (x_pos + tick_width, ground_y - i), 1)