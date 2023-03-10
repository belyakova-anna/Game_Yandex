import sqlite3
import pygame
import sys
import os
from random import choice, randint


def terminate():
    pygame.quit()
    sys.exit()


class AnimatedSprite(pygame.sprite.Sprite):  # анимация
    def __init__(self, imgs, x, y, x_size, y_size, time, *group):  # на вход названия картинок, по которым
        # их можно найти в словаре tile_images, координаты, размер, время смены одной картинки из анимации,
        # группы спрайтов, к которым относится объект
        super().__init__(*group)
        self.time = time
        self.frames = [tile_images[el] for el in imgs]
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = pygame.Rect(x, y, x_size, y_size)

    def update(self):
        self.cur_frame = (self.cur_frame + self.time) % len(self.frames)
        self.image = self.frames[int(self.cur_frame)]


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def start_screen(screen):  # начальный экран
    font_start = pygame.font.Font('data/Undertale-Battle-Font.ttf', 50)

    text_play = font_start.render('play', True, (0, 0, 0))
    text_start = font_start.render('Civil defense', True, (255, 255, 255))
    textRect_play = text_start.get_rect()
    textRect_start = text_start.get_rect()

    fon = pygame.transform.scale(load_image('fon1.jpeg'), (width, height))
    screen.blit(fon, (0, 0))

    textRect_start.center = (width // 2, height // 2)
    textRect_play.center = (width // 2 + textRect_play[2] // 3 + 10, height // 4 * 3 + textRect_play[3] // 2)
    screen.blit(text_start, textRect_start)
    screen.blit(text_play, textRect_play)

    UI(ui_start, 'for_text', width // 2 - 106, height // 4 * 3)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                clicked_sprites = [el for el in ui_start if el.rect.collidepoint(pos)]
                for el in clicked_sprites:  # если нажата кнопка play
                    if el.tile_type == 'for_text':
                        return
            if event.type == pygame.QUIT:
                terminate()
        ui_start.draw(screen)
        screen.blit(text_play, textRect_play)
        pygame.display.flip()


def to_time_format(time):  # вспомогательная функция
    # принимает число, возвращает строку в формате мин:сек
    time = [str(time // 60), str(time % 60)]
    if len(str(time[0])) < 2:
        time[0] = '0' + time[0]
    if len(str(time[1])) < 2:
        time[1] = '0' + time[1]
    time = time[0] + ':' + time[1]
    return time


def died_screen(screen):  # экран подсчёта достижений
    global home, cat_died_group

    for el in coin_group:
        el.kill()
    cat_died_group = pygame.sprite.Group()

    font_died = pygame.font.Font('data/Undertale-Battle-Font.ttf', 50)

    text_died = font_died.render('Игра завершена', True, (255, 255, 255))
    textRect_died = text_died.get_rect()

    font_died_little = pygame.font.Font('data/Undertale-Battle-Font.ttf', 50)

    # количество убитых монстров
    text_count_killed = font_died_little.render(str(hero.count_killed), True, (255, 255, 255))
    textRect_count_killed = text_count_killed.get_rect()

    # количество собранных монет
    text_count_money = font_died_little.render(str(hero.count_money_from_level), True, (255, 255, 255))
    textRect_count_money = text_count_money.get_rect()

    # время с начала игры
    text_clock = font_died_little.render(to_time_format(pygame.time.get_ticks() // 1000 - time_start), True,
                                         (255, 255, 255))
    textRect_clock = text_clock.get_rect()

    fon = pygame.transform.scale(load_image('died_fon.png'), (width, height))
    screen.blit(fon, (0, 0))

    UI(ui_died_group, 'close', width - tile_width - 50, 50)
    UI(ui_died_group, 'clock', (width // 8) * 1, height // 2 + 50)
    UI(ui_died_group, 'moneta_screen', (width // 8) * 3.5, height // 2 + 50)
    UI(ui_died_group, 'count_dead', (width // 8) * 6, height // 2 + 50)
    UI(ui_died_to_home, 'skip', (width // 2) - 126, height - 160)
    textRect_count_killed.center = ((width // 8) * 6 + tile_width + 30, height // 2 + tile_height // 2 + 50)
    textRect_count_money.center = ((width // 8) * 3.5 + tile_width + 30, height // 2 + tile_height // 2 + 50)
    textRect_clock.center = ((width // 8) * 1 + tile_width + 90, height // 2 + tile_height // 2 + 50)
    textRect_died.center = (width // 2, 70)
    screen.blit(text_died, textRect_died)
    screen.blit(text_count_killed, textRect_count_killed)
    screen.blit(text_count_money, textRect_count_money)
    screen.blit(text_clock, textRect_clock)

    AnimatedSprite(['1orange', '2orange', '3orange', '4orange'], width // 2 - 120,
                   height // 2 - 220, width // 2, width // 2, 0.045, cat_died_group)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                clicked_sprites = [el for el in ui_died_group if el.rect.collidepoint(pos)]
                for el in clicked_sprites:  # нажать на крестик = закрыть игру
                    if el.tile_type == 'close':
                        terminate()
                clicked_sprites = [el for el in ui_died_to_home if el.rect.collidepoint(pos)]
                for el in clicked_sprites:  # нажать на кнопку = вернуться на домашний экран игры
                    if el.tile_type == 'skip':
                        hero.start_game = 1
                        home = 1
                        return
            if event.type == pygame.QUIT:
                terminate()

        screen.blit(fon, (0, 0))

        screen.blit(text_count_killed, textRect_count_killed)
        screen.blit(text_died, textRect_died)
        screen.blit(text_count_money, textRect_count_money)
        screen.blit(text_clock, textRect_clock)
        ui_died_to_home.draw(screen)
        ui_died_group.draw(screen)

        cat_died_group.update()
        cat_died_group.draw(screen)
        pygame.display.flip()


def change_hero(el):  # смена скина
    global home, hero_type
    with open('data/home.txt', 'r') as f:  # считываем файл
        a = f.read()
    with open('data/home.txt', 'w') as f:  # изменяем содержимое файла
        if el.tile_type == 'necromancer' and hero.tile_type == 'elf':
            a = a.replace('N', 'E')
            f.write(a)
        elif el.tile_type == 'dino' and hero.tile_type == 'elf':
            a = a.replace('D', 'E')
            f.write(a)
        elif el.tile_type == 'elf' and hero.tile_type == 'necromancer':
            a = a.replace('E', 'N')
            f.write(a)
        elif el.tile_type == 'dino' and hero.tile_type == 'necromancer':
            a = a.replace('D', 'N')
            f.write(a)
        elif el.tile_type == 'necromancer' and hero.tile_type == 'dino':
            a = a.replace('N', 'D')
            f.write(a)
        elif el.tile_type == 'elf' and hero.tile_type == 'dino':
            a = a.replace('E', 'D')
            f.write(a)

        elif el.tile_type == 'elf' and hero.tile_type == 'knight':
            a = a.replace('E', 'K')
            f.write(a)
        elif el.tile_type == 'knight' and hero.tile_type == 'elf':
            a = a.replace('K', 'E')
            f.write(a)
        elif el.tile_type == 'necromancer' and hero.tile_type == 'knight':
            a = a.replace('N', 'K')
            f.write(a)
        elif el.tile_type == 'knight' and hero.tile_type == 'necromancer':
            a = a.replace('K', 'N')
            f.write(a)
        elif el.tile_type == 'dino' and hero.tile_type == 'knight':
            a = a.replace('D', 'K')
            f.write(a)
        elif el.tile_type == 'knight' and hero.tile_type == 'dino':
            a = a.replace('K', 'D')
            f.write(a)
        else:
            f.write(a)
    hero_type = el.tile_type
    home = 1


def home_screen(screen):  # домашняя комната
    global home, hero
    fps = 60
    clock = pygame.time.Clock()

    font1 = pygame.font.Font('data/Undertale-Battle-Font.ttf', 20)

    text_necromancer = font1.render('Некромант', True, (255, 255, 255))  # имя некроманта
    textRect_necromancer = text_necromancer.get_rect()

    text_necromancer_buy = font1.render('купить 50', True, (255, 255, 255))  # цена скина некроманта
    textRect_necromancer_buy = text_necromancer_buy.get_rect()

    text_dino = font1.render('Дино', True, (255, 255, 255))  # имя динозавтра
    textRect_dino = text_dino.get_rect()

    text_dino_buy = font1.render('купить 50', True, (255, 255, 255))  # цена скина динозавра
    textRect_dino_buy = text_dino_buy.get_rect()

    text_elf = font1.render('Эльф', True, (255, 255, 255))  # имя эльфа
    textRect_elf = text_elf.get_rect()

    text_elf_buy = font1.render('купить 50', True, (255, 255, 255))  # цена скина эльфа
    textRect_elf_buy = text_elf_buy.get_rect()

    text_knight = font1.render('Рыцарь', True, (255, 255, 255))  # имя рыцаря
    textRect_knight = text_elf.get_rect()

    text_knight_buy = font1.render('купить 50', True, (255, 255, 255))  # цена скина рыцаря
    textRect_knight_buy = text_elf_buy.get_rect()

    font2 = pygame.font.Font('data/Undertale-Battle-Font.ttf', 40)

    text_money = font2.render(str(hero.count_money), True, (0, 0, 0))  # накопленные монеты
    textRect_money = text_money.get_rect()
    textRect_money.center = (tile_width * 2.5, tile_height * 1.5)
    while True:
        clock.tick(fps)
        screen.fill(pygame.Color('black'))
        home_sprites.draw(screen)
        hero_group.draw(screen)
        ui_home_group.draw(screen)
        if hero.cur_scene == 'level':
            home = 0
            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONUP:
                home_pos = pygame.mouse.get_pos()
                home_clicked_sprites = [el for el in ui_home_group if el.rect.collidepoint(home_pos)]
                for el in home_clicked_sprites:
                    if el.tile_type == 'close_home':  # нажат крестик = завершаем сеанс игры
                        terminate()
                    if el.tile_type == 'is_sound':  # нажата кнопка изменения состояния звука
                        el.play = (el.play + 1) % 2
                        if el.play:
                            el.image = tile_images['is_sound']
                            pygame.mixer.Channel(0).unpause()
                        else:
                            el.image = tile_images['isnt_sound']
                            pygame.mixer.Channel(0).pause()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # нажата клавиша p для смены персонажа
                    for el in skins_group:
                        if (abs(hero.rect[0] - el.rect[0]) <= tile_width) and (
                                abs(hero.rect[1] - el.rect[1]) <= tile_height) and (
                                el.tile_type != hero.tile_type) and el.available:
                            change_hero(el)
                            return
                        elif (abs(hero.rect[0] - el.rect[0]) <= tile_width) and (
                                abs(hero.rect[1] - el.rect[1]) <= tile_height) and (
                                el.tile_type != hero.tile_type) and (hero.count_money >= 50):
                            el.available = 1
                            hero.count_money = hero.count_money - 50
                            cur.execute("""DELETE from constants""")
                            cur.execute("""INSERT INTO constants (coins) VALUES(?)""", (hero.count_money,))
                            db.commit()
                            if el.tile_type == 'elf':
                                n = cur.execute("""SELECT necromancer FROM skins""").fetchall()[0][0]
                                d = cur.execute("""SELECT dino FROM skins""").fetchall()[0][0]
                                k = cur.execute("""SELECT knight FROM skins""").fetchall()[0][0]
                                cur.execute("""DELETE from skins""")
                                cur.execute("""INSERT INTO skins VALUES(?, ?, ?, ?)""", (n, d, 1, k))
                                db.commit()
                            elif el.tile_type == 'dino':
                                n = cur.execute("""SELECT necromancer FROM skins""").fetchall()[0][0]
                                e = cur.execute("""SELECT elf FROM skins""").fetchall()[0][0]
                                k = cur.execute("""SELECT knight FROM skins""").fetchall()[0][0]
                                cur.execute("""DELETE from skins""")
                                cur.execute("""INSERT INTO skins VALUES(?, ?, ?, ?)""", (n, 1, e, k))
                                db.commit()
                            elif el.tile_type == 'necromancer':
                                e = cur.execute("""SELECT elf FROM skins""").fetchall()[0][0]
                                d = cur.execute("""SELECT dino FROM skins""").fetchall()[0][0]
                                k = cur.execute("""SELECT knight FROM skins""").fetchall()[0][0]
                                cur.execute("""DELETE from skins""")
                                cur.execute("""INSERT INTO skins VALUES(?, ?, ?, ?)""", (1, d, e, k))
                                db.commit()
                            elif el.tile_type == 'knight':
                                n = cur.execute("""SELECT necromancer FROM skins""").fetchall()[0][0]
                                e = cur.execute("""SELECT elf FROM skins""").fetchall()[0][0]
                                d = cur.execute("""SELECT dino FROM skins""").fetchall()[0][0]
                                cur.execute("""DELETE from skins""")
                                cur.execute("""INSERT INTO skins VALUES(?, ?, ?, ?)""", (n, d, e, 1))
                                db.commit()
                            text_money = font2.render(str(hero.count_money), True, (0, 0, 0))
                            textRect_money = text_money.get_rect()
                            textRect_money.center = (tile_width * 2.5, tile_height * 1.5)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:  # перемещение героя
            hero.move(-1, 0)
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            hero.move(1, 0)
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            hero.move(0, -1)
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            hero.move(0, 1)
        # генерация текста при приближении к персонажу в домашней сцене
        if necromancer and (abs(hero.rect[0] - necromancer.rect[0]) <= tile_width) and (
                abs(hero.rect[1] - necromancer.rect[1]) <= tile_height):
            if necromancer.available:
                textRect_necromancer.center = (
                    necromancer.rect[0] + text_necromancer.get_rect()[2] // 4, necromancer.rect[1])
                screen.blit(text_necromancer, textRect_necromancer)
            else:
                textRect_necromancer_buy.center = (
                    necromancer.rect[0] + text_necromancer_buy.get_rect()[2] - 70, necromancer.rect[1])
                screen.blit(text_necromancer_buy, textRect_necromancer_buy)
        if dino and (abs(hero.rect[0] - dino.rect[0]) <= tile_width) and (
                abs(hero.rect[1] - dino.rect[1]) <= tile_height):
            if dino.available:
                textRect_dino.center = (dino.rect[0] + text_dino.get_rect()[2] - 10, dino.rect[1])
                screen.blit(text_dino, textRect_dino)
            else:
                textRect_dino_buy.center = (dino.rect[0] + text_dino_buy.get_rect()[2] - 70, dino.rect[1])
                screen.blit(text_dino_buy, textRect_dino_buy)
        if elf and (abs(hero.rect[0] - elf.rect[0]) <= tile_width) and (
                abs(hero.rect[1] - elf.rect[1]) <= tile_height):
            if elf.available:
                textRect_elf.center = (elf.rect[0] + text_elf.get_rect()[2] - 10, elf.rect[1])
                screen.blit(text_elf, textRect_elf)
            else:
                textRect_elf_buy.center = (elf.rect[0] + text_elf_buy.get_rect()[2] - 70, elf.rect[1])
                screen.blit(text_elf_buy, textRect_elf_buy)
        if knight and (abs(hero.rect[0] - knight.rect[0]) <= tile_width) and (
                abs(hero.rect[1] - knight.rect[1]) <= tile_height):
            if knight.available:
                textRect_knight.center = (knight.rect[0] + text_knight.get_rect()[2] - 45, knight.rect[1])
                screen.blit(text_knight, textRect_knight)
            else:
                textRect_knight_buy.center = (knight.rect[0] + text_knight_buy.get_rect()[2] - 70, knight.rect[1])
                screen.blit(text_knight_buy, textRect_knight_buy)
        screen.blit(text_money, textRect_money)
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


class Box(pygame.sprite.Sprite):  # ящик на игровой карте
    def __init__(self, inside, pos_x, pos_y):
        super().__init__(level_sprites, box_group)
        self.inside = inside
        self.image = tile_images['box']
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.need_to_open = 0
        self.opened = 0
        self.is_taken = 0

        self.frames = [pygame.transform.scale(load_image('chest_empty_open_anim_f1.png'), (tile_width, tile_height)),
                       pygame.transform.scale(load_image('chest_empty_open_anim_f2.png'), (tile_width, tile_height))]
        self.cur_frame = 0
        self.weapon = None

    def update(self):
        if self.need_to_open and not self.opened:
            self.cur_frame = (self.cur_frame + 0.05) % len(self.frames)
            self.image = self.frames[int(self.cur_frame)]
            if int(self.cur_frame) == 1 and self.inside == 'weapon':  # генерируем оружие внутри ящика
                self.opened = 1
                self.need_to_open = 0
                self.weapon = Weapon(choice(weapon), self.rect[0], self.rect[1])
            elif int(self.cur_frame) == 1 and self.inside == 'potion_lifes':  # генерируем зелье жизни внутри ящика
                self.opened = 1
                self.need_to_open = 0
                self.potion_lifes = PotionLifes(self.rect[0], self.rect[1])
            elif int(self.cur_frame) == 1 and self.inside == 'potion_energy':  # генерируем зелье энергии внутри ящика
                self.opened = 1
                self.need_to_open = 0
                self.potion_energy = PotionEnergy(self.rect[0], self.rect[1])


class PotionLifes(pygame.sprite.Sprite):  # зелье жизней внутри ящика
    def __init__(self, pos_x, pos_y):  # на вход принимает координаты
        super().__init__(level_sprites, weapon_group)
        self.image = tile_images['potion_lifes']
        self.rect = self.image.get_rect().move(
            pos_x, pos_y)


class PotionEnergy(pygame.sprite.Sprite):  # зелье энергии внутри ящика
    def __init__(self, pos_x, pos_y):  # на вход принимает координаты
        super().__init__(level_sprites, weapon_group)
        self.image = tile_images['potion_energy']
        self.rect = self.image.get_rect().move(
            pos_x, pos_y)


class Weapon(pygame.sprite.Sprite):  # оружие внутри ящика
    def __init__(self, tile_type, pos_x, pos_y):  # на вход принимает название оружие из словаря и координаты
        super().__init__(level_sprites, weapon_group)
        self.type_gun = tile_type
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            pos_x, pos_y)


class Tile(pygame.sprite.Sprite):  # плитки
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
            super().__init__(home_sprites, empty_home_group)
        elif tile_type == "empty_level":
            super().__init__(level_sprites, empty_level_group)
        elif tile_type == "dino":
            super().__init__(level_sprites, dino_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Necromancer(pygame.sprite.Sprite):  # персонаж в домашней комнате
    def __init__(self, pos_x, pos_y):
        super().__init__(home_sprites, necromancer_group, skins_group)
        self.available = cur.execute("""SELECT necromancer FROM skins""").fetchall()[0][0]
        self.tile_type = 'necromancer'
        self.image = tile_images['necromancer']
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Dino(pygame.sprite.Sprite):  # персонаж в домашней комнате
    def __init__(self, pos_x, pos_y):
        super().__init__(home_sprites, dino_group, skins_group)
        self.available = cur.execute("""SELECT dino FROM skins""").fetchall()[0][0]
        self.tile_type = 'dino'
        self.image = tile_images['dino']
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Elf(pygame.sprite.Sprite):  # персонаж в домашней комнате
    def __init__(self, pos_x, pos_y):
        super().__init__(home_sprites, elf_group, skins_group)
        self.available = cur.execute("""SELECT elf FROM skins""").fetchall()[0][0]
        self.tile_type = 'elf'
        self.image = tile_images['elf']
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Knight(pygame.sprite.Sprite):  # персонаж в домашней комнате
    def __init__(self, pos_x, pos_y):
        super().__init__(home_sprites, knight_group, skins_group)
        self.available = cur.execute("""SELECT knight FROM skins""").fetchall()[0][0]
        self.tile_type = 'knight'
        self.image = tile_images['knight']
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Monster(pygame.sprite.Sprite):  # монстр
    def __init__(self, tile_type, pos_x, pos_y):  # название монстра и его координаты
        super().__init__(level_sprites, monsters_group)
        self.tile_type = tile_type
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.rotation = 'right'
        self.v = 1
        if self.tile_type == 'orc':  # в зависимости от типа монстра у них разное количество жизней
            self.lifes = 6
        elif self.tile_type == 'imp':
            self.lifes = 3
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
                # если монстр достаточно близко к hero, то монстр за ним бежит
                if self.rect[0] >= hero.rect[0] and self.rect[1] == hero.rect[1]:
                    hero.move(- tile_width / hero.v, 0)
                elif self.rect[0] <= hero.rect[0] and self.rect[1] == hero.rect[1]:
                    hero.move(tile_width / hero.v, 0)
                elif self.rect[0] == hero.rect[0] and self.rect[1] >= hero.rect[1]:
                    hero.move(0, - tile_height / hero.v)
                elif self.rect[0] == hero.rect[0] and self.rect[1] <= hero.rect[1]:
                    hero.move(0, tile_height / hero.v)
                elif self.rect[0] <= hero.rect[0] and self.rect[1] <= hero.rect[1]:
                    hero.move(tile_width / hero.v, tile_height / hero.v)
                elif self.rect[0] >= hero.rect[0] and self.rect[1] <= hero.rect[1]:
                    hero.move(- tile_width / hero.v, tile_height / hero.v)
                elif self.rect[0] <= hero.rect[0] and self.rect[1] >= hero.rect[1]:
                    hero.move(tile_width / hero.v, - tile_height / hero.v)
                elif self.rect[0] >= hero.rect[0] and self.rect[1] >= hero.rect[1]:
                    hero.move(- tile_width / hero.v, - tile_height / hero.v)

                if self.rect[0] >= hero.rect[0] and not hero.all_right:
                    hero.move(- tile_width / hero.v, 0)
                if self.rect[0] <= hero.rect[0] and not hero.all_right:
                    hero.move(tile_width / hero.v, 0)
                if self.rect[1] >= hero.rect[1] and not hero.all_right:
                    hero.move(0, - tile_height / hero.v)
                if self.rect[1] <= hero.rect[1] and not hero.all_right:
                    hero.move(0, tile_height / hero.v)
                if self.rect[0] <= hero.rect[0] and self.rect[1] <= hero.rect[1] and not hero.all_right:
                    hero.move(tile_width / hero.v, tile_height / hero.v)
                if self.rect[0] >= hero.rect[0] and self.rect[1] <= hero.rect[1] and not hero.all_right:
                    hero.move(- tile_width / hero.v, tile_height / hero.v)
                if self.rect[0] <= hero.rect[0] and self.rect[1] >= hero.rect[1] and not hero.all_right:
                    hero.move(tile_width / hero.v, - tile_height / hero.v)
                if self.rect[0] >= hero.rect[0] and self.rect[1] >= hero.rect[1] and not hero.all_right:
                    hero.move(- tile_width / hero.v, - tile_height / hero.v)

                hero.count_lifes.count = hero.count_lifes.count - 1
                if hero.count_lifes.count <= 0:
                    died_screen(screen)

    def update(self):  # проверка на попадание выстрела в монстра
        for el in fire_group:
            if self.rect.colliderect(el.rect):
                self.lifes = self.lifes - 1
                el.kill()
        if self.lifes == 0 and not self.is_died:  # если монстр убит
            self.die()

    def die(self):  # монстр убит, становится чб, выбрасывает около себя монетки
        need = self.tile_type + '_bw'
        self.image = tile_images[need]
        self.is_died = 1
        hero.count_killed = hero.count_killed + 1

        Coin(self.rect[0], self.rect[1])
        Coin(self.rect[0], self.rect[1])
        Coin(self.rect[0], self.rect[1])


class Coin(pygame.sprite.Sprite):  # монетки, которые получает игрок после смерти врага
    def __init__(self, x, y):
        super().__init__(level_sprites, coin_group)
        self.x = x
        self.y = y
        self.image = tile_images['moneta']
        self.rect = self.image.get_rect().move(randint(x, x + 3 * tile_width), randint(y, y + 3 * tile_height))

    def update(self):
        # проверка на то, что монеты на таком участке уровня, откуда пользователь их может забрать
        if (pygame.sprite.spritecollideany(self, wall_group) or pygame.sprite.spritecollideany(self, box_group)
                or pygame.sprite.spritecollideany(self, portal_group)
                or pygame.sprite.spritecollideany(self, empty_level_group)):
            self.rect = self.image.get_rect().move(randint(self.x, self.x + 3 * tile_width),
                                                   randint(self.y, self.y + 3 * tile_height))
        if pygame.sprite.spritecollideany(self, hero_group):  # звук сбора героем монет
            if music.play:
                pygame.mixer.Channel(2).play(pygame.mixer.Sound('data/coin.mp3'))
            self.kill()
            hero.count_money = hero.count_money + 1
            cur.execute("""DELETE from constants""")
            cur.execute("""INSERT INTO constants (coins) VALUES(?)""", (hero.count_money,))
            db.commit()
            hero.count_money_from_level = hero.count_money_from_level + 1


class UI_counter(pygame.sprite.Sprite):  # картинки подсчёта энергии и жизней во время игры
    def __init__(self, tile_type, count, x, y):
        self.tile_type = tile_type
        if tile_type == 'lifes':
            super().__init__(ui_group)
            self.count = count
            self.maxi = count
            self.name = tile_type + str(self.count)
            self.image = tile_images[self.name]
            self.rect = self.image.get_rect().move(x, y)
        elif tile_type == 'energy':
            super().__init__(ui_group)
            self.count = count
            self.maxi = count
            self.name = tile_type + str((self.count - 1) // 20 + 1)
            self.image = tile_images[self.name]
            self.rect = self.image.get_rect().move(x, y)
        elif tile_type == 'ui_fon':
            super().__init__(ui_group)
            self.count = count
            self.name = tile_type
            self.image = tile_images[self.name]
            self.rect = self.image.get_rect().move(x, y)

    def update(self):  # изменение количества энергии или жизней игрока
        if self.tile_type == 'lifes':
            super().__init__(ui_group)
            self.name = self.tile_type + str(self.count)
            self.image = tile_images[self.name]
        elif self.tile_type == 'energy':
            super().__init__(ui_group)
            self.name = self.tile_type + str((self.count - 1) // 20 + 1)
            self.image = tile_images[self.name]


class Hero(pygame.sprite.Sprite):  # главный герой
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(hero_group)
        self.start_game = 1
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.rotation = 'right'
        self.v = 4
        UI_counter('ui_fon', 5, tile_width - 5, tile_height - 5)
        self.count_lifes = UI_counter('lifes', 5, tile_width, tile_height)
        self.count_energy = UI_counter('energy', 100, tile_width, tile_height * 2)
        self.has_gun = 0
        self.level = 'level1.txt'
        self.all_right = 1
        self.count_killed = 0
        self.count_money = cur.execute("""SELECT coins FROM constants""").fetchall()[0][0]
        self.cur_scene = 'home'
        self.count_money_from_level = 0
        self.tile_type = tile_type

    def got_gun(self, type_gun):  # hero получил пистолет - у него меняется image
        hero.count_energy.count = hero.count_energy.maxi
        pict = self.tile_type + '_' + type_gun + '.png'
        hero.image = pygame.transform.scale(load_image(pict), (tile_width, tile_height))
        if hero.rotation == 'left':
            hero.image = pygame.transform.flip(self.image, True, False)
        self.has_gun = 1

    def action(self):  # если hero что-то забрал из ящика
        for el in box_group:
            if (abs(hero.rect[0] - el.rect[0]) <= tile_width) and (
                    abs(hero.rect[1] - el.rect[1]) <= tile_height) and not el.opened:
                el.need_to_open = 1
            elif (abs(hero.rect[0] - el.rect[0]) <= tile_width) and (
                    abs(hero.rect[1] - el.rect[1]) <= tile_height) and el.opened and el.inside == 'weapon':
                el.is_taken = 1
                el.weapon.image = pygame.transform.scale(load_image('None.png'), (tile_width, tile_height))
                hero.got_gun(el.weapon.type_gun)
            elif (abs(hero.rect[0] - el.rect[0]) <= tile_width) and (
                    abs(hero.rect[1] - el.rect[
                        1]) <= tile_height) and el.opened and not el.is_taken and el.inside == 'potion_lifes':
                el.is_taken = 1
                el.potion_lifes.image = pygame.transform.scale(load_image('None.png'), (tile_width, tile_height))
                hero.count_lifes.count = hero.count_lifes.maxi
            elif (abs(hero.rect[0] - el.rect[0]) <= tile_width) and (
                    abs(hero.rect[1] - el.rect[
                        1]) <= tile_height) and el.opened and not el.is_taken and el.inside == 'potion_energy':
                el.is_taken = 1
                el.potion_energy.image = pygame.transform.scale(load_image('None.png'), (tile_width, tile_height))
                hero.count_energy.count = hero.count_energy.maxi

    def move(self, dx, dy):  # перемещение hero
        global cat_loading_group, level_changed
        if self.cur_scene == 'home':
            self.all_right = 1
            for el in home_sprites:
                el.rect = pygame.rect.Rect(el.rect[0] - dx * self.v, el.rect[1] - dy * self.v,
                                           el.rect[2],
                                           el.rect[3])
            if pygame.sprite.spritecollideany(self, exit_group):
                self.cur_scene = 'level'
                level_changed = 1
            if (pygame.sprite.spritecollideany(self, empty_home_group)
                    or pygame.sprite.spritecollideany(self, wall_home_group)
                    or pygame.sprite.spritecollideany(self, guitar_group)):
                self.all_right = 0
                for el in home_sprites:
                    el.rect = pygame.rect.Rect(el.rect[0] + dx * self.v, el.rect[1] + dy * self.v,
                                               el.rect[2],
                                               el.rect[3])
            if dx == -1 and self.rotation == 'right' and self.all_right:
                self.image = pygame.transform.flip(self.image, True, False)
                self.rotation = 'left'
            elif dx == 1 and self.rotation == 'left' and self.all_right:
                self.image = pygame.transform.flip(self.image, True, False)
                self.rotation = 'right'
        if self.cur_scene == 'level':
            self.all_right = 1
            for el in level_sprites:
                el.rect = pygame.rect.Rect(el.rect[0] - dx * self.v, el.rect[1] - dy * self.v,
                                           el.rect[2],
                                           el.rect[3])
            if (pygame.sprite.spritecollideany(
                    self, box_group) or pygame.sprite.spritecollideany(self, empty_level_group)
                    or pygame.sprite.spritecollideany(self, wall_group)):
                self.all_right = 0
                for el in level_sprites:
                    el.rect = pygame.rect.Rect(el.rect[0] + dx * self.v, el.rect[1] + dy * self.v,
                                               el.rect[2],
                                               el.rect[3])
            if dx == -1 and self.rotation == 'right' and self.all_right:
                self.image = pygame.transform.flip(self.image, True, False)
                self.rotation = 'left'
            elif dx == 1 and self.rotation == 'left' and self.all_right:
                self.image = pygame.transform.flip(self.image, True, False)
                self.rotation = 'right'
            if pygame.sprite.spritecollideany(self, portal_group):
                cat_loading_group = pygame.sprite.Group()
                loading()

    def shoot(self):  # выстрел из оружия героя
        if hero.count_energy.count > 0:
            if music.play:
                pygame.mixer.Channel(1).play(pygame.mixer.Sound('data/shoot.mp3'))
            Fire(self.rect[0], self.rect[1])
            hero.count_energy.count = hero.count_energy.count - 1


class Fire(pygame.sprite.Sprite):  # пули персонажа
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
        self.v_fire = 3

        self.to_where = [0, 0]
        for el in monsters_group:  # пули летят к монстру в зоне доступности
            if (abs(el.rect[0] - self.rect[0]) <= (tile_width * 5)) and (
                    abs(el.rect[1] - self.rect[1]) <= (tile_width * 5)) and (not el.is_died):
                delta_x = (self.rect[0] + self.rect[2] // 2) - (el.rect[0] + el.rect[2])
                delta_y = (self.rect[1] + self.rect[3] // 2) - (el.rect[1] + el.rect[3])
                self.to_where = [- delta_x / (abs(delta_x) + abs(delta_y)), - delta_y / (abs(delta_x) + abs(delta_y))]
        while self.to_where == [0, 0]:
            self.to_where = [randint(-1, 1), randint(-1, 1)]

    def update(self):  # удаление пуль, когда они отдалены от hero
        self.rect = pygame.rect.Rect(self.rect[0] + self.v_fire * self.to_where[0],
                                     self.rect[1] + self.v_fire * self.to_where[1],
                                     self.rect[2],
                                     self.rect[3])
        if (abs(self.rect[0] - hero.rect[0]) > (tile_width * 5)) or (
                abs(self.rect[1] - hero.rect[1]) > (tile_height * 5)):
            self.kill()


def loading():  # картинка ожидания следующего уровня
    global level_changed

    for el in coin_group:
        el.kill()

    start_ticks = pygame.time.get_ticks()

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

        seconds = (pygame.time.get_ticks() - start_ticks) / 1000

        pygame.display.flip()
        if seconds > 5:
            level_changed = 1
            return


class UI(pygame.sprite.Sprite):  # интерфейс
    def __init__(self, group, tile_type, x, y):
        self.tile_type = tile_type
        super().__init__(group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(x, y)
        if self.tile_type == 'is_sound':
            if music:
                self.play = music.play
                if not self.play:
                    self.image = tile_images['isnt_sound']
            else:
                self.play = 1


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
            elif level[y][x] == 'bw':
                Tile('floor_fon', x + dx, y + dy)
                Box('weapon', x + dx, y + dy)
            elif level[y][x] == 'bl':
                Tile('floor_fon', x + dx, y + dy)
                Box('potion_lifes', x + dx, y + dy)
            elif level[y][x] == 'be':
                Tile('floor_fon', x + dx, y + dy)
                Box('potion_energy', x + dx, y + dy)
            elif level[y][x] == 'or':
                Tile('floor', x + dx, y + dy)
                Monster('orc', x + dx, y + dy)
            elif level[y][x] == 'i':
                Tile('floor', x + dx, y + dy)
                Monster('imp', x + dx, y + dy)


def generate_home(level, hero_type):
    e, h, n, d, k = None, None, None, None, None  # персонажи домашнего экрана и герой
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
                h = Hero(hero_type, x + dx, y + dy)
            elif level[y][x] == 'N':
                Tile('floor_home_fon', x + dx, y + dy)
                n = Necromancer(x + dx, y + dy)
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
            elif level[y][x] == 'D':
                Tile('floor_home_fon', x + dx, y + dy)
                d = Dino(x + dx, y + dy)
            elif level[y][x] == 'E':
                Tile('floor_home_fon', x + dx, y + dy)
                e = Elf(x + dx, y + dy)
            elif level[y][x] == 'K':
                Tile('floor_home_fon', x + dx, y + dy)
                k = Knight(x + dx, y + dy)
    return h, n, d, e, k


if __name__ in '__main__':
    with sqlite3.connect('data/database.db') as db:
        cur = db.cursor()

        pygame.init()
        my_font = pygame.font.Font('data/Undertale-Battle-Font.ttf', 50)

        pygame.mixer.Channel(0).play(pygame.mixer.Sound('data/fon_music.mp3'), -1)

        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        size = screen.get_size()
        width, height = size

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

            'is_sound': pygame.transform.scale(load_image('is_sound.png'), (tile_width, tile_height)),
            'isnt_sound': pygame.transform.scale(load_image('isnt_sound.png'), (tile_width, tile_height)),

            'elf': pygame.transform.scale(load_image('elf_square.png'),
                                          (tile_width, tile_height)),
            'knight': pygame.transform.scale(load_image('knight_m_idle_anim_f0.png'),
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
            'necromancer': pygame.transform.scale(load_image('necromancer_idle_anim_f1.png'),
                                                  (tile_width, tile_height)),
            'okult1': pygame.transform.scale(load_image('okult1.png'), (tile_width, tile_height)),
            'okult2': pygame.transform.scale(load_image('okult2.png'), (tile_width, tile_height)),
            'okult3': pygame.transform.scale(load_image('okult3.png'), (tile_width, tile_height)),
            'okult4': pygame.transform.scale(load_image('okult4.png'), (tile_width, tile_height)),
            'box': pygame.transform.scale(load_image('chest_empty_open_anim_f0.png'), (tile_width, tile_height)),
            '3black': pygame.transform.scale(load_image('3black.png'), (tile_width, tile_height)),
            '7black': pygame.transform.scale(load_image('7black.png'), (tile_width, tile_height)),
            '3gold': pygame.transform.scale(load_image('3gold.png'), (tile_width, tile_height)),
            '7gold': pygame.transform.scale(load_image('7gold.png'), (tile_width, tile_height)),
            '3blue': pygame.transform.scale(load_image('3blue.png'), (tile_width, tile_height)),
            '7blue': pygame.transform.scale(load_image('7blue.png'), (tile_width, tile_height)),
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
            'imp': pygame.transform.scale(load_image('imp_idle_anim_f0.png'), (tile_width, tile_height)),
            'imp_bw': pygame.transform.scale(load_image('imp_idle_anim_f0_bw.png'), (tile_width, tile_height)),
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
            'potion_lifes': pygame.transform.scale(load_image('flask_big_red.png'), (tile_width, tile_height)),
            'potion_energy': pygame.transform.scale(load_image('flask_big_blue.png'), (tile_width, tile_height)),
            'for_text': pygame.transform.scale(load_image('for_text.png'), (212, 64)),
            'clock': pygame.transform.scale(load_image('clock.png'), (tile_width, tile_height)),
            'moneta': pygame.transform.scale(load_image('moneta.png'), (tile_width // 2, tile_height // 2)),
            'moneta_screen': pygame.transform.scale(load_image('moneta.png'), (tile_width, tile_height)),
            'percent': pygame.transform.scale(load_image('percent.png'), (width // 3 * 2, height // 12)),
            'count_dead': pygame.transform.scale(load_image('count_dead.png'), (tile_width, tile_height)),
            'skip': pygame.transform.scale(load_image('skip.png'), (252, 80)),

            '1orange': pygame.transform.scale(load_image('1orange.png'), (200, 200)),
            '2orange': pygame.transform.scale(load_image('2orange.png'), (200, 200)),
            '3orange': pygame.transform.scale(load_image('3orange.png'), (200, 200)),
            '4orange': pygame.transform.scale(load_image('4orange.png'), (200, 200)),
        }

        ui_start = pygame.sprite.Group()
        start_screen(screen)

        home_sprites = pygame.sprite.Group()
        skins_group = pygame.sprite.Group()
        wall_home_group = pygame.sprite.Group()
        floor_home_group = pygame.sprite.Group()
        exit_group = pygame.sprite.Group()
        necromancer_group = pygame.sprite.Group()
        dino_group = pygame.sprite.Group()
        elf_group = pygame.sprite.Group()
        knight_group = pygame.sprite.Group()
        guitar_group = pygame.sprite.Group()
        empty_home_group = pygame.sprite.Group()
        ui_home_group = pygame.sprite.Group()

        ui_died_group = pygame.sprite.Group()
        ui_died_to_home = pygame.sprite.Group()

        level_sprites = pygame.sprite.Group()
        hero_group = pygame.sprite.Group()
        floor_group = pygame.sprite.Group()
        coin_group = pygame.sprite.Group()
        wall_group = pygame.sprite.Group()
        ui_group = pygame.sprite.Group()
        portal_group = pygame.sprite.Group()
        box_group = pygame.sprite.Group()
        weapon_group = pygame.sprite.Group()
        monsters_group = pygame.sprite.Group()
        fire_group = pygame.sprite.Group()
        empty_level_group = pygame.sprite.Group()

        cat_loading_group = pygame.sprite.Group()

        cat_died_group = pygame.sprite.Group()

        weapon = ['3gold', '3blue', '3black', '7gold', '7blue', '7black']

        filename = 'home.txt'

        home_map = load_level(filename)
        home_map = [el.split() for el in home_map]

        if 'E' in ' '.join([' '.join(el) for el in home_map]) and 'N' in ' '.join(
                [' '.join(el) for el in home_map]) and 'K' in ' '.join([' '.join(el) for el in home_map]):
            hero_type = 'dino'
        elif 'D' in ' '.join([' '.join(el) for el in home_map]) and 'N' in ' '.join(
                [' '.join(el) for el in home_map]) and 'K' in ' '.join([' '.join(el) for el in home_map]):
            hero_type = 'elf'
        elif 'E' in ' '.join([' '.join(el) for el in home_map]) and 'D' in ' '.join(
                [' '.join(el) for el in home_map]) and 'K' in ' '.join([' '.join(el) for el in home_map]):
            hero_type = 'necromancer'
        elif 'E' in ' '.join([' '.join(el) for el in home_map]) and 'D' in ' '.join(
                [' '.join(el) for el in home_map]) and 'N' in ' '.join([' '.join(el) for el in home_map]):
            hero_type = 'knight'

        home = 1
        hero, necromancer, dino, elf, knight = generate_home(home_map, hero_type)
        hero.cur_scene = 'home'
        close_home = UI(ui_home_group, 'close_home', width - tile_width - 50, 50)
        money = UI(ui_home_group, 'coin_fon', tile_width, tile_height)
        button_pkm = UI(ui_home_group, 'pkm', tile_width, height - tile_height * 2)
        button_p = UI(ui_home_group, 'p', 2 * tile_width + 10, height - tile_height * 2)

        music = None
        music = UI(ui_home_group, 'is_sound', 3 * tile_width + 20, height - tile_height * 2)
        home_screen(screen)

        running = True
        fps = 60
        clock = pygame.time.Clock()
        level_changed = 1

        while running:
            if home:  # сцена дома
                hero = None
                elf = None
                dino = None
                necromancer = None
                home_sprites = pygame.sprite.Group()
                skins_group = pygame.sprite.Group()
                wall_home_group = pygame.sprite.Group()
                floor_home_group = pygame.sprite.Group()
                exit_group = pygame.sprite.Group()
                necromancer_group = pygame.sprite.Group()
                dino_group = pygame.sprite.Group()
                elf_group = pygame.sprite.Group()
                knight_group = pygame.sprite.Group()
                guitar_group = pygame.sprite.Group()
                empty_home_group = pygame.sprite.Group()
                ui_home_group = pygame.sprite.Group()
                ui_home_group = pygame.sprite.Group()

                hero_group = pygame.sprite.Group()

                filename = 'home.txt'
                home_map = load_level(filename)
                home_map = [el.split() for el in home_map]
                hero, necromancer, dino, elf, knight = generate_home(home_map, hero_type)
                hero.cur_scene = 'home'
                close_home = UI(ui_home_group, 'close_home', width - tile_width - 50, 50)
                money = UI(ui_home_group, 'coin_fon', tile_width, tile_height)
                button_pkm = UI(ui_home_group, 'pkm', tile_width, height - tile_height * 2)
                button_p = UI(ui_home_group, 'p', 2 * tile_width + 10, height - tile_height * 2)
                music = UI(ui_home_group, 'is_sound', 3 * tile_width + 20, height - tile_height * 2)
                home_screen(screen)

            else:  # сцена уровня
                if level_changed:
                    if hero.start_game:
                        hero.count_money_from_level = 0
                        hero.count_killed = 0
                        time_start = pygame.time.get_ticks() // 1000
                    hero.start_game = 0
                    level_sprites = pygame.sprite.Group()
                    floor_group = pygame.sprite.Group()
                    wall_group = pygame.sprite.Group()
                    ui_group = pygame.sprite.Group()
                    portal_group = pygame.sprite.Group()
                    box_group = pygame.sprite.Group()
                    weapon_group = pygame.sprite.Group()
                    monsters_group = pygame.sprite.Group()
                    fire_group = pygame.sprite.Group()
                    empty_level_group = pygame.sprite.Group()

                    filenames = ['level1.txt', 'level2.txt', 'level3.txt', 'level4.txt', 'level5.txt']
                    filename = hero.level
                    save = hero.level
                    while save == hero.level:
                        hero.level = choice(filenames)
                    level_map = load_level(filename)
                    level_map = [el.split() for el in level_map]
                    hero.cur_scene = 'level'
                    generate_level(level_map)

                    button_pkm = UI(ui_group, 'pkm', tile_width, height - tile_height * 2)
                    button_p = UI(ui_group, 'p', 2 * tile_width + 10, height - tile_height * 2)
                    close = UI(ui_group, 'close', width - tile_width - 50, 50)
                    music = UI(ui_group, 'is_sound', 3 * tile_width + 20, height - tile_height * 2)

                    level_changed = 0
                clock.tick(fps)
                screen.fill(pygame.Color('black'))

                for el in monsters_group:  # перемещение монстров, если рядом игрок
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
                            if el.tile_type == 'is_sound':
                                el.play = (el.play + 1) % 2
                                if el.play:
                                    el.image = tile_images['is_sound']
                                    pygame.mixer.Channel(0).unpause()
                                else:
                                    el.image = tile_images['isnt_sound']
                                    pygame.mixer.Channel(0).pause()
                        if hero.has_gun and event.button == 3:  # выстрел игрока из оружия
                            hero.shoot()
                    if event.type == pygame.KEYDOWN:  # взять предмет из ящика
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
                coin_group.update()
                coin_group.draw(screen)
                hero_group.draw(screen)
                ui_group.draw(screen)

                hero.count_lifes.update()
                hero.count_energy.update()

                fire_group.update()

            pygame.display.flip()
        db.commit()
        terminate()
