import pygame
import random
import sys
import os

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
TRANSPARENT = (0, 0, 0, 0)

# Load images
road_image_path = r"C:\Users\aditya\OneDrive\Desktop\thiru\ghh.jpg"  # Raw string to handle backslashes
man_image_path = r"C:\Users\aditya\OneDrive\Desktop\thiru\man.jpg"  # Image of the man

if not os.path.exists(road_image_path):
    print(f"Error: The image path '{road_image_path}' does not exist.")
    pygame.quit()
    sys.exit()

if not os.path.exists(man_image_path):
    print(f"Error: The image path '{man_image_path}' does not exist.")
    pygame.quit()
    sys.exit()

try:
    road_image = pygame.image.load(road_image_path)
    road_image = pygame.transform.scale(road_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    man_image = pygame.image.load(man_image_path)
    man_size = (50, 100)  # Size of the man image
    man_image = pygame.transform.scale(man_image, man_size)

    enemy_image = pygame.image.load(man_image_path)
    enemy_image = pygame.transform.scale(enemy_image, man_size)
except pygame.error as e:
    print(f"Error loading image: {e}")
    pygame.quit()
    sys.exit()

# Player settings
player_size = man_size
player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT - 2 * player_size[1]]

# Enemy settings
enemy_size = man_size[0]
enemy_list = []

# Speed settings
speed = 10

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Car Run")

# Set up clock
clock = pygame.time.Clock()

# Score
score = 0
font = pygame.font.SysFont("monospace", 35)

def set_level(score, speed):
    if score < 20:
        speed = 5
    elif score < 40:
        speed = 8
    elif score < 60:
        speed = 12
    else:
        speed = 15
    return speed

def drop_enemies(enemy_list):
    delay = random.random()
    if len(enemy_list) < 10 and delay < 0.1:
        x_pos = random.randint(0, SCREEN_WIDTH - enemy_size)
        y_pos = 0
        enemy_list.append([x_pos, y_pos])

def draw_enemies(enemy_list):
    for enemy_pos in enemy_list:
        screen.blit(enemy_image, (enemy_pos[0], enemy_pos[1]))

def update_enemy_positions(enemy_list, score):
    for idx, enemy_pos in enumerate(enemy_list):
        if enemy_pos[1] >= 0 and enemy_pos[1] < SCREEN_HEIGHT:
            enemy_pos[1] += speed
        else:
            enemy_list.pop(idx)
            score += 1
    return score

def collision_check(enemy_list, player_pos):
    for enemy_pos in enemy_list:
        if detect_collision(enemy_pos, player_pos):
            return True
    return False

def detect_collision(player_pos, enemy_pos):
    p_x = player_pos[0]
    p_y = player_pos[1]

    e_x = enemy_pos[0]
    e_y = enemy_pos[1]

    if (e_x >= p_x and e_x < (p_x + player_size[0])) or (p_x >= e_x and p_x < (e_x + enemy_size)):
        if (e_y >= p_y and e_y < (p_y + player_size[1])) or (p_y >= e_y and p_y < (e_y + player_size[1])):
            return True
    return False

def game_loop():
    global score, speed, enemy_list, player_pos, game_over
    score = 0
    speed = 10
    enemy_list = []
    player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT - 2 * player_size[1]]
    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_pos[0] > 0:
            player_pos[0] -= 10
        if keys[pygame.K_RIGHT] and player_pos[0] < SCREEN_WIDTH - player_size[0]:
            player_pos[0] += 10

        # Draw road image
        screen.blit(road_image, (0, 0))

        drop_enemies(enemy_list)
        score = update_enemy_positions(enemy_list, score)
        speed = set_level(score, speed)

        text = font.render("Score: {0}".format(score), True, WHITE)
        screen.blit(text, (10, 10))

        draw_enemies(enemy_list)

        screen.blit(man_image, (player_pos[0], player_pos[1]))

        if collision_check(enemy_list, player_pos):
            game_over = True

        pygame.display.update()

        clock.tick(30)

    game_over_screen()

def game_over_screen():
    global game_over, score
    game_over_font = pygame.font.SysFont("monospace", 50)
    button_font = pygame.font.SysFont("monospace", 35)
    end_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 100, 200, 50)
    continue_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 20, 200, 50)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if end_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
                if continue_button.collidepoint(event.pos):
                    main_menu()

        screen.blit(road_image, (0, 0))
        game_over_text = game_over_font.render("Game Over!", True, RED)
        score_text = button_font.render("Score: {0}".format(score), True, WHITE)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 4))
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 4 + 60))

        pygame.draw.rect(screen, TRANSPARENT, end_button)
        end_text = button_font.render("End", True, WHITE)
        screen.blit(end_text, (end_button.x + (end_button.width - end_text.get_width()) // 2,
                               end_button.y + (end_button.height - end_text.get_height()) // 2))

        pygame.draw.rect(screen, TRANSPARENT, continue_button)
        continue_text = button_font.render("Continue", True, WHITE)
        screen.blit(continue_text, (continue_button.x + (continue_button.width - continue_text.get_width()) // 2,
                                    continue_button.y + (continue_button.height - continue_text.get_height()) // 2))

        pygame.display.update()
        clock.tick(30)

def main_menu():
    menu_font = pygame.font.SysFont("monospace", 50)
    button_font = pygame.font.SysFont("monospace", 35)
    start_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, 200, 100)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    game_loop()

        screen.blit(road_image, (0, 0))
        menu_text = menu_font.render("Temple Run", True, WHITE)
        screen.blit(menu_text, (SCREEN_WIDTH // 2 - menu_text.get_width() // 2, SCREEN_HEIGHT // 4))

        pygame.draw.rect(screen, TRANSPARENT, start_button)
        start_text = button_font.render("Start", True, WHITE)
        screen.blit(start_text, (start_button.x + (start_button.width - start_text.get_width()) // 2,
                                 start_button.y + (start_button.height - start_text.get_height()) // 2))

        pygame.display.update()
        clock.tick(30)

if __name__ == "__main__":
    main_menu()
