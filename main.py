import pygame
from pygame.time import Clock
import time

clock: Clock = pygame.time.Clock()

pygame.init()

screen = pygame.display.set_mode((600, 360))
pygame.display.set_caption("Rat Run")
icon = pygame.image.load("images/rat.png")
pygame.display.set_icon(icon)

bg = pygame.image.load("images/bg.jpg").convert()

cactys = pygame.image.load("images/Кактус.png").convert_alpha()

cactys_list_in_game = []
walk_right = [
    pygame.image.load("images/run_right/rat_run_right1.png").convert_alpha(),
    pygame.image.load("images/run_right/rat_run_right2.png").convert_alpha(),
    pygame.image.load("images/run_right/rat_run_right3.png").convert_alpha(),
    pygame.image.load("images/run_right/rat_run_right4.png").convert_alpha()
]

walk_left = [
    pygame.image.load("images/run_left/rat_run_left1.png").convert_alpha(),
    pygame.image.load("images/run_left/rat_run_left2.png").convert_alpha(),
    pygame.image.load("images/run_left/rat_run_left3.png").convert_alpha(),
    pygame.image.load("images/run_left/rat_run_left4.png").convert_alpha()
]

pac = 0
bg_x = 0

player_speed = 7
player_x = 150
player_y = 202

is_jump = False
jump_count = 8.25

cactys_timer = pygame.USEREVENT + 1
pygame.time.set_timer(cactys_timer, 5500)

coin_true = False
replay = 0

label = pygame.font.Font("fonts/Roboto-Bold.ttf", 40)
lose_label = label.render('Ты проиграл!', True, (193, 196, 193))
restart_label = label.render('Играть заново', True, (115, 132, 148))
restart_label_rect = restart_label.get_rect(topleft=(175, 125))
gameplay = True

game_over_sound = pygame.mixer.Sound("sounds/game-over.mp3")
bg_sound = pygame.mixer.music.load('sounds/music.mp3')



running = True
while running:
    screen.blit(bg, (bg_x, 0))
    screen.blit(bg, (bg_x + 600, 0))

    if gameplay:

        replay_label = label.render(f'Попыток: {replay}', True, (115, 132, 148))
        screen.blit(replay_label, (10, 10))

        if is_jump == False and player_y < 202:
            player_y = 202

        if player_y > 202:
            player_y = 202

        player_rect = walk_right[pac].get_rect(topleft=(player_x, player_y))

        if cactys_list_in_game:
            for (i, el) in enumerate(cactys_list_in_game):
                screen.blit(cactys, el)
                el.x -= 10

                if el.x < -1:
                    cactys_list_in_game.pop(i)

                if player_rect.colliderect(el):
                    pygame.mixer.music.pause()
                    time.sleep(0.15)
                    gameplay = False
                    game_over_sound.play()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player_x > 25:
            player_x -= player_speed
            player_speed = 8.1
            screen.blit(walk_left[pac], (player_x, player_y))
        else:
            screen.blit(walk_right[pac], (player_x, player_y))
        if keys[pygame.K_d] and player_x <= 430:
            player_x += player_speed
            player_speed = 8.5
        if pac == 3:
            pac = 0
        else:
            pac += 1

        bg_x -= 5

        if bg_x == -600:
            bg_x = 0

        if not is_jump:
            if keys[pygame.K_SPACE]:
                is_jump = True
        else:
            if jump_count >= -8.25:
                player_speed = 9
                if jump_count > 0:
                    player_y -= (jump_count ** 2) / 2
                else:
                    player_y += (jump_count ** 2) / 2
                jump_count -= 1
            else:
                player_speed = 8
                is_jump = False
                jump_count = 8.25

    else:
        screen.fill((87, 88, 89))
        screen.blit(lose_label, (180, 50))
        screen.blit(restart_label, restart_label_rect)

        mouse = pygame.mouse.get_pos()
        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            replay += 1

            player_x = 150
            cactys_list_in_game.clear()

    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == cactys_timer:
            cactys_list_in_game.append(cactys.get_rect(topleft=(600, 190)))
    clock.tick(17)