# Simulación de Tiro con Arco - Física

Este proyecto es una simulación interactiva del tiro parabólico aplicado al lanzamiento de una flecha con arco. Demuestra los principios de la física del movimiento parabólico y permite a los usuarios experimentar con diferentes parámetros.

## Requisitos

- Python 3.7 o superior
- Pygame 2.5.0 o superior

## Instalación

1. Clona este repositorio
2. Instala las dependencias: `pip install -r requirements.txt`
3. Ejecuta la aplicación: `python src/main.py`

## Controles

- **Flechas Arriba/Abajo**: Ajustar el ángulo de lanzamiento
- **Teclas +/-**: Ajustar la velocidad inicial
- **Espacio**: Disparar la flecha
- **R**: Reiniciar la simulación
- **G**: Cambiar el valor de la gravedad

## Conceptos Físicos

La simulación implementa las siguientes fórmulas del tiro parabólico:

- Posición horizontal: x(t) = v₀ · cos(θ) · t
- Posición vertical: y(t) = v₀ · sin(θ) · t - (1/2)g · t²
- Alcance máximo: R = (v₀² · sin(2θ))/g
- Altura máxima: H = (v₀² · sin²(θ))/(2g)
- Tiempo de vuelo: T = (2v₀ · sin(θ))/g

## Estructura del Proyecto

- `src/`: Código fuente
  - `physics.py`: Implementación de las fórmulas físicas
  - `bow.py`: Clase que representa el arco
  - `arrow.py`: Clase que representa la flecha
  - `renderer.py`: Visualización con Pygame
  - `simulation.py`: Lógica principal de la simulación
  - `main.py`: Punto de entrada del programa