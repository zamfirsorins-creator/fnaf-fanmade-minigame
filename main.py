import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Retro Minigames Project")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 32)
big_font = pygame.font.SysFont(None, 60)

# culori
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK = (14, 14, 18)
GRAY = (90, 90, 90)
LIGHT_GRAY = (170, 170, 170)
PURPLE = (135, 45, 160)
DARK_PURPLE = (70, 0, 90)
YELLOW = (230, 190, 30)
BLUE = (20, 30, 120)
BROWN = (120, 70, 30)

# starea jocului
game_state = "level1"

# player
player = pygame.Rect(120, 380, 45, 90)
speed = 4

# LEVEL 1
level1_items = [
    pygame.Rect(260, 470, 30, 30),
    pygame.Rect(390, 220, 30, 30),
    pygame.Rect(600, 470, 30, 30),
]
level1_collected = 0
level1_door = pygame.Rect(690, 380, 60, 110)

# LEVEL 2
level2_room = 0
bear = pygame.Rect(600, 380, 45, 65)

# LEVEL 3
gifts = [
    {"color_name": "yellow", "color": YELLOW, "rect": pygame.Rect(130, 430, 30, 30), "taken": False},
    {"color_name": "blue", "color": BLUE, "rect": pygame.Rect(230, 430, 30, 30), "taken": False},
    {"color_name": "brown", "color": BROWN, "rect": pygame.Rect(330, 430, 30, 30), "taken": False},
    {"color_name": "purple", "color": PURPLE, "rect": pygame.Rect(430, 430, 30, 30), "taken": False},
]

characters = [
    {"color_name": "yellow", "color": YELLOW, "rect": pygame.Rect(120, 160, 45, 70), "done": False},
    {"color_name": "blue", "color": BLUE, "rect": pygame.Rect(280, 160, 45, 70), "done": False},
    {"color_name": "brown", "color": BROWN, "rect": pygame.Rect(440, 160, 45, 70), "done": False},
    {"color_name": "purple", "color": PURPLE, "rect": pygame.Rect(600, 160, 45, 70), "done": False},
]

held_gift = None


def reset_player():
    player.x = 100
    player.y = 380


def draw_scanlines():
    for y in range(0, HEIGHT, 4):
        pygame.draw.line(screen, (0, 0, 0), (0, y), (WIDTH, y), 1)


