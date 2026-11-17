# Juego de esquivar obstáculos (Pygame)

Juego para dos jugadores hecho con Pygame. Los dos cuadrados tienen que esquivar los obstáculos rojos que caen desde arriba. Cada jugador tiene 3 vidas y la partida termina cuando los dos se quedan sin vidas.

## Gameplay

<video src="gameplay.mp4" controls width="800"></video>

Si el vídeo no se ve, ábrelo aquí: [gameplay.mp4](gameplay.mp4)

## Cómo ejecutarlo

```bash
pip install pygame
python main.py
```

## Controles

| Tecla | Acción |
|---|---|
| ESPACIO | Empezar la partida desde la pantalla de inicio |
| Flechas | Mover al jugador 1 (azul, abajo a la derecha) |
| W A S D | Mover al jugador 2 (naranja, abajo a la izquierda) |
| `+` / `-` | Subir / bajar la velocidad del jugador 1 |
| ESC | Pausar / continuar |
| Teclado + ENTER | Escribir el nombre y guardar la puntuación tras el Game Over |
| R | Reiniciar tras guardar la puntuación |

## Estructura de archivos

| Archivo | Contenido |
|---|---|
| `config.py` | Constantes: tamaño de la ventana, colores, velocidades, tiempos de aparición, tamaños de los obstáculos, vidas y fichero de récords. |
| `player.py` | Clase `Player`: movimiento, límites de pantalla, cambio de velocidad, vidas, invulnerabilidad y reinicio. |
| `obstacle.py` | Clase `Obstacle`: tamaño, posición y velocidad aleatorios, y movimiento hacia abajo. |
| `scores.py` | Funciones para leer y guardar los récords en `scores.txt`. |
| `main.py` | Crea la ventana, los jugadores y los obstáculos, y ejecuta el bucle del juego (eventos, lógica y dibujo). |
| `scores.txt` | Se crea solo al guardar la primera puntuación. Cada línea es `nombre;puntuación`. |

En cada partida se gana **1 punto por cada obstáculo que sale por abajo sin chocar con nadie**.

---

## Retos

### 1. Player boundaries — Límites de pantalla

**Cómo funciona:** los jugadores no pueden salir de la ventana por ningún lado.

**Cómo se ha hecho:** en `player.py` hay un método `keep_inside_screen()` que usa `clamp_ip()`. Este método mete el rectángulo del jugador dentro de un rectángulo del tamaño de la ventana. Se llama al final de `moveArrows()` y de `moveWASD()`, después de mover al jugador.

```python
def keep_inside_screen(self):
    self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))
```

### 2. Random obstacle sizes — Tamaños aleatorios

**Cómo funciona:** cada obstáculo tiene un tamaño distinto entre 20 y 70 píxeles y siempre aparece entero dentro del ancho de la ventana.

**Cómo se ha hecho:** en `obstacle.py` el tamaño se elige con `random.randint()` entre `OBSTACLE_MIN_SIZE` y `OBSTACLE_MAX_SIZE`, que están en `config.py`. La posición x se elige entre `0` y `WIDTH - size`, así el obstáculo nunca se sale por la derecha.

```python
size = random.randint(OBSTACLE_MIN_SIZE, OBSTACLE_MAX_SIZE)
x = random.randint(0, WIDTH - size)
```

### 3. Collision with Player 2 — Colisión del segundo jugador

**Cómo funciona:** la partida termina si un obstáculo toca a cualquiera de los dos jugadores.

**Cómo se ha hecho:** en `main.py` se recorren los obstáculos y se comprueba con `colliderect()` si chocan con el jugador 1 **o** con el jugador 2. Si choca con alguno, `game_over` pasa a `True`.

```python
for obstacle in obstacles:
    if player.rect.colliderect(obstacle.rect) or player2.rect.colliderect(obstacle.rect):
        game_over = True
        break
```

> Con el reto 10 esta comprobación se ha cambiado: ahora un choque con cualquiera de los dos jugadores le quita una vida en lugar de terminar la partida.

### 4. Pause game — Pausar el juego

