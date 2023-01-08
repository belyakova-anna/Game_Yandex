import random

import pygame
import sys
import os
from random import choice, randint


def terminate():
    pygame.quit()
    sys.exit()


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, imgs, x, y, x_size, y_size, time, *group):
        super().__init__(*group)
        self.time = time
        self.frames = [tile_images[el] for el in imgs]
        # print(self.frames)
        # self.frames = imgs[:]
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        # print(tile_width * x, tile_height * y)
        self.rect = pygame.Rect(x, y, x_size, y_size)

    def update(self):
        self.cur_frame = (self.cur_frame + self.time) % len(self.frames)
        self.image = self.frames[int(self.cur_frame)]


class AnimatedPortal(pygame.sprite.Sprite):
    def __init__(self, num, x, y):
        super().__init__(level_sprites, portal_group)
        if num == 1:
            self.frames = [pygame.transform.scale(load_image('11.png'), (tile_width, tile_height)),
                           pygame.transform.scale(load_image('21.png'), (tile_width, tile_height)),
                           pygame.transform.scale(load_image('31.png'), (tile_width, tile_height)),
                           pygame.transform.scale(load_image('41.png'), (tile_width, tile_height))]
        elif num == 2:
            self.frames = [pygame.transform.scale(load_image('12.png'), (tile_width, tile_height)),
                           pygame.transform.scale(load_image('22.png'), (tile_width, tile_height)),
                           pygame.transform.scale(load_image('32.png'), (tile_width, tile_height)),
                           pygame.transform.scale(load_image('42.png'), (tile_width, tile_height))]
        elif num == 3:
            self.frames = [pygame.transform.scale(load_image('13.png'), (tile_width, tile_height)),
                           pygame.transform.scale(load_image('23.png'), (tile_width, tile_height)),
                           pygame.transform.scale(load_image('33.png'), (tile_width, tile_height)),
                           pygame.transform.scale(load_image('43.png'), (tile_width, tile_height))]
        elif num == 4:
            self.frames = [pygame.transform.scale(load_image('14.png'), (tile_width, tile_height)),
                           pygame.transform.scale(load_image('24.png'), (tile_width, tile_height)),
                           pygame.transform.scale(load_image('34.png'), (tile_width, tile_height)),
                           pygame.transform.scale(load_image('44.png'), (tile_width, tile_height))]
        self.cur_frame = 0
        self.image = self.frames[int(self.cur_frame)]
        self.rect = pygame.Rect(tile_width * x, tile_height * y, tile_width, tile_height)

    def update(self):
        self.cur_frame = (self.cur_frame + 0.05) % len(self.frames)
        self.image = self.frames[int(self.cur_frame)]


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def start_screen(screen):
    intro_text = ["Civil defense"]
    fon = pygame.transform.scale(load_image('fon1.jpeg'), (width, height))
    screen.blit(fon, (0, 0))
    text_coord = 250
    for line in intro_text:
        string_rendered = my_font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                # terminate()
                return  # начинаем игру
        pygame.display.flip()


