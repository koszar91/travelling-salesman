from math import exp, sqrt, inf, pi, cos, sin
import pygame
import copy
import random


# ANNEALING PARAMETERS
N_CITIES = 50
CITIES_PATTERN = 'random'  # can be 'random' or 'circle'
TEMP_START = 1e6
TEMP_END = 1e-4
TEMP_CHANGE = 0.999


# GRAPHIC PARAMETERS
WIDTH, HEIGHT = 1200, 900
CITY_RADIUS = 7
FONT_SIZE = 35
BORDER_THICKNESS = 70
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (205, 205, 205)


def generate_cities(n, width, height, method):
    def dist(city1, city2):
        return sqrt((city2[0] - city1[0]) ** 2 + (city2[1] - city1[1]) ** 2)
    res = []
    if method == 'random':
        for i in range(n):
            x = random.random() * (width - 2 * BORDER_THICKNESS) + BORDER_THICKNESS
            y = random.random() * (height - 2 * BORDER_THICKNESS) + BORDER_THICKNESS
            res.append((x, y))
    elif method == 'circle':
        alpha = 0
        alpha_change = 2 * pi / n
        r = 0.8 * min(width / 2, height / 2)
        for i in range(n):
            x = r * cos(alpha) + width / 2
            y = r * sin(alpha) + height / 2
            alpha += alpha_change
            res.append((x, y))
        for i in range(n * 10):
            i = random.randint(0, n-1)
            j = random.randint(0, n-1)
            res[i], res[j] = res[j], res[i]
    elif method == 'special':
        for i in range(n):
            x = random.random() * (width - 2 * BORDER_THICKNESS) + BORDER_THICKNESS
            y = random.random() * (height - 2 * BORDER_THICKNESS) + BORDER_THICKNESS
            res.append((x, y))

        idx_of_second_city = None
        min_dist = inf
        for i in range(1, n):
            if dist(res[0], res[i]) < min_dist:
                idx_of_second_city = i
        res[1], res[idx_of_second_city] = res[idx_of_second_city], res[1]
    return res


def get_route_length(route):
    def dist(city1, city2):
        return sqrt((city2[0] - city1[0]) ** 2 + (city2[1] - city1[1]) ** 2)
    result = 0
    length = len(route)
    for i in range(length):
        result += dist(route[i], route[(i + 1) % length]) / 10
    return result


def get_next_route(route):
    length = len(route)
    res = route[:]
    i = random.randint(0, length - 1)
    j = random.randint(0, length - 1)
    res[i], res[j] = res[j], res[i]
    return res


def draw(surface, city_color, route_color, n_cities, route, route_width, city_radius):
    screen.fill(BLACK)
    # draw route
    for i in range(n_cities):
        pygame.draw.line(surface, route_color, route[i], route[(i + 1) % n_cities], route_width)
    # draw cities
    for city in cities:
        pygame.draw.circle(surface, city_color, city, city_radius)
    # draw text
    if finished:
        t = 'DONE'
    else:
        t = "temperature: {}".format(round(temp, 10))
    screen.blit(font.render(t, True, RED), (20, 15))
    pygame.display.update()


if __name__ == '__main__':
    # setup visualization
    pygame.init()
    window_size = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Travelling Salesman Problem using SA")
    font = pygame.font.SysFont(None, FONT_SIZE)

    # setup logic
    cities = generate_cities(N_CITIES, WIDTH, HEIGHT, CITIES_PATTERN)
    temp = TEMP_START
    new_route = cities[:]
    curr_route = cities[:]
    curr_length = inf
    curr_step_for_temp = 0

    finished = False
    close_window = False

    while not close_window:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close_window = True

        if not finished:
            # calculate step
            new_route = get_next_route(curr_route)
            new_length = get_route_length(new_route)
            diff = new_length - curr_length
            if diff < 0 or exp(-diff / temp) > random.random():
                curr_route = copy.deepcopy(new_route)
                curr_length = new_length

            temp *= TEMP_CHANGE
            if temp <= TEMP_END:
                temp = TEMP_END
                finished = True

        draw(screen, RED, WHITE, N_CITIES, curr_route, 3, CITY_RADIUS)

    pygame.quit()