**Cómo funciona:** al pulsar ESC el juego se para y aparece **PAUSE**. Al pulsar ESC otra vez, continúa. Mientras está en pausa los jugadores no se mueven, los obstáculos no caen y no aparecen obstáculos nuevos.

**Cómo se ha hecho:** hay una variable `paused` que cambia de valor con cada pulsación de ESC (`paused = not paused`). Toda la lógica del juego (mover, crear obstáculos, colisiones) está dentro de `if not game_over and not paused:`, así que en pausa no se ejecuta. Lo que sí se sigue haciendo es dibujar, y si `paused` es `True` se muestra el texto PAUSE.

Al salir de la pausa se suma el tiempo que ha durado a `last_obstacle_spawn_time`. Así no aparece un obstáculo de golpe nada más continuar.

### 5. Restart game — Reiniciar la partida

**Cómo funciona:** cuando aparece Game Over, al pulsar R empieza una partida nueva sin cerrar el programa. La puntuación vuelve a 0, desaparecen los obstáculos y los jugadores vuelven a su posición inicial.

**Cómo se ha hecho:** cada `Player` guarda su posición inicial (`start_x`, `start_y`) al crearse, y el método `reset()` lo devuelve a ella. En `main.py`, al pulsar R con `game_over` activado:

```python
score = 0
obstacles = []
player.reset()
player2.reset()
game_over = False
start_time = current_time
paused_total = 0
survival_time = 0
last_obstacle_spawn_time = current_time
```

### 6. Survival timer — Tiempo de supervivencia

**Cómo funciona:** arriba se muestran los segundos que llevan sobreviviendo los jugadores. El contador se para en Game Over y no avanza durante la pausa.

**Cómo se ha hecho:** con `pygame.time.get_ticks()`, que da los milisegundos desde que arrancó el programa.
- `start_time` guarda el momento en que empezó la partida.
- `paused_total` acumula los milisegundos que se ha estado en pausa.
- El tiempo sobrevivido es `current_time - start_time - paused_total`.

Este cálculo solo se hace dentro de `if not game_over and not paused:`, así que en pausa y en Game Over el valor se queda congelado. En pantalla se muestra en segundos (`survival_time // 1000`).

### 7. Increasing difficulty — Dificultad progresiva

**Cómo funciona:** cada 10 puntos los obstáculos aparecen más a menudo. El intervalo baja 50 ms cada vez, pero nunca baja de 150 ms.

**Cómo se ha hecho:** en cada vuelta del bucle se calcula el intervalo a partir de la puntuación. `score // 10` dice cuántas veces se han conseguido 10 puntos, y `max()` evita bajar del mínimo.

```python
spawn_delay = max(MIN_SPAWN_OBSTACLE_DELAY,
                  SPAWN_OBSTACLE_DELAY - (score // 10) * SPAWN_DELAY_STEP)
```

Con los valores de `config.py` (500, 50 y 150): 0 puntos → 500 ms, 10 puntos → 450 ms, 20 puntos → 400 ms… y desde 70 puntos se queda en 150 ms.

### 8. Change player speed — Cambiar velocidad

**Cómo funciona:** el jugador 1 sube su velocidad con `+` y la baja con `-`. La velocidad mínima es 2 y la máxima 12. Cada pulsación cambia la velocidad una sola vez.

**Cómo se ha hecho:** se usa el evento `KEYDOWN`, que solo ocurre una vez cada vez que se pulsa la tecla, aunque se mantenga apretada. Se acepta tanto el carácter `+` / `-` del teclado normal como las teclas del teclado numérico. El método `change_speed()` de `Player` limita el valor con `max()` y `min()`:

```python
def change_speed(self, amount):
    self.speed = max(PLAYER_MIN_SPEED, min(PLAYER_MAX_SPEED, self.speed + amount))
```

### 9. High score — Récord de puntuación

**Cómo funciona:** se muestra el mejor resultado conseguido mientras el programa está abierto, junto a la puntuación actual. Al reiniciar, la puntuación vuelve a 0 pero el récord se mantiene.

**Cómo se ha hecho:** la variable `high_score` se crea una sola vez, antes del bucle. Cada vez que `score` la supera, se actualiza. Al pulsar R solo se pone a 0 `score`, no `high_score`.