def draw_room_background():
    screen.fill(DARK)

    pygame.draw.rect(screen, (35, 35, 80), (0, 0, WIDTH, HEIGHT), 18)
    pygame.draw.rect(screen, (15, 15, 20), (60, 60, 680, 460))

    tile = 64
    for y in range(60, 520, tile):
        for x in range(60, 740, tile):
            if (x // tile + y // tile) % 2 == 0:
                color = (35, 35, 38)
            else:
                color = (8, 8, 10)
            pygame.draw.rect(screen, color, (x, y, tile, tile))


def draw_hall_background(room_number):
    screen.fill(DARK)

    tile = 50
    for y in range(80, 520, tile):
        for x in range(60, 740, tile):
            if (x // tile + y // tile) % 3 == 0:
                color = WHITE
            elif (x // tile + y // tile) % 3 == 1:
                color = LIGHT_GRAY
            else:
                color = BLACK

            pygame.draw.rect(screen, color, (x, y, tile, tile))

    pygame.draw.rect(screen, (20, 20, 25), (0, 0, WIDTH, 80))
    pygame.draw.rect(screen, (20, 20, 25), (0, 520, WIDTH, 80))
    pygame.draw.rect(screen, (80, 80, 100), (0, 0, WIDTH, HEIGHT), 18)

    text = font.render(f"Camera {room_number + 1}/4", True, WHITE)
    screen.blit(text, (30, 30))


def draw_player():
    keys = pygame.key.get_pressed()
    moving = keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]

    if moving:
        walk = 4 if (pygame.time.get_ticks() // 200) % 2 == 0 else -4
    else:
        walk = 0

    x = player.x
    y = player.y

    pygame.draw.rect(screen, PURPLE, (x - 10, y - 24, 38, 24))
    pygame.draw.rect(screen, DARK_PURPLE, (x - 5, y - 30, 28, 6))

    pygame.draw.rect(screen, WHITE, (x - 5, y - 16, 8, 6))
    pygame.draw.rect(screen, WHITE, (x + 13, y - 16, 8, 6))
    pygame.draw.rect(screen, BLACK, (x + 13, y - 5, 10, 4))

    pygame.draw.rect(screen, PURPLE, (x + 12, y, 36, 50))

    pygame.draw.rect(screen, PURPLE, (x - 28, y + 10 + walk, 40, 13))
    pygame.draw.rect(screen, PURPLE, (x - 15, y + 34 - walk, 25, 13))

    pygame.draw.rect(screen, PURPLE, (x + 18, y + 48, 11, 52 + walk))
    pygame.draw.rect(screen, PURPLE, (x + 38, y + 48, 11, 38 - walk))

    pygame.draw.rect(screen, PURPLE, (x + 10, y + 96 + walk, 24, 13))
    pygame.draw.rect(screen, PURPLE, (x + 38, y + 80 - walk, 24, 13))


def draw_bear(rect):
    pygame.draw.rect(screen, YELLOW, (rect.x + 8, rect.y + 15, 32, 45))
    pygame.draw.rect(screen, YELLOW, (rect.x, rect.y, 48, 35))

    pygame.draw.rect(screen, YELLOW, (rect.x + 3, rect.y - 10, 12, 15))
    pygame.draw.rect(screen, YELLOW, (rect.x + 33, rect.y - 10, 12, 15))

    pygame.draw.rect(screen, WHITE, (rect.x + 10, rect.y + 12, 8, 6))
    pygame.draw.rect(screen, WHITE, (rect.x + 30, rect.y + 12, 8, 6))
    pygame.draw.rect(screen, BLACK, (rect.x + 22, rect.y + 23, 8, 5))


def move_player():
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player.x -= speed
    if keys[pygame.K_RIGHT]:
        player.x += speed
    if keys[pygame.K_UP]:
        player.y -= speed
    if keys[pygame.K_DOWN]:
        player.y += speed

    if player.left < 70:
        player.left = 70
    if player.right > 730:
        player.right = 730
    if player.top < 130:
        player.top = 130
    if player.bottom > 500:
        player.bottom = 500


def update_level1():
    global game_state, level1_collected

    move_player()

    for item in level1_items[:]:
        if player.colliderect(item):
            level1_items.remove(item)
            level1_collected += 1

    if level1_collected == 3 and player.colliderect(level1_door):
        reset_player()
        game_state = "level2"


def draw_level1():
    draw_room_background()

    pygame.draw.rect(screen, YELLOW, level1_door)

    for item in level1_items:
        pygame.draw.rect(screen, WHITE, item)
        pygame.draw.rect(screen, LIGHT_GRAY, (item.x + 5, item.y + 5, 20, 8))

    draw_player()

    text = font.render(f"Level 1 - Obiecte: {level1_collected}/3", True, WHITE)
    screen.blit(text, (30, 30))

    if level1_collected == 3:
        msg = font.render("Mergi la usa galbena", True, WHITE)
        screen.blit(msg, (30, 555))

    draw_scanlines()


def update_level2():
    global game_state, level2_room

    move_player()

    if player.colliderect(bear):
        level2_room += 1
        reset_player()

        if level2_room >= 4:
            level2_room = 0
            reset_player()
            game_state = "level3"

def draw_level2():
    draw_hall_background(level2_room)

    # mutăm ursul în locuri diferite în funcție de cameră
    bear_positions = [
        (600, 380),
        (620, 160),
        (130, 180),
        (560, 420),
    ]

    bear.x, bear.y = bear_positions[min(level2_room, 3)]

    draw_bear(bear)
    draw_player()

    msg = font.render("Urmareste ursul auriu", True, WHITE)
    screen.blit(msg, (30, 555))

    draw_scanlines()


def draw_static_character(character):
    rect = character["rect"]
    color = character["color"]

    pygame.draw.rect(screen, color, (rect.x + 8, rect.y + 25, 30, 45))
    pygame.draw.rect(screen, color, (rect.x, rect.y, 48, 35))

    pygame.draw.rect(screen, WHITE, (rect.x + 10, rect.y + 13, 8, 6))
    pygame.draw.rect(screen, WHITE, (rect.x + 30, rect.y + 13, 8, 6))

    if character["done"]:
        pygame.draw.rect(screen, (0, 220, 0), (rect.x + 12, rect.y + 75, 25, 8))


def update_level3():
    global game_state, held_gift

    move_player()

    for gift in gifts:
        if not gift["taken"] and held_gift is None:
            if player.colliderect(gift["rect"]):
                held_gift = gift
                gift["taken"] = True

    for character in characters:
        if player.colliderect(character["rect"]):
            if held_gift is not None:
                if held_gift["color_name"] == character["color_name"]:
                    character["done"] = True
                    held_gift = None

    all_done = True
    for character in characters:
        if not character["done"]:
            all_done = False

    if all_done:
        game_state = "end"


def draw_level3():
    draw_room_background()

    for character in characters:
        draw_static_character(character)

    for gift in gifts:
        if not gift["taken"]:
            pygame.draw.rect(screen, gift["color"], gift["rect"])
            pygame.draw.rect(screen, WHITE, (gift["rect"].x + 12, gift["rect"].y, 6, 30))
            pygame.draw.rect(screen, WHITE, (gift["rect"].x, gift["rect"].y + 12, 30, 6))

    if held_gift is not None:
        gift_rect = pygame.Rect(player.x + 20, player.y - 55, 24, 24)
        pygame.draw.rect(screen, held_gift["color"], gift_rect)
        pygame.draw.rect(screen, WHITE, (gift_rect.x + 9, gift_rect.y, 5, 24))
        pygame.draw.rect(screen, WHITE, (gift_rect.x, gift_rect.y + 9, 24, 5))

    draw_player()

    done_count = 0
    for character in characters:
        if character["done"]:
            done_count += 1

    text = font.render(f"Level 3 - Cadouri livrate: {done_count}/4", True, WHITE)
    screen.blit(text, (30, 30))

    msg = font.render("Du fiecare cadou la personajul de aceeasi culoare", True, WHITE)
    screen.blit(msg, (30, 555))

    draw_scanlines()


def draw_end_screen():
    screen.fill(BLACK)

    title = big_font.render("Joc terminat!", True, WHITE)
    screen.blit(title, (260, 240))

    msg = font.render("Ai terminat toate cele 3 levele.", True, WHITE)
    screen.blit(msg, (245, 310))

    draw_scanlines()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if game_state == "level1":
        update_level1()
        draw_level1()

    elif game_state == "level2":
        update_level2()
        draw_level2()

    elif game_state == "level3":
        update_level3()
        draw_level3()

    elif game_state == "end":
        draw_end_screen()

    pygame.display.flip()
    clock.tick(60)