import pygame
import sys
import random

pygame.init()

# Paramètres de base du jeu
screen_width = 600
screen_height = 400
game_window = pygame.display.set_mode((screen_width, screen_height))

# Couleurs
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)

# Fréquence d'actualisation
clock = pygame.time.Clock()
snake_speed = 15

# Initialisation du serpent
snake_pos = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]

# Types de nourriture avec leurs couleurs et effets
food_types = {
    'speed_up': {'color': pygame.Color(255, 50, 50), 'speed_change': 5},
    'slow_down': {'color': pygame.Color(50, 255, 50), 'speed_change': -3}
}

# Choisir un type de nourriture aléatoirement et initialiser sa position
food_type = random.choice(list(food_types.keys()))
food_pos = [random.randrange(1, (screen_width//10)) * 10, random.randrange(1, (screen_height//10)) * 10]
food_spawn = True

direction = 'RIGHT'
change_to = direction

# Boucle principale du jeu
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != 'DOWN':
                direction = 'UP'
            if event.key == pygame.K_DOWN and direction != 'UP':
                direction = 'DOWN'
            if event.key == pygame.K_LEFT and direction != 'RIGHT':
                direction = 'LEFT'
            if event.key == pygame.K_RIGHT and direction != 'LEFT':
                direction = 'RIGHT'

    # Mouvement du serpent
    if direction == 'UP':
        snake_pos[1] -= 10
    if direction == 'DOWN':
        snake_pos[1] += 10
    if direction == 'LEFT':
        snake_pos[0] -= 10
    if direction == 'RIGHT':
        snake_pos[0] += 10

    # Croissance du serpent
    snake_body.insert(0, list(snake_pos))
    if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
        food_spawn = False
        # Appliquer l'effet de la nourriture
        snake_speed += food_types[food_type]['speed_change']
        # Assurer que la vitesse du serpent ne devient pas trop lente ou trop rapide
        snake_speed = max(5, min(30, snake_speed))
    else:
        snake_body.pop()

    if not food_spawn:
        food_type = random.choice(list(food_types.keys()))
        food_pos = [random.randrange(1, (screen_width//10)) * 10, random.randrange(1, (screen_height//10)) * 10]
    food_spawn = True

    # Affichage
    game_window.fill(black)
    for pos in snake_body:
        pygame.draw.rect(game_window, white, pygame.Rect(pos[0], pos[1], 10, 10))
    pygame.draw.rect(game_window, food_types[food_type]['color'], pygame.Rect(food_pos[0], food_pos[1], 10, 10))

    # Vérification des collisions
    if snake_pos[0] < 0 or snake_pos[0] > screen_width-10 or snake_pos[1] < 0 or snake_pos[1] > screen_height-10:
        pygame.quit()
        sys.exit()
    for block in snake_body[1:]:
        if snake_pos == block:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    clock.tick(snake_speed)
