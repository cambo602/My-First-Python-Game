import pygame
import sys
import random

pygame.init()

WIDTH = 800
HEIGHT = 600

BLUE = (0, 0, 200)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BACKGROUND_COLOUR = (0, 0, 0)

player_size = 50
player_pos = [WIDTH/2, HEIGHT-2*player_size]

enemy_size = 50
enemy_pos = [random.randint(0, WIDTH-enemy_size), 0]
enemy_speed = 10
enemy_list = [enemy_pos]

screen = pygame.display.set_mode((WIDTH, HEIGHT))

score = 0

game_over = False

clock = pygame.time.Clock()

myFont = pygame.font.SysFont("monospace", 35)

def set_level(score, enemy_speed):
    if score < 20:
        enemy_speed = 4
    elif score < 40:
        enemy_speed = 6
    elif score < 60:
        enemy_speed = 10
    else:
        enemy_speed = 15
    return enemy_speed

def drop_enemies(enemy_list):
    delay = random.random()
    if len(enemy_list) < 10 and delay < 0.2:
        x_pos = random.randint(0, WIDTH-enemy_size)
        y_pos = 0
        enemy_list.append([x_pos, y_pos])

def draw_enemies(enemy_list):
    for enemy_pos in enemy_list:
        pygame.draw.rect(screen, RED, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))

def update_enemies(enemy_list, score):
    # Update pos of enemy
    for idx, enemy_pos in enumerate(enemy_list):
        if enemy_pos[1] >= 0 and enemy_pos[1] < HEIGHT:
            enemy_pos[1] += enemy_speed
        else:
            enemy_list.pop(idx)
            score += 1
    return score

def collision_check(enemy_list, player_pos):
    for enemy_pos in enemy_list:
        if hit_detect(enemy_pos, player_pos):
            return True
    return False
        

def hit_detect(player_pos, enemy_pos):
    p_x = player_pos[0]
    p_y = player_pos[1]

    e_x = enemy_pos[0]
    e_y = enemy_pos[1]

    if (e_x >= p_x and e_x < (p_x + player_size)) or (p_x >= e_x and p_x < (e_x+enemy_size)):
        if (e_y >= p_y and e_y < (p_y + player_size)) or (p_y >= e_y and p_y < (e_y+enemy_size)):
            return True
    return False

    

while not game_over:

    for event in pygame.event.get():
        print(event)

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.KEYDOWN:
            x = player_pos[0]
            y = player_pos[1]
            if event.key == pygame.K_RIGHT:
                x += player_size
            elif event.key == pygame.K_LEFT:
                x -= player_size

            player_pos = [x,y]

    screen.fill(BACKGROUND_COLOUR)

    clock.tick(30)
    
    score = update_enemies(enemy_list, score)

    text = "Score: " + str(score)
    label = myFont.render(text, 1, YELLOW)
    screen.blit(label,(WIDTH-200, HEIGHT-40))
    
    enemy_speed = set_level(score, enemy_speed)
    
    drop_enemies(enemy_list)
    if collision_check(enemy_list, player_pos):
        game_over = True
        break
    
    draw_enemies(enemy_list)
    
    
    pygame.draw.rect(screen, BLUE, (round(player_pos[0]), round(player_pos[1]), round(player_size), round(player_size)))
    
    pygame.display.update()
 
