import pygame
import sys
from simulation import Simulation
from renderer import Renderer


def main():
    """Función principal que inicia la simulación de tiro con arco"""
    # Inicializar pygame
    pygame.init()

    # Crear instancias de las clases principales
    simulation = Simulation()
    renderer = Renderer()

    # Ejecutar la simulación
    simulation.run(renderer)

    # Salir limpiamente cuando termine
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()