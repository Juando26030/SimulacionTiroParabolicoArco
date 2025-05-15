import math


class Physics:
    """Clase que contiene todas las fórmulas físicas para el tiro parabólico"""

    def __init__(self, gravity=9.81):
        """Inicializa la clase Physics con un valor predeterminado para la gravedad"""
        self.gravity = gravity

    def set_gravity(self, gravity):
        """Permite cambiar el valor de la gravedad"""
        self.gravity = gravity

    def horizontal_position(self, initial_velocity, angle, time):
        """Calcula la posición horizontal en función del tiempo
        x(t) = v0x * t = v0 * cos(θ) * t
        """
        return initial_velocity * math.cos(math.radians(angle)) * time

    def vertical_position(self, initial_velocity, angle, time):
        """Calcula la posición vertical en función del tiempo
        y(t) = v0y * t - (1/2)g * t^2 = v0 * sin(θ) * t - (1/2)g * t^2
        """
        return (initial_velocity * math.sin(math.radians(angle)) * time) - \
            (0.5 * self.gravity * time ** 2)

    def max_horizontal_distance(self, initial_velocity, angle):
        """Calcula el alcance horizontal máximo
        R = (v0^2 * sin(2θ)) / g
        """
        return (initial_velocity ** 2 * math.sin(math.radians(2 * angle))) / self.gravity

    def max_height(self, initial_velocity, angle):
        """Calcula la altura máxima
        H = (v0^2 * sin^2(θ)) / (2g)
        """
        return (initial_velocity ** 2 * math.sin(math.radians(angle)) ** 2) / (2 * self.gravity)

    def flight_time(self, initial_velocity, angle):
        """Calcula el tiempo de vuelo
        T = (2 * v0 * sin(θ)) / g
        """
        return (2 * initial_velocity * math.sin(math.radians(angle))) / self.gravity

    def current_velocity_x(self, initial_velocity, angle):
        """Calcula la componente horizontal de la velocidad (constante)"""
        return initial_velocity * math.cos(math.radians(angle))

    def current_velocity_y(self, initial_velocity, angle, time):
        """Calcula la componente vertical de la velocidad en un tiempo dado
        vy(t) = v0y - g*t = v0*sin(θ) - g*t
        """
        return initial_velocity * math.sin(math.radians(angle)) - self.gravity * time