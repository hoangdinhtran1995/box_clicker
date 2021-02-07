# monkey clicking game
import pygame
import random
import math

pygame.init()

# create screen
screen = pygame.display.set_mode((800, 600))

# clock
clock = pygame.time.Clock()

pygame.display.set_caption("monkey box")

font = pygame.font.Font("freesansbold.ttf", 80)
time_font = pygame.font.Font("freesansbold.ttf", 32)


def dispnumbs(x, y, number):
    score = font.render(str(number), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text(x, y):
    over_text = font.render("GAME OVER", True, (200, 100, 100))
    screen.blit(over_text, (x, y))
    restart_text = time_font.render("Press Space to restart", True, (200, 100, 100))
    screen.blit(restart_text, (x + 80, y + 100))


def make_coordinates(numbers):
    x_cord = []
    y_cord = []
    x_cord_add = -1
    y_cord_add = -1
    for index in range(numbers):
        # check collision for each one
        collision = True
        while collision:
            collision = False

            # generate location
            x_cord_add = random.randint(50, 700)
            y_cord_add = random.randint(50, 480)

            # check collision
            for j in range(len(x_cord)):
                distance = math.sqrt(math.pow(x_cord[j] - x_cord_add, 2) + math.pow(y_cord[j] - y_cord_add, 2))
                if distance < 100:
                    collision = True

        x_cord.append(x_cord_add)
        y_cord.append(y_cord_add)

    return x_cord, y_cord


def display_time(cur_time, time_limit):
    time_text = time_font.render("Time: " + str(round(time_limit - cur_time, 1)), True, (150, 150, 150))
    screen.blit(time_text, (325, 10))


def display_level(level_number):
    level_text = time_font.render("Level " + str(level_number), True, (150, 150, 150))
    screen.blit(level_text, (10, 10))


def draw_boxes(box_x_cord, box_y_cord):
    if len(box_x_cord) > 0:
        white = (255, 255, 255)
        for index in range(len(box_x_cord)):
            pygame.draw.rect(screen, white, (box_x_cord[index], box_y_cord[index], 90, 80))


def check_collisions(x_coordinates_list, y_coordinates_list, click_position, current_number_index):
    number = -1
    for index in range(len(x_coordinates_list)):
        if x_coordinates_list[index] < click_position[0] < x_coordinates_list[index] + 90:
            if y_coordinates_list[index] < click_position[1] < y_coordinates_list[index] + 80:
                number = index + current_number_index
    return number


def restart():
    global level_initiated
    global game_over
    global n
    global level
    global time_lim
    level_initiated = False
    game_over = False
    n = first_n
    level = 1
    time_lim = first_time_lim

first_time_lim = 1
first_n = 3


boxed = False
level_initiated = False
game_over = False
running = True
n = first_n
level = 1
time_lim = first_time_lim

while running:

    if not level_initiated:
        xcord, ycord = make_coordinates(n)
        xcord_box = xcord.copy()
        ycord_box = ycord.copy()
        time = 0
        boxed = False
        current_number = 0
        level_initiated = True

    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_SPACE:
                restart()

        if event.type == pygame.MOUSEBUTTONUP and boxed:
            pos = pygame.mouse.get_pos()
            num = check_collisions(xcord_box, ycord_box, pos, current_number)
            if num != -1:
                if num == current_number:
                    del xcord_box[0]
                    del ycord_box[0]
                    current_number += 1
                    if num == n - 1:
                        level_initiated = False
                        n += 1
                        level += 1
                        time_lim += 0.5

                else:
                    # game over
                    xcord_box.clear()
                    ycord_box.clear()
                    game_over = True

    for i in range(len(xcord)):
        dispnumbs(xcord[i], ycord[i], i + 1)

    if time >= time_lim:
        draw_boxes(xcord_box, ycord_box)
        boxed = True
    else:
        time += 1 / 30
        display_time(time, time_lim)

    display_level(level)

    if game_over:
        game_over_text(150, 10)

    clock.tick(30)
    pygame.display.update()