```python
if score > high_score:
    high_score = score
```

---

## Retos adicionales

### 10. Lives system — Sistema de vidas

**Cómo funciona:** cada jugador empieza con 3 vidas, que se ven arriba (`Lives  P1: 3   P2: 3`). Cuando un obstáculo le golpea, pierde una vida en lugar de terminar la partida. Después del golpe tiene 2 segundos de invulnerabilidad, así un mismo obstáculo no le quita varias vidas. Si un jugador se queda sin vidas desaparece y el otro sigue jugando solo. La partida termina cuando los dos se quedan sin vidas.

**Cómo se ha hecho:** en `config.py` están `PLAYER_LIVES = 3` y `INVULNERABLE_TIME = 2000` (ms). Cada `Player` guarda sus vidas (`lives`) y el momento en que termina su invulnerabilidad (`invulnerable_until`):

```python
def is_alive(self):
    return self.lives > 0

def is_invulnerable(self, current_time):
    return current_time < self.invulnerable_until

def hit(self, current_time):
    self.lives -= 1
    self.invulnerable_until = current_time + INVULNERABLE_TIME
```

En `main.py`, a cada jugador vivo y no invulnerable que choca con un obstáculo se le quita una vida. Cuando ninguno de los dos está vivo, empieza el Game Over:

```python
for p in (player, player2):
    if p.is_alive() and not p.is_invulnerable(current_time):
        for obstacle in obstacles:
            if p.rect.colliderect(obstacle.rect):
                p.hit(current_time)
                break

if not player.is_alive() and not player2.is_alive():
    game_over = True
```

Detalles:
- Un jugador sin vidas no se mueve ni se dibuja.
- Al salir de la pausa se suma el tiempo pausado a `invulnerable_until`, así la invulnerabilidad no se gasta mientras el juego está parado.
- Al reiniciar con R, `reset()` devuelve las 3 vidas a cada jugador.

### 12. Save high scores — Guardar récords en fichero

**Cómo funciona:**
- **Al abrir el juego:** aparece una pantalla de inicio con las 5 mejores puntuaciones de `scores.txt`, de mayor a menor. Con ESPACIO empieza la partida.
- **Al terminar la partida:** se pide el nombre del jugador dentro de la propia ventana del juego. Se escribe con el teclado, se borra con Backspace y se guarda con ENTER (máximo 12 caracteres, no puede estar vacío).
- **Después de guardar:** se ve el top 5 actualizado y se puede pulsar R para jugar otra vez.

**Cómo se ha hecho:** la lectura y la escritura del fichero están en `scores.py`. Cada línea del fichero es `nombre;puntuación`.

- `save_score(name, points)` abre el fichero en modo `"a"` (añadir) y escribe una línea nueva.
- `load_top_scores()` lee todas las líneas, las ordena de mayor a menor puntuación y devuelve las 5 primeras. Si el fichero aún no existe, devuelve una lista vacía.

```python
scores.sort(key=lambda item: item[1], reverse=True)
return scores[:TOP_SCORES]
```

En `main.py` hay dos variables nuevas que controlan en qué pantalla está el juego:
- `start_screen`: está activa al abrir el juego y se desactiva con ESPACIO.
- `entering_name`: se activa al llegar al Game Over.

El nombre se va formando con los eventos `KEYDOWN`:

```python
if event.key == pygame.K_RETURN:
    if player_name.strip() != "":
        save_score(player_name.strip(), score)
        top_scores = load_top_scores()
        entering_name = False
elif event.key == pygame.K_BACKSPACE:
    player_name = player_name[:-1]
elif event.unicode.isprintable() and ... and len(player_name) < MAX_NAME_LENGTH:
    player_name += event.unicode
```

Mientras se escribe el nombre, las teclas solo sirven para escribir. Por eso pulsar R mete una "r" en el nombre y no reinicia. El carácter `;` no se admite porque es el separador del fichero.

El "High score" de arriba (reto 9) sigue empezando en 0 en cada ejecución. Los récords guardados se ven en el top 5.
