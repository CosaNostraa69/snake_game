import pygame
import sys
import random

pygame.init()

def game_init():
    global snake_pos, snake_body, food_pos, food_spawn, direction, change_to, score, food_type, snake_speed
    snake_pos = [100, 50]
    snake_body = [[100, 50], [90, 50], [80, 50]]
    food_pos = [random.randrange(1, (screen_width // 10)) * 10, random.randrange(1, (screen_height // 10)) * 10]
    food_spawn = True
    direction = 'RIGHT'
    change_to = direction
    score = 0
    food_type = random.choice(list(food_types.keys()))
    snake_speed = 15

def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    if choice == 'game_over':
        score_rect.midtop = (screen_width / 2, screen_height / 4)
    else:
        score_rect.midtop = (screen_width / 10, 15)
    game_window.blit(score_surface, score_rect)

def show_restart_button():
    restart_font = pygame.font.SysFont('Arial', 25)
    restart_surface = restart_font.render('Replay', True, white)
    restart_rect = restart_surface.get_rect()
    restart_rect.midtop = (screen_width / 2, screen_height / 2)
    pygame.draw.rect(game_window, red, restart_rect.inflate(20, 10))
    game_window.blit(restart_surface, restart_rect)
    pygame.display.flip()
    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and restart_rect.collidepoint(event.pos):
                waiting_for_input = False
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

# Paramètres de base du jeu
screen_width = 600
screen_height = 400
game_window = pygame.display.set_mode((screen_width, screen_height))

# Couleurs
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)  # Ajouté pour le bouton de redémarrage

# Fréquence d'actualisation
clock = pygame.time.Clock()

# Types de nourriture avec leurs couleurs et effets
food_types = {
    'speed_up': {'color': pygame.Color(255, 50, 50), 'speed_change': 5},
    'slow_down': {'color': pygame.Color(50, 255, 50), 'speed_change': -3}
}

game_init()  # Initialiser le jeu

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

    snake_body.insert(0, list(snake_pos))
    if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
        food_spawn = False
        score += 1  # Augmenter le score
        snake_speed += food_types[food_type]['speed_change']
        snake_speed = max(5, min(30, snake_speed))
    else:
        snake_body.pop()

    if not food_spawn:
        food_type = random.choice(list(food_types.keys()))
        food_pos = [random.randrange(1, (screen_width//10)) * 10, random.randrange(1, (screen_height//10)) * 10]
    food_spawn = True

    game_window.fill(black)
    for pos in snake_body:
        pygame.draw.rect(game_window, white, pygame.Rect(pos[0], pos[1], 10, 10))
    pygame.draw.rect(game_window, food_types[food_type]['color'], pygame.Rect(food_pos[0], food_pos[1], 10, 10))

    # Afficher le score pendant le jeu
    show_score('running', white, 'Arial', 20)

    if snake_pos[0] < 0 or snake_pos[0] > screen_width-10 or snake_pos[1] < 0 or snake_pos[1] > screen_height-10 or snake_pos in snake_body[1:]:
        show_score('game_over', red, 'times', 20)
        show_restart_button()
        game_init()  # Réinitialiser le jeu

    pygame.display.update()
    clock.tick(snake_speed)
