import pygame
from config import *
from player import Player
from obstacle import Obstacle
from scores import load_top_scores, save_score

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Player Game")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 80)

# Create a player object
player = Player(WIDTH - 150, HEIGHT - 70)  # Bottom right
player2 = Player(100, HEIGHT - 70, PLAYER_COLOR2, 2)  # Second player, bottom left

obstacles = []  # List to store obstacles

last_obstacle_spawn_time = pygame.time.get_ticks()  # Track the last time an obstacle was spawned

score = 0
high_score = 0  # Reto 9: best score during this execution
game_over = False
paused = False  # Reto 4

# Reto 12: start screen, name input and best scores from scores.txt
start_screen = True
entering_name = False
player_name = ""
top_scores = load_top_scores()

# Reto 6: survival timer
start_time = pygame.time.get_ticks()
pause_start_time = 0
paused_total = 0  # Total milliseconds spent paused
survival_time = 0  # Milliseconds survived


def draw_centered_text(text, text_font, y):
    """Draw a white text horizontally centered at height y"""
    image = text_font.render(text, True, (255, 255, 255))
    screen.blit(image, image.get_rect(center=(WIDTH // 2, y)))


def draw_top_scores(y):
    """Reto 12: draw the best scores, from highest to lowest"""
    draw_centered_text("TOP 5", font, y)
    if not top_scores:
        draw_centered_text("No scores yet", font, y + 40)
    for position, (name, points) in enumerate(top_scores, start=1):
        draw_centered_text(f"{position}. {name}  {points}", font, y + 40 * position)


# GAME loop
running = True
while running:
    current_time = pygame.time.get_ticks()

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            # Reto 12: start screen, SPACE starts the game
            if start_screen:
                if event.key == pygame.K_SPACE:
                    start_screen = False
                    start_time = current_time
                    last_obstacle_spawn_time = current_time

            # Reto 12: type the name after Game Over
            elif entering_name:
                if event.key == pygame.K_RETURN:
                    if player_name.strip() != "":
                        save_score(player_name.strip(), score)
                        top_scores = load_top_scores()
                        entering_name = False
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                elif (event.unicode.isprintable() and event.unicode != ""
                      and event.unicode != ";" and len(player_name) < MAX_NAME_LENGTH):
                    player_name += event.unicode

            # Reto 4: pause / resume with ESC
            elif event.key == pygame.K_ESCAPE and not game_over:
                paused = not paused
                if paused:
                    pause_start_time = current_time
                else:
                    pause_duration = current_time - pause_start_time
                    paused_total += pause_duration
                    last_obstacle_spawn_time += pause_duration
                    # Reto 10: the invulnerability does not run out during the pause
                    player.invulnerable_until += pause_duration
                    player2.invulnerable_until += pause_duration

            # Reto 5: restart with R after Game Over
            elif event.key == pygame.K_r and game_over:
                score = 0
                obstacles = []
                player.reset()
                player2.reset()
                game_over = False
                start_time = current_time
                paused_total = 0
                survival_time = 0
                last_obstacle_spawn_time = current_time

            # Reto 8: change the first player's speed with + and -
            elif event.unicode == "+" or event.key == pygame.K_KP_PLUS:
                player.change_speed(1)
            elif event.unicode == "-" or event.key == pygame.K_KP_MINUS:
                player.change_speed(-1)

    if not start_screen and not game_over and not paused:
        # Reto 6: update survival time
        survival_time = current_time - start_time - paused_total

        # Reto 7: spawn faster every 10 points, never below the minimum
        spawn_delay = max(MIN_SPAWN_OBSTACLE_DELAY,
                          SPAWN_OBSTACLE_DELAY - (score // 10) * SPAWN_DELAY_STEP)

        # OBSTACLES spawning logic
        if current_time - last_obstacle_spawn_time > spawn_delay:
            obstacles.append(Obstacle())
            last_obstacle_spawn_time = current_time

        # Update the position of each obstacle
        for obstacle in obstacles:
            obstacle.move()

        # Remove obstacles that are off the screen (1 point for each dodged obstacle)
        visible_obstacles = []
        for obstacle in obstacles:
            if not obstacle.is_off_screen():
                visible_obstacles.append(obstacle)
            else:
                score += 1
        obstacles = visible_obstacles

        # Reto 9: update the high score
        if score > high_score:
            high_score = score

        # Update the player's position (Reto 10: only players with lives)
        if player.is_alive():
            player.moveArrows()
        if player2.is_alive():
            player2.moveWASD()  # Update the second player's position

        # Reto 10: a hit takes one life, unless the player is invulnerable
        for p in (player, player2):
            if p.is_alive() and not p.is_invulnerable(current_time):
                for obstacle in obstacles:
                    if p.rect.colliderect(obstacle.rect):
                        p.hit(current_time)
                        break

        # Reto 10: the game ends when both players have no lives
        if not player.is_alive() and not player2.is_alive():
            game_over = True
            entering_name = True  # Reto 12: ask for the name
            player_name = ""

    screen.fill(BACKGROUND_COLOR)  # Black background

    if start_screen:
        # Reto 12: start screen with the best scores
        draw_centered_text("DODGE THE OBSTACLES", big_font, 100)
        draw_top_scores(200)
        draw_centered_text("Press SPACE to start", font, HEIGHT - 80)
        pygame.display.flip()
        clock.tick(FPS)
        continue

    if player.is_alive():
        player.draw(screen)  # Draw the player rectangle
    if player2.is_alive():
        player2.draw(screen)  # Draw the second player rectangle

    for obstacle in obstacles:
        obstacle.draw(screen)  # Draw each obstacle

    # Score, high score (Reto 9) and survival time (Reto 6)
    hud = f"Score: {score}   High score: {high_score}   Time: {survival_time // 1000}s"
    screen.blit(font.render(hud, True, (255, 255, 255)), (10, 10))

    # Reto 10: lives of each player
    lives_text = f"Lives  P1: {player.lives}   P2: {player2.lives}"
    screen.blit(font.render(lives_text, True, (255, 255, 255)), (10, 45))

    if paused:
        draw_centered_text("PAUSE", big_font, HEIGHT // 2)

    if game_over:
        draw_centered_text("GAME OVER", big_font, 130)
        if entering_name:
            # Reto 12: name input
            draw_centered_text("Enter your name and press ENTER:", font, 220)
            draw_centered_text(player_name + "_", font, 270)
        else:
            draw_top_scores(200)
            draw_centered_text("Press R to restart", font, HEIGHT - 60)

    pygame.display.flip()
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