def home_screen(screen):
    fps = 60
    clock = pygame.time.Clock()

    font1 = pygame.font.Font('data/Undertale-Battle-Font.ttf', 20)

    # Create a font file by passing font file
    # and size of the font
    text_necromancer = font1.render('Некромант', True, (255, 255, 255))
    textRect_necromancer = text_necromancer.get_rect()

    text_dino = font1.render('Дино', True, (255, 255, 255))
    textRect_dino = text_dino.get_rect()
    while True:
        clock.tick(fps)
        screen.fill(pygame.Color('black'))
        home_sprites.draw(screen)
        hero_group.draw(screen)
        ui_home_group.draw(screen)
        if hero.cur_scene == 'level':
            return

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONUP:
                home_pos = pygame.mouse.get_pos()
                home_clicked_sprites = [el for el in ui_home_group if el.rect.collidepoint(home_pos)]
                for el in home_clicked_sprites:
                    if el.tile_type == 'close_home':
                        terminate()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            hero.move(-1, 0)
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            hero.move(1, 0)
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            hero.move(0, -1)
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            hero.move(0, 1)
        if (abs(hero.rect[0] - necromancer.rect[0]) <= tile_width) and (
                abs(hero.rect[1] - necromancer.rect[1]) <= tile_height):
            textRect_necromancer.center = (
            necromancer.rect[0] + text_necromancer.get_rect()[2] // 4, necromancer.rect[1])
            screen.blit(text_necromancer, textRect_necromancer)
        if (abs(hero.rect[0] - dino.rect[0]) <= tile_width) and (
                abs(hero.rect[1] - dino.rect[1]) <= tile_height):
            textRect_dino.center = (dino.rect[0] + text_dino.get_rect()[2] - 10, dino.rect[1])
            screen.blit(text_dino, textRect_dino)
        pygame.display.flip()


def load_level(filename):
    filename = "data/" + filename
    try:
        with open(filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]
    except Exception:
        print(f"Файл с изображением '{filename}' не найден")
        sys.exit()
    return level_map


class Box(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(level_sprites, box_group)
        self.image = tile_images['box']
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.need_to_open = 0
        self.opened = 0
        self.weapon_is_taken = 0

        self.frames = [pygame.transform.scale(load_image('chest_empty_open_anim_f1.png'), (tile_width, tile_height)),
                       pygame.transform.scale(load_image('chest_empty_open_anim_f2.png'), (tile_width, tile_height))]
        self.cur_frame = 0
        self.weapon = None

    def update(self):
        if self.need_to_open and not self.opened:
            self.cur_frame = (self.cur_frame + 0.05) % len(self.frames)
            self.image = self.frames[int(self.cur_frame)]
            if int(self.cur_frame) == 1:
                self.opened = 1
                self.need_to_open = 0
                self.weapon = Weapon(choice(weapon), self.rect[0], self.rect[1])


class Weapon(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(level_sprites, weapon_group)
        self.type_gun = tile_type
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            pos_x, pos_y)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        if tile_type in ['wall_left', 'wall_right', 'side_left', 'side_right', 'top_left', 'top_right', 'down_left',
                         'down_right']:
            super().__init__(level_sprites, wall_group)
        elif tile_type == 'wall_home':
            super().__init__(home_sprites, wall_home_group)
        elif tile_type in ['floor_home', 'cover1', 'cover2', 'cover3', 'cover4', 'cover5',
                           'cover6', 'cover7', 'cover8']:
            super().__init__(home_sprites, floor_home_group)
        elif tile_type == 'floor_fon':
            super().__init__(level_sprites)
        elif tile_type == 'floor_home_fon':
            super().__init__(home_sprites)
        elif tile_type in ['exit_left', 'exit_right']:
            super().__init__(home_sprites, exit_group, floor_home_group)
        elif tile_type in ['necromancer', 'okult1', 'okult2', 'okult3', 'okult4']:
            super().__init__(home_sprites, necromancer_group)
        elif tile_type in ['guitar1', 'guitar2', 'guitar3', 'guitar4']:
            super().__init__(home_sprites, guitar_group)
        elif tile_type == "floor":
            super().__init__(level_sprites, floor_group)
        elif tile_type == "empty_home":
            super().__init__(home_sprites, empty_group)
        elif tile_type == "empty_level":
            super().__init__(level_sprites, empty_group)
        elif tile_type == "dino":
            super().__init__(level_sprites, dino_group)
        # im = tile_images[tile_type]
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Necromancer(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(home_sprites, necromancer_group)
        self.image = tile_images['necromancer']
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Dino(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(home_sprites, necromancer_group)
        self.image = tile_images['dino']
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Orc(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(level_sprites, monsters_group)
        self.tile_type = tile_type
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.rotation = 'right'
        self.v = 1
        self.lifes = 5
        self.is_died = 0

    def move(self, dx, dy):
        if not self.is_died:
            self.rect = pygame.rect.Rect(self.rect[0] + dx * self.v, self.rect[1] + dy * self.v,
                                         self.rect[2],
                                         self.rect[3])
            if (pygame.sprite.spritecollideany(self, box_group)
                    or pygame.sprite.spritecollideany(self, wall_group)):
                self.rect = pygame.rect.Rect(self.rect[0] - dx * self.v, self.rect[1] - dy * self.v,
                                             self.rect[2],
                                             self.rect[3])
            if pygame.sprite.spritecollideany(self, hero_group):
                if self.rect[0] <= hero.rect[0] and self.rect[1] <= hero.rect[1]:
                    hero.move(tile_width // hero.v, tile_height // hero.v)
                if self.rect[0] >= hero.rect[0] and self.rect[1] <= hero.rect[1]:
                    hero.move(- tile_width // hero.v, tile_height // hero.v)
                if self.rect[0] <= hero.rect[0] and self.rect[1] >= hero.rect[1]:
                    hero.move(tile_width // hero.v, - tile_height // hero.v)
                if self.rect[0] >= hero.rect[0] and self.rect[1] >= hero.rect[1]:
                    hero.move(- tile_width // hero.v, - tile_height // hero.v)
                hero.count_lifes.count = hero.count_lifes.count - 1
                if hero.count_lifes.count <= 0:
                    print('У тебя закончились жизни')
                    terminate()

    def update(self):
        for el in fire_group:
            if self.rect.colliderect(el.rect):
                self.lifes = self.lifes - 1
                el.kill()
        if self.lifes == 0:
            need = self.tile_type + '_bw'
            self.image = tile_images[need]
            self.is_died = 1


class UI_counter(pygame.sprite.Sprite):
    def __init__(self, tile_type, count, x, y):
        self.tile_type = tile_type
        if tile_type == 'lifes':
            super().__init__(ui_group)
            self.count = count
            self.name = tile_type + str(self.count)
            self.image = tile_images[self.name]
            self.rect = self.image.get_rect().move(x, y)
        elif tile_type == 'energy':
            super().__init__(ui_group)
            self.count = count
            self.name = tile_type + str((self.count - 1) // 20 + 1)
            self.image = tile_images[self.name]
            self.rect = self.image.get_rect().move(x, y)
        elif tile_type == 'ui_fon':
            super().__init__(ui_group)
            self.count = count
            self.name = tile_type
            self.image = tile_images[self.name]
            self.rect = self.image.get_rect().move(x, y)

    def update(self):
        if self.tile_type == 'lifes':
            super().__init__(ui_group)
            self.name = self.tile_type + str(self.count)
            self.image = tile_images[self.name]
        elif self.tile_type == 'energy':
            super().__init__(ui_group)
            self.name = self.tile_type + str((self.count - 1) // 20 + 1)
            self.image = tile_images[self.name]


class Hero(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        if tile_type == 'elf':
            super().__init__(hero_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.rotation = 'right'
        self.v = 4
        UI_counter('ui_fon', 5, tile_width - 5, tile_height - 5)
        self.count_lifes = UI_counter('lifes', 5, tile_width, tile_height)
        self.count_energy = UI_counter('energy', 100, tile_width, tile_height * 2)
        self.has_gun = 0

    def got_gun(self, type_gun):
        pict = 'elf_' + type_gun + '.png'
        hero.image = pygame.transform.scale(load_image(pict), (tile_width, tile_height))
        if hero.rotation == 'left':
            hero.image = pygame.transform.flip(self.image, True, False)
        self.has_gun = 1

    def action(self):
        for el in box_group:
            if (abs(hero.rect[0] - el.rect[0]) <= tile_width) and (
                    abs(hero.rect[1] - el.rect[1]) <= tile_height) and not el.opened:
                el.need_to_open = 1
            elif (abs(hero.rect[0] - el.rect[0]) <= tile_width) and (
                    abs(hero.rect[1] - el.rect[1]) <= tile_height) and el.opened:
                el.weapon_is_taken = 1
                el.weapon.image = pygame.transform.scale(load_image('None.png'), (tile_width, tile_height))
                hero.got_gun(el.weapon.type_gun)

    def move(self, dx, dy):
        if self.cur_scene == 'home':
            all_right = 1
            for el in home_sprites:
                el.rect = pygame.rect.Rect(el.rect[0] - dx * self.v, el.rect[1] - dy * self.v,
                                           el.rect[2],
                                           el.rect[3])
            if pygame.sprite.spritecollideany(self, exit_group):
                self.cur_scene = 'level'
            if (pygame.sprite.spritecollideany(self, necromancer_group)
                    or pygame.sprite.spritecollideany(self, empty_group)
                    or pygame.sprite.spritecollideany(self, wall_home_group)
                    or pygame.sprite.spritecollideany(self, guitar_group)
                    or pygame.sprite.spritecollideany(self, dino_group)):
                all_right = 0
                for el in home_sprites:
                    el.rect = pygame.rect.Rect(el.rect[0] + dx * self.v, el.rect[1] + dy * self.v,
                                               el.rect[2],
                                               el.rect[3])
            if dx == -1 and self.rotation == 'right' and all_right:
                self.image = pygame.transform.flip(self.image, True, False)
                self.rotation = 'left'
            elif dx == 1 and self.rotation == 'left' and all_right:
                self.image = pygame.transform.flip(self.image, True, False)
                self.rotation = 'right'
        if self.cur_scene == 'level':
            all_right = 1
            for el in level_sprites:
                el.rect = pygame.rect.Rect(el.rect[0] - dx * self.v, el.rect[1] - dy * self.v,
                                           el.rect[2],
                                           el.rect[3])
            if (pygame.sprite.spritecollideany(
                    self, box_group) or pygame.sprite.spritecollideany(self, empty_group)
                    or pygame.sprite.spritecollideany(self, wall_group)):
                all_right = 0
                for el in level_sprites:
                    el.rect = pygame.rect.Rect(el.rect[0] + dx * self.v, el.rect[1] + dy * self.v,
                                               el.rect[2],
                                               el.rect[3])
            if dx == -1 and self.rotation == 'right' and all_right:
                self.image = pygame.transform.flip(self.image, True, False)
                self.rotation = 'left'
            elif dx == 1 and self.rotation == 'left' and all_right:
                self.image = pygame.transform.flip(self.image, True, False)
                self.rotation = 'right'
            if pygame.sprite.spritecollideany(self, portal_group):
                loading()

    def shoot(self):
        if hero.count_energy.count > 0:
            Fire(self.rect[0], self.rect[1])
            hero.count_energy.count = hero.count_energy.count - 1


class Fire(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(level_sprites, fire_group)
        self.image = tile_images['fire']
        if hero.rotation == 'left':
            self.x = x - self.image.get_rect()[2]
            self.y = y + self.image.get_rect()[3]
        else:
            self.x = x + hero.rect[2]
            self.y = y + self.image.get_rect()[3]
        self.rect = self.image.get_rect().move(self.x, self.y)
        self.v_fire = 2

        self.to_where = [0, 0]
        for el in monsters_group:
            if (abs(el.rect[0] - self.rect[0]) <= (tile_width * 5)) and (
                    abs(el.rect[1] - self.rect[1]) <= (tile_width * 5)):
                delta_x = (self.rect[0] + self.rect[2] // 2) - (el.rect[0] + el.rect[2])
                delta_y = (self.rect[1] + self.rect[3] // 2) - (el.rect[1] + el.rect[3])
                self.to_where = [- delta_x / (abs(delta_x) + abs(delta_y)), - delta_y / (abs(delta_x) + abs(delta_y))]
        while self.to_where == [0, 0]:
            self.to_where = [randint(-1, 1), randint(-1, 1)]

    def update(self):
        self.rect = pygame.rect.Rect(self.rect[0] + self.v_fire * self.to_where[0],
                                     self.rect[1] + self.v_fire * self.to_where[1],
                                     self.rect[2],
                                     self.rect[3])


def loading():
    start_ticks = pygame.time.get_ticks()  # starter tick

    font_loading = pygame.font.Font('data/Undertale-Battle-Font.ttf', 50)
    text_loading = font_loading.render('LOADING', True, (255, 255, 255))
    textRect_loading = text_loading.get_rect()
    AnimatedSprite(['cat1', 'cat2', 'cat3', 'cat4', 'cat5', 'cat6', 'cat7', 'cat8', 'cat9'], width // 2 - 120,
                   height // 2 - 180, width // 2, width // 2, 0.003, cat_loading_group)
    while True:
        screen.fill(pygame.Color('black'))
        textRect_loading.center = (width // 2, height // 2 + 100)
        screen.blit(text_loading, textRect_loading)
        cat_loading_group.update()
        cat_loading_group.draw(screen)

        seconds = (pygame.time.get_ticks() - start_ticks) / 1000  # calculate how many seconds

        # где то здесь пропишешь выход из loading и начало след уровня
        pygame.display.flip()
        if seconds > 5:  # if more than 10 seconds close the game
            terminate()


'''class Enemy(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        if tile_type == 'elf':
            super().__init__(hero_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y - (tile_height / 7 * 4))
'''


class UI(pygame.sprite.Sprite):
    def __init__(self, tile_type, x, y):
        self.tile_type = tile_type
        if tile_type == 'close':
            super().__init__(ui_group)
        elif tile_type == 'p':
            super().__init__(ui_group)
        elif tile_type == 'pkm':
            super().__init__(ui_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(x, y)


class UI_home(pygame.sprite.Sprite):
    def __init__(self, tile_type, x, y):
        self.tile_type = tile_type
        if tile_type == 'close_home':
            super().__init__(ui_home_group)
        elif tile_type == 'coin_fon':
            super().__init__(ui_home_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(x, y)


def generate_level(level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == 'H':
                center = [x, y]
    x_screen = width // tile_width
    y_screen = height // tile_height
    x_screen_center = x_screen // 2
    y_screen_center = y_screen // 2
    dx = x_screen_center - center[0]
    dy = y_screen_center - center[1]
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == 'e':
                Tile('empty_level', x + dx, y + dy)
            elif level[y][x] == 'wl':
                Tile('wall_left', x + dx, y + dy)
            elif level[y][x] == 'wr':
                Tile('wall_right', x + dx, y + dy)
            elif level[y][x] == 'sl':
                Tile('side_left', x + dx, y + dy)
            elif level[y][x] == 'sr':
                Tile('side_right', x + dx, y + dy)
            elif level[y][x] == 'dl':
                Tile('down_left', x + dx, y + dy)
            elif level[y][x] == 'dr':
                Tile('down_right', x + dx, y + dy)
            elif level[y][x] == 'f':
                Tile('floor', x + dx, y + dy)
            elif level[y][x] == 'H':
                Tile('floor', x + dx, y + dy)
                hero.rect = pygame.rect.Rect((x + dx) * tile_width, (y + dy) * tile_height,
                                             hero.rect[2],
                                             hero.rect[3])
            elif level[y][x] == 'p1':
                Tile('floor', x + dx, y + dy)
                AnimatedSprite(['11', '21', '31', '41'], (x + dx) * tile_width, (y + dy) * tile_height, tile_width,
                               tile_height, 0.05, level_sprites, portal_group)
            elif level[y][x] == 'p2':
                Tile('floor', x + dx, y + dy)
                AnimatedSprite(['12', '22', '32', '42'], (x + dx) * tile_width, (y + dy) * tile_height, tile_width,
                               tile_height, 0.05, level_sprites, portal_group)
            elif level[y][x] == 'p3':
                Tile('floor', x + dx, y + dy)
                AnimatedSprite(['13', '23', '33', '43'], (x + dx) * tile_width, (y + dy) * tile_height, tile_width,
                               tile_height, 0.05, level_sprites, portal_group)
            elif level[y][x] == 'p4':
                Tile('floor', x + dx, y + dy)
                AnimatedSprite(['14', '24', '34', '44'], (x + dx) * tile_width, (y + dy) * tile_height, tile_width,
                               tile_height, 0.05, level_sprites, portal_group)
            elif level[y][x] == 'b':
                Tile('floor_fon', x + dx, y + dy)
                Box(x + dx, y + dy)
            elif level[y][x] == 'or':
                Tile('floor', x + dx, y + dy)
                Orc('orc', x + dx, y + dy)
    # return hero


def generate_home(level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == 'H':
                center = [x, y]
    x_screen = width // tile_width
    y_screen = height // tile_height
    x_screen_center = x_screen // 2
    y_screen_center = y_screen // 2
    dx = x_screen_center - center[0]
    dy = y_screen_center - center[1]
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == 'f':
                Tile('floor_home', x + dx, y + dy)
            elif level[y][x] == 'e':
                Tile('empty_home', x + dx, y + dy)
            elif level[y][x] == 'w':
                Tile('wall_home', x + dx, y + dy)
            elif level[y][x] == 'el':
                Tile('exit_left', x + dx, y + dy)
            elif level[y][x] == 'er':
                Tile('exit_right', x + dx, y + dy)
            elif level[y][x] == 'c1':
                Tile('cover1', x + dx, y + dy)
            elif level[y][x] == 'c2':
                Tile('cover2', x + dx, y + dy)
            elif level[y][x] == 'c3':
                Tile('cover3', x + dx, y + dy)
            elif level[y][x] == 'c4':
                Tile('cover4', x + dx, y + dy)
            elif level[y][x] == 'c5':
                Tile('cover5', x + dx, y + dy)
            elif level[y][x] == 'c6':
                Tile('cover6', x + dx, y + dy)
            elif level[y][x] == 'c7':
                Tile('cover7', x + dx, y + dy)
            elif level[y][x] == 'c8':
                Tile('cover8', x + dx, y + dy)
            elif level[y][x] == 'H':
                Tile('floor_home', x + dx, y + dy)
                hero = Hero('elf', x + dx, y + dy)
            elif level[y][x] == 'N':
                Tile('floor_home_fon', x + dx, y + dy)
                necromancer = Necromancer(x + dx, y + dy)
            elif level[y][x] == 'o1':
                Tile('floor_home_fon', x + dx, y + dy)
                Tile('okult1', x + dx, y + dy)
            elif level[y][x] == 'o2':
                Tile('floor_home_fon', x + dx, y + dy)
                Tile('okult2', x + dx, y + dy)
            elif level[y][x] == 'o3':
                Tile('floor_home_fon', x + dx, y + dy)
                Tile('okult3', x + dx, y + dy)
            elif level[y][x] == 'o4':
                Tile('floor_home_fon', x + dx, y + dy)
                Tile('okult4', x + dx, y + dy)
            elif level[y][x] == 'g1':
                Tile('floor_home_fon', x + dx, y + dy)
                Tile('guitar1', x + dx, y + dy)
            elif level[y][x] == 'g2':
                Tile('floor_home_fon', x + dx, y + dy)
                Tile('guitar2', x + dx, y + dy)
            elif level[y][x] == 'g3':
                Tile('floor_home_fon', x + dx, y + dy)
                Tile('guitar3', x + dx, y + dy)
            elif level[y][x] == 'd':
                Tile('floor_home_fon', x + dx, y + dy)
                dino = Dino(x + dx, y + dy)
    return hero, necromancer, dino


if __name__ in '__main__':
    pygame.init()
    my_font = pygame.font.Font('data/Undertale-Battle-Font.ttf', 50)

    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    # screen = pygame.display.set_mode((500, 500))
    size = screen.get_size()
    width, height = size

    start_screen(screen)

    tile_width = tile_height = 60
    tile_images = {
        'floor': pygame.transform.scale(load_image('floor_1.png'), (tile_width, tile_height)),
        'floor_fon': pygame.transform.scale(load_image('floor_1.png'), (tile_width, tile_height)),
        'wall_left': pygame.transform.scale(load_image('wall_left.png'), (tile_width, tile_height)),
        'wall_right': pygame.transform.scale(load_image('wall_right.png'), (tile_width, tile_height)),
        'side_left': pygame.transform.scale(load_image('wall_side_mid_left.png'), (tile_width, tile_height)),
        'side_right': pygame.transform.scale(load_image('wall_side_mid_right.png'), (tile_width, tile_height)),
        'down_left': pygame.transform.scale(load_image('down_left.png'), (tile_width, tile_height)),
        'down_right': pygame.transform.scale(load_image('down_right.png'), (tile_width, tile_height)),
        'empty_home': pygame.transform.scale(load_image('black.png'), (tile_width, tile_height)),
        'empty_level': pygame.transform.scale(load_image('black.png'), (tile_width, tile_height)),
        'close': pygame.transform.scale(load_image('close.png'), (tile_width, tile_height)),
        'p': pygame.transform.scale(load_image('p.png'), (tile_width, tile_height)),
        'pkm': pygame.transform.scale(load_image('ПКМ.png'), (tile_width, tile_height)),
        'elf': pygame.transform.scale(load_image('elf_square.png'),
                                      (tile_width, tile_height)),
        'wall_home': pygame.transform.scale(load_image('wall.png'), (tile_width, tile_height)),
        'floor_home': pygame.transform.scale(load_image('floor_home.png'), (tile_width, tile_height)),
        'floor_home_fon': pygame.transform.scale(load_image('floor_home.png'), (tile_width, tile_height)),
        'exit_left': pygame.transform.scale(load_image('exit_left.png'), (tile_width, tile_height)),
        'exit_right': pygame.transform.scale(load_image('exit_right.png'), (tile_width, tile_height)),
        'cover1': pygame.transform.scale(load_image('cover1.png'), (tile_width, tile_height)),
        'cover2': pygame.transform.scale(load_image('cover2.png'), (tile_width, tile_height)),
        'cover3': pygame.transform.scale(load_image('cover3.png'), (tile_width, tile_height)),
        'cover4': pygame.transform.scale(load_image('cover4.png'), (tile_width, tile_height)),
        'cover5': pygame.transform.scale(load_image('cover5.png'), (tile_width, tile_height)),
        'cover6': pygame.transform.scale(load_image('cover6.png'), (tile_width, tile_height)),
        'cover7': pygame.transform.scale(load_image('cover7.png'), (tile_width, tile_height)),
        'cover8': pygame.transform.scale(load_image('cover8.png'), (tile_width, tile_height)),
        'necromancer': pygame.transform.scale(load_image('necromancer_idle_anim_f1.png'), (tile_width, tile_height)),
        'okult1': pygame.transform.scale(load_image('okult1.png'), (tile_width, tile_height)),
        'okult2': pygame.transform.scale(load_image('okult2.png'), (tile_width, tile_height)),
        'okult3': pygame.transform.scale(load_image('okult3.png'), (tile_width, tile_height)),
        'okult4': pygame.transform.scale(load_image('okult4.png'), (tile_width, tile_height)),
        'box': pygame.transform.scale(load_image('chest_empty_open_anim_f0.png'), (tile_width, tile_height)),
        # '1black': pygame.transform.scale(load_image('1black.png'), (tile_width, tile_height)),
        # '2black': pygame.transform.scale(load_image('2black.png'), (tile_width, tile_height)),
        '3black': pygame.transform.scale(load_image('3black.png'), (tile_width, tile_height)),
        # '4black': pygame.transform.scale(load_image('4black.png'), (tile_width, tile_height)),
        # '5black': pygame.transform.scale(load_image('5black.png'), (tile_width, tile_height)),
        # '6black': pygame.transform.scale(load_image('6black.png'), (tile_width, tile_height)),
        '7black': pygame.transform.scale(load_image('7black.png'), (tile_width, tile_height)),
        # '8black': pygame.transform.scale(load_image('8black.png'), (tile_width, tile_height)),
        # '1gold': pygame.transform.scale(load_image('1gold.png'), (tile_width, tile_height)),
        # '2gold': pygame.transform.scale(load_image('2gold.png'), (tile_width, tile_height)),
        '3gold': pygame.transform.scale(load_image('3gold.png'), (tile_width, tile_height)),
        # '4gold': pygame.transform.scale(load_image('4gold.png'), (tile_width, tile_height)),
        # '5gold': pygame.transform.scale(load_image('5gold.png'), (tile_width, tile_height)),
        # '6gold': pygame.transform.scale(load_image('6gold.png'), (tile_width, tile_height)),
        '7gold': pygame.transform.scale(load_image('7gold.png'), (tile_width, tile_height)),
        # '8gold': pygame.transform.scale(load_image('8gold.png'), (tile_width, tile_height)),
        # '1blue': pygame.transform.scale(load_image('1blue.png'), (tile_width, tile_height)),
        # '2blue': pygame.transform.scale(load_image('2blue.png'), (tile_width, tile_height)),
        '3blue': pygame.transform.scale(load_image('3blue.png'), (tile_width, tile_height)),
        # '4blue': pygame.transform.scale(load_image('4blue.png'), (tile_width, tile_height)),
        # '5blue': pygame.transform.scale(load_image('5blue.png'), (tile_width, tile_height)),
        # '6blue': pygame.transform.scale(load_image('6blue.png'), (tile_width, tile_height)),
        '7blue': pygame.transform.scale(load_image('7blue.png'), (tile_width, tile_height)),
        # '8blue': pygame.transform.scale(load_image('8blue.png'), (tile_width, tile_height)),
        'cat1': pygame.transform.scale(load_image('frame_0_delay-0.12s.png'), (200, 200)),
        'cat2': pygame.transform.scale(load_image('frame_1_delay-0.12s.png'), (200, 200)),
        'cat3': pygame.transform.scale(load_image('frame_2_delay-0.12s.png'), (200, 200)),
        'cat4': pygame.transform.scale(load_image('frame_3_delay-0.12s.png'), (200, 200)),
        'cat5': pygame.transform.scale(load_image('frame_4_delay-0.12s.png'), (200, 200)),
        'cat6': pygame.transform.scale(load_image('frame_5_delay-0.12s.png'), (200, 200)),
        'cat7': pygame.transform.scale(load_image('frame_6_delay-0.12s.png'), (200, 200)),
        'cat8': pygame.transform.scale(load_image('frame_7_delay-0.12s.png'), (200, 200)),
        'cat9': pygame.transform.scale(load_image('frame_8_delay-0.12s.png'), (200, 200)),
        '11': pygame.transform.scale(load_image('11.png'), (tile_width, tile_height)),
        '21': pygame.transform.scale(load_image('21.png'), (tile_width, tile_height)),
        '31': pygame.transform.scale(load_image('31.png'), (tile_width, tile_height)),
        '41': pygame.transform.scale(load_image('41.png'), (tile_width, tile_height)),

        '12': pygame.transform.scale(load_image('12.png'), (tile_width, tile_height)),
        '22': pygame.transform.scale(load_image('22.png'), (tile_width, tile_height)),
        '32': pygame.transform.scale(load_image('32.png'), (tile_width, tile_height)),
        '42': pygame.transform.scale(load_image('42.png'), (tile_width, tile_height)),

        '13': pygame.transform.scale(load_image('13.png'), (tile_width, tile_height)),
        '23': pygame.transform.scale(load_image('23.png'), (tile_width, tile_height)),
        '33': pygame.transform.scale(load_image('33.png'), (tile_width, tile_height)),
        '43': pygame.transform.scale(load_image('43.png'), (tile_width, tile_height)),

        '14': pygame.transform.scale(load_image('14.png'), (tile_width, tile_height)),
        '24': pygame.transform.scale(load_image('24.png'), (tile_width, tile_height)),
        '34': pygame.transform.scale(load_image('34.png'), (tile_width, tile_height)),
        '44': pygame.transform.scale(load_image('44.png'), (tile_width, tile_height)),

        'orc': pygame.transform.scale(load_image('orc_warrior_idle_anim_f0.png'), (tile_width, tile_height)),
        'orc_bw': pygame.transform.scale(load_image('orc_warrior_idle_anim_f0_bw.png'), (tile_width, tile_height)),
        'lifes0': pygame.transform.scale(load_image('lifes0.png'), (180, 48)),
        'lifes1': pygame.transform.scale(load_image('lifes1.png'), (180, 48)),
        'lifes2': pygame.transform.scale(load_image('lifes2.png'), (180, 48)),
        'lifes3': pygame.transform.scale(load_image('lifes3.png'), (180, 48)),
        'lifes4': pygame.transform.scale(load_image('lifes4.png'), (180, 48)),
        'lifes5': pygame.transform.scale(load_image('lifes5.png'), (180, 48)),
        'energy0': pygame.transform.scale(load_image('energy0.png'), (180, 48)),
        'energy1': pygame.transform.scale(load_image('energy1.png'), (180, 48)),
        'energy2': pygame.transform.scale(load_image('energy2.png'), (180, 48)),
        'energy3': pygame.transform.scale(load_image('energy3.png'), (180, 48)),
        'energy4': pygame.transform.scale(load_image('energy4.png'), (180, 48)),
        'energy5': pygame.transform.scale(load_image('energy5.png'), (180, 48)),
        'ui_fon': pygame.transform.scale(load_image('ui_fon1.png'), (186, 123)),
        'guitar1': pygame.transform.scale(load_image('g1.png'), (tile_width, tile_height)),
        'guitar2': pygame.transform.scale(load_image('g2.png'), (tile_width, tile_height)),
        'guitar3': pygame.transform.scale(load_image('g3.png'), (tile_width, tile_height)),
        'dino': pygame.transform.scale(load_image('lizard_m_idle_anim_f0.png'), (tile_width, tile_height)),
        'coin_fon': pygame.transform.scale(load_image('coin_fon.png'), (144, 56)),
        'close_home': pygame.transform.scale(load_image('close.png'), (tile_width, tile_height)),
        'fire': pygame.transform.scale(load_image('shot.png'), (tile_width // 2, tile_height // 2)),
    }

    home_sprites = pygame.sprite.Group()
    wall_home_group = pygame.sprite.Group()
    floor_home_group = pygame.sprite.Group()
    exit_group = pygame.sprite.Group()
    necromancer_group = pygame.sprite.Group()
    dino_group = pygame.sprite.Group()
    guitar_group = pygame.sprite.Group()
    empty_group = pygame.sprite.Group()
    ui_home_group = pygame.sprite.Group()

    level_sprites = pygame.sprite.Group()
    hero_group = pygame.sprite.Group()
    floor_group = pygame.sprite.Group()
    wall_group = pygame.sprite.Group()
    ui_group = pygame.sprite.Group()
    portal_group = pygame.sprite.Group()
    box_group = pygame.sprite.Group()
    weapon_group = pygame.sprite.Group()
    monsters_group = pygame.sprite.Group()
    fire_group = pygame.sprite.Group()

    cat_loading_group = pygame.sprite.Group()

    # '1black', '2black', '3black', '4black', '5black', '6black', '7black', '8black',
    weapon = ['3gold', '3blue', '3black', '7gold', '7blue', '7black']

    filename = 'home.txt'
    home_map = load_level(filename)
    home_map = [el.split() for el in home_map]
    hero, necromancer, dino = generate_home(home_map)
    hero.cur_scene = 'home'
    close_home = UI_home('close_home', width - tile_width - 50, 50)
    money = UI_home('coin_fon', tile_width, tile_height)
    home_screen(screen)

    filename = 'level1.txt'
    level_map = load_level(filename)
    level_map = [el.split() for el in level_map]
    hero.cur_scene = 'level'
    generate_level(level_map)

    button_pkm = UI('pkm', tile_width, height - tile_height * 2)
    button_p = UI('p', 2 * tile_width + 10, height - tile_height * 2)
    close = UI('close', width - tile_width - 50, 50)

    running = True
    fps = 60
    clock = pygame.time.Clock()
    while running:
        clock.tick(fps)
        screen.fill(pygame.Color('black'))

        for el in monsters_group:
            if (abs(el.rect[0] - hero.rect[0]) <= (tile_width * 5)) and (
                    abs(el.rect[1] - hero.rect[1]) <= (tile_width * 5)):
                if el.rect[0] < hero.rect[0] and el.rect[1] < hero.rect[1]:
                    el.move(1, 1)
                elif el.rect[0] > hero.rect[0] and el.rect[1] > hero.rect[1]:
                    el.move(-1, -1)
                elif el.rect[0] < hero.rect[0] and el.rect[1] > hero.rect[1]:
                    el.move(1, -1)
                elif el.rect[0] > hero.rect[0] and el.rect[1] < hero.rect[1]:
                    el.move(-1, 1)

                elif el.rect[0] == hero.rect[0] and el.rect[1] > hero.rect[1]:
                    el.move(0, -1)
                elif el.rect[0] == hero.rect[0] and el.rect[1] < hero.rect[1]:
                    el.move(0, 1)
                elif el.rect[0] < hero.rect[0] and el.rect[1] == hero.rect[1]:
                    el.move(1, 0)
                elif el.rect[0] > hero.rect[0] and el.rect[1] == hero.rect[1]:
                    el.move(-1, 0)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                clicked_sprites = [el for el in ui_group if el.rect.collidepoint(pos)]
                for el in clicked_sprites:
                    if el.tile_type == 'close':
                        terminate()
                if hero.has_gun:
                    hero.shoot()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    hero.action()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            hero.move(-1, 0)
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            hero.move(1, 0)
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            hero.move(0, -1)
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            hero.move(0, 1)

        level_sprites.update()
        level_sprites.draw(screen)
        monsters_group.draw(screen)
        hero_group.draw(screen)
        ui_group.draw(screen)

        hero.count_lifes.update()
        hero.count_energy.update()

        fire_group.update()

        pygame.display.flip()
    terminate()
