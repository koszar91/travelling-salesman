from math import exp, sqrt, inf, pi, cos, sin
import pygame
import copy
import random

# screen
from numba import jit

WIDTH, HEIGHT = 800, 600
FPS = 120

# colors
RED = (255, 0, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

# sizes
CITY_RADIUS = 5
FONT_SIZE = 25

# cities
cities = []

# simulated annealing stuff
START_TEMPERATURE = 150
TEMPERATURE_CHANGE = 0.5
STEPS_FOR_TEMP = 20


def gen_rand_cities(n, width, height):
    res = []
    width *= 0.8
    width += 0.2 * width
    height *= 0.8
    height += 0.2 * height
    for i in range(n):
        x = random.random() * width
        y = random.random() * height
        res.append([x, y])
    return res


def gen_circle_cities(n, width, height):
    res = []
    alpha = 0
    alpha_change = 2 * pi / n
    r = 0.8 * min(width/2, height/2)
    for i in range(n):
        x = r * cos(alpha) + width/2
        y = r * sin(alpha) + height/2
        alpha += alpha_change
        res.append((x, y))
    for i in range(1000):
        res = next_route(res)
    return res


def dist(city1, city2):
    return sqrt((city2[0] - city1[0]) ** 2 + (city2[1] - city1[1]) ** 2)


def total_length(route):
    result = 0
    length = len(route)
    for i in range(length):
        result += dist(route[i], route[(i + 1) % length])
    return result


def next_route(route):
    i = random.randint(0, len(route) - 1)
    route[i], route[(i+1)%len(route)] = route[(i+1)%len(route)], route[i]
    return route


def draw_cities(surface):
    for city in cities:
        pygame.draw.circle(surface, YELLOW, city, CITY_RADIUS)


def draw_route(surface, route):
    length = len(route)
    for i in range(length):
        pygame.draw.line(surface, RED, route[i], route[(i + 1) % length])


if __name__ == '__main__':
    # setup visualization
    pygame.init()
    window_size = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Travelling Salesman Problem using SA")
    font = pygame.font.SysFont(None, FONT_SIZE)
    clock = pygame.time.Clock()

    # setup logic
    cities = gen_circle_cities(10, WIDTH, HEIGHT)
    temp = START_TEMPERATURE
    best_route = copy.deepcopy(cities)
    best_length = inf
    candidate_route = copy.deepcopy(best_route)
    curr_step_for_temp = 0

    finished = False
    close_window = False
    while not close_window:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close_window = True

        if not finished:
            # calculate step
            candidate_route = next_route(candidate_route)
            candidate_length = total_length(candidate_route)
            diff = candidate_length - best_length
            if diff < 0 or exp(-diff / temp) > random.random():
                best_length = candidate_length
                best_route = copy.deepcopy(candidate_route)

            if curr_step_for_temp < STEPS_FOR_TEMP:
                curr_step_for_temp += 1
            else:
                curr_step_for_temp = 0
                temp -= TEMPERATURE_CHANGE
            if temp <= 0:
                temp = 0
                finished = True

        # draw graphics
        screen.fill(BLACK)
        draw_cities(screen)
        draw_route(screen, best_route)
        screen.blit(font.render("temperature: " + repr(round(temp, 3)),
                                True, YELLOW), (20, 50))
        screen.blit(font.render("best length: " + repr(round(best_length, 3)),
                                True, YELLOW), (20, 20))
        pygame.display.update()

    pygame.quit()
