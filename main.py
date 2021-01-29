# импортирование нужных библиотек
import os
import sys
import pygame

pygame.init()
pygame.key.set_repeat(200, 70)

# инициализация параметров экрана
FPS = 60
WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

player = None
enemys = []

# инициализация групп
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
box_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
enemys_group = pygame.sprite.Group()
cursor_group = pygame.sprite.Group()
btn1_group = pygame.sprite.Group()
btn2_group = pygame.sprite.Group()

levels_name = ['levelex.txt', 'levelex1.txt']


# функция для удаление всех спрайтов
def kill_all():
    for sprite0 in all_sprites:
        sprite0.kill()

    for sprite0 in tiles_group:
        sprite0.kill()

    for sprite0 in box_group:
        sprite0.kill()

    for sprite0 in player_group:
        sprite0.kill()

    for sprite0 in enemys_group:
        sprite0.kill()

    for sprite0 in cursor_group:
        sprite0.kill()

    for sprite0 in btn1_group:
        sprite0.kill()

    for sprite0 in btn2_group:
        sprite0.kill()


# функция для загрузки изображений
def load_image(name, size=None, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    if size is not None:
        image = pygame.transform.scale(image, size)
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
        image = image.convert()
    else:
        image = image.convert_alpha()
    return image


# функция для загрузки уровня
def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    repeat_map = [line.replace('.', '*') for line in level_map]
    level_map += repeat_map
    # и подсчитываем максимальную длину
    max_width = WIDTH // tile_width + 1
    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '*'), level_map))


# функция для расчета кол-во убитых врагов
def count_dies(num):
    text = 'Врагов убито:'
    font = pygame.font.Font(None, 30)
    string_rendered = font.render(text, 1, pygame.Color('white'))
    intro_rect = string_rendered.get_rect()
    text_coord = 530
    intro_rect.top = text_coord
    intro_rect.x = 10
    screen.blit(string_rendered, intro_rect)
    text = str(num)
    string_rendered = font.render(text, 1, pygame.Color('white'))
    intro_rect = string_rendered.get_rect()
    text_coord = 530
    intro_rect.top = text_coord
    intro_rect.x = 160
    screen.blit(string_rendered, intro_rect)


# функция для расчета кол-во здоровья игрока
def count_hp(hp):
    text = 'Здоровья осталось:'
    font = pygame.font.Font(None, 30)
    string_rendered = font.render(text, 1, pygame.Color('white'))
    intro_rect = string_rendered.get_rect()
    text_coord = 480
    intro_rect.top = text_coord
    intro_rect.x = 10
    screen.blit(string_rendered, intro_rect)
    text = str(int(hp))
    string_rendered = font.render(text, 1, pygame.Color('white'))
    intro_rect = string_rendered.get_rect()
    # text_coord = 630
    intro_rect.top = text_coord
    intro_rect.x = 220
    screen.blit(string_rendered, intro_rect)


# функция для генерации уровня
def generate_level(level, t, level_name):
    new_player, x, y = None, None, None
    with open('data\\enemys.txt') as f:
        f = list(f)
        print(level)
        count = int(f[levels_name.index(level_name)].strip())

    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '*':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y).add(box_group)
            elif level[y][x] == '.' and t == 0:
                Tile('empty', x, y).add(tiles_group)
                new_player = Player(x, y)
                t = 1
            elif level[y][x] == '^':
                Tile('empty', x, y).add(tiles_group)
                enemys.append(Enemy(x, y))
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y, count


def terminate():
    pygame.quit()
    sys.exit()


# функция, отвечающая за открытия экрана победы
def win_screen():
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 300)
    text_coord = 100
    string_rendered = font.render("win", 1, pygame.Color('white'))
    intro_rect = string_rendered.get_rect()
    text_coord += 100
    intro_rect.top = text_coord
    intro_rect.x = 200
    text_coord += intro_rect.height
    global W
    while True and not W:
        cursor.rect.x, cursor.rect.y = pygame.mouse.get_pos()
        for event0 in pygame.event.get():
            if event0.type == pygame.QUIT:
                terminate()
            elif event0.type == pygame.KEYDOWN and event0.key == pygame.K_RETURN:
                cursor.kill()
                W = 1
        screen.blit(fon, (0, 0))
        cursor_group.draw(screen)
        screen.blit(string_rendered, intro_rect)
        pygame.display.flip()
        clock.tick(FPS)


# функция, отвечающая за открытия экрана проигрыша
def death_screen():
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 300)
    text_coord = 100
    string_rendered = font.render("death", 1, pygame.Color('white'))
    intro_rect = string_rendered.get_rect()
    text_coord += 100
    intro_rect.top = text_coord
    intro_rect.x = 100
    text_coord += intro_rect.height
    global W
    while True and not W:
        cursor.rect.x, cursor.rect.y = pygame.mouse.get_pos()
        for event0 in pygame.event.get():
            if event0.type == pygame.QUIT:
                terminate()
            elif event0.type == pygame.KEYDOWN and event0.key == pygame.K_RETURN:
                cursor.kill()
                W = 1
        screen.blit(fon, (0, 0))
        cursor_group.draw(screen)
        screen.blit(string_rendered, intro_rect)
        pygame.display.flip()
        clock.tick(FPS)


# функция, отвечающая за открытия главного экрана
def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    # уровень 1
    lev1_image = load_image('уровень 1.png', (228, 60))
    lev1 = pygame.sprite.Sprite()
    lev1.image = lev1_image
    lev1.rect = lev1.image.get_rect()
    lev1.rect.x, lev1.rect.y = 50, 50
    btn1_group.add(lev1)

    # уровень 2
    lev2_image = load_image('уровень 2.png', (228, 60))
    lev2 = pygame.sprite.Sprite()
    lev2.image = lev2_image
    lev2.rect = lev2.image.get_rect()
    lev2.rect.x, lev2.rect.y = 50, 150
    btn2_group.add(lev2)

    btn1_group.draw(screen)
    btn2_group.draw(screen)

    cursor1 = Cursor()

    while True:
        cursor1.rect.x, cursor1.rect.y = pygame.mouse.get_pos()

        for event0 in pygame.event.get():
            if event0.type == pygame.QUIT:
                terminate()
            elif event0.type == pygame.MOUSEBUTTONDOWN and pygame.sprite.spritecollideany(cursor1, btn1_group):
                cursor1.kill()
                return 'levelex.txt'
            elif event0.type == pygame.MOUSEBUTTONDOWN and pygame.sprite.spritecollideany(cursor1, btn2_group):
                cursor1.kill()
                return 'levelex1.txt'

        screen.blit(fon, (0, 0))
        btn1_group.draw(screen)
        btn2_group.draw(screen)
        cursor_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


# анимация движения у врагов
e_images = ['Walking\\Golem_03_Walking_000', 'Walking\\Golem_03_Walking_001', 'Walking\\Golem_03_Walking_002',
            'Walking\\Golem_03_Walking_003', 'Walking\\Golem_03_Walking_004', 'Walking\\Golem_03_Walking_005',
            'Walking\\Golem_03_Walking_006', 'Walking\\Golem_03_Walking_007', 'Walking\\Golem_03_Walking_008']

e_images_l = ['Walking_l\\1w', 'Walking_l\\2w', 'Walking_l\\3w', 'Walking_l\\4w',
              'Walking_l\\5w', 'Walking_l\\6w', 'Walking_l\\7w', 'Walking_l\\8w',
              'Walking_l\\9w']

# анимация атаки у врагов
e_attack = ['Attacking\\Golem_03_Attacking_000', 'Attacking\\Golem_03_Attacking_001',
            'Attacking\\Golem_03_Attacking_002', 'Attacking\\Golem_03_Attacking_003',
            'Attacking\\Golem_03_Attacking_004', 'Attacking\\Golem_03_Attacking_005',
            'Attacking\\Golem_03_Attacking_006', 'Attacking\\Golem_03_Attacking_007',
            'Attacking\\Golem_03_Attacking_008']

e_images_r = [load_image(i + '.png', (62, 92)) for i in e_images]
e_images_l = [load_image(i + '.png', (62, 92)) for i in e_images_l]
e_attack_images = [load_image(i + '.png', (62, 92)) for i in e_attack]

# анимация движения у главного персонажа
p_images = ['player\\Wraith_01_Moving Forward_001', 'player\\Wraith_01_Moving Forward_002',
            'player\\Wraith_01_Moving Forward_003', 'player\\Wraith_01_Moving Forward_004',
            'player\\Wraith_01_Moving Forward_005', 'player\\Wraith_01_Moving Forward_006',
            'player\\Wraith_01_Moving Forward_007', 'player\\Wraith_01_Moving Forward_008',
            'player\\Wraith_01_Moving Forward_009', 'player\\Wraith_01_Moving Forward_010',
            'player\\Wraith_01_Moving Forward_011']

player_images_r = [load_image(i + '.png', (52, 82)) for i in p_images]
player_images_l = [load_image(i + '(1).png', (52, 82)) for i in p_images]

tile_images = {'wall': load_image('box.png', (80, 80)), 'empty': load_image('grass.png', (80, 80))}


tile_width = tile_height = 80


# класс, отвечающий за курсор
class Cursor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(cursor_group, all_sprites)
        self.image = load_image("cursor.png")
        rect = self.image.get_rect()
        self.rect = pygame.Rect(rect.x, rect.y, 50, 50)
        self.rect.x, self.rect.y = pygame.mouse.get_pos()


# класс, отвечающий за врагов
class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        self.health = 100
        super().__init__(enemys_group, all_sprites)
        self.cadr = 0
        self.attack_cadr = 0
        self.directions = e_images_r
        self.attacking = e_attack_images
        self.image = self.directions[self.cadr]
        self.step = 1
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)

    # изменение направления врага на правое
    def change_direction_on_r(self):
        self.directions = e_images_r

    # изменение направлени  я врага на левое
    def change_direction_on_l(self):
        self.directions = e_images_l

    # ближний удар врага
    def hit1(self, x, y):
        if x - 100 <= self.rect.x <= x + 200 and y - 100 <= self.rect.y <= y + 200:
            self.health -= 10

    # дальний удар врага
    def hit2(self, x, y):
        if x - 500 <= self.rect.x <= x + 600 and y - 500 <= self.rect.y <= y + 600:
            self.health -= 5

    # анимация ходьбы у врагов
    def e_animate(self):
        self.cadr = (self.cadr + 1) % 8
        self.image = self.directions[self.cadr]

    # анимация удара у врогов
    def e_animate_h(self):
        self.attack_cadr = (self.attack_cadr + 1) % 8
        self.image = e_attack_images[self.attack_cadr]

    # ходьба врагов
    def go(self):
        speed = 1
        px = player.rect.x
        py = player.rect.y
        # Movement x
        if (((self.rect.x - px) ** 2) + ((self.rect.y - py) ** 2)) ** (1 / 2) < 300:
            if self.rect.x > px:
                self.rect.x -= speed
                enemy.change_direction_on_l()
            elif self.rect.x < px:
                self.rect.x += speed
                enemy.change_direction_on_r()
            # Movement y
            if self.rect.y < py:
                self.rect.y += speed
            elif self.rect.y > py:
                self.rect.y -= speed
            enemy.e_animate()

    # атака врагов
    def e_attack(self):
        if (self.rect.x == player.rect.x) and (self.rect.y == player.rect.y):
            player.hp -= 0.001
            enemy.e_animate_h()

    # смерть врагов
    def die(self):
        self.kill()


# класс, отвечающий за игровое поле
class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


# класс, отвечающий за героя, которым управляет игрок
class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        print(11111111)
        super().__init__(player_group, all_sprites)
        self.directions = player_images_r
        self.cadr = 0
        self.hp = 200
        self.is_attack = False
        self.attack_cadr = 0
        self.image = self.directions[self.cadr]
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)

    # анимация движения игрока
    def animate(self):
        self.cadr = (self.cadr + 1) % 11
        self.image = self.directions[self.cadr]

    # ходьба игрока
    def go(self):
        self.is_attack = False

    # изменение направления игрока на правое
    def change_direction_on_r(self):
        self.directions = player_images_r

    # изменение направления игрока на левое
    def change_direction_on_l(self):
        self.directions = player_images_l

    # атака игрока
    def attack(self):
        self.is_attack = True
        self.attack_cadr += 1


# класс, отвечающий за смещение картинки по движению персонажа
class Camera:
    # зададим начальный сдвиг камеры и размер поля для возможности реализации циклического сдвига
    def __init__(self, field_size):
        self.dx = 0
        self.dy = 0
        self.field_size = field_size

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        # вычислим координату клитки, если она уехала влево за границу экрана
        if obj.rect.x < -obj.rect.width:
            obj.rect.x += (self.field_size[0] + 1) * obj.rect.width
        # вычислим координату клитки, если она уехала вправо за границу экрана
        if obj.rect.x >= (self.field_size[0]) * obj.rect.width:
            obj.rect.x += -obj.rect.width * (1 + self.field_size[0])
        obj.rect.y += self.dy
        # вычислим координату клитки, если она уехала вверх за границу экрана
        if obj.rect.y < -obj.rect.height:
            obj.rect.y += (self.field_size[1] + 1) * obj.rect.height
        # вычислим координату клитки, если она уехала вниз за границу экрана
        if obj.rect.y >= (self.field_size[1]) * obj.rect.height:
            obj.rect.y += -obj.rect.height * (1 + self.field_size[1])

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


# запуск программы
level_name = start_screen()

T = 0
player, level_x, level_y, quan = generate_level(load_level(level_name), T, level_name)
camera = Camera((level_x, level_y))
cursor = Cursor()
pygame.mouse.set_visible(False)
enemy_die = 0
count_dies(enemy_die)
W = 0
STEP = 50
g = 0

running = True

# основной цикл выполнения программы
while running:
    cursor.rect.x, cursor.rect.y = pygame.mouse.get_pos()
    if W:
        kill_all()
        level_name = start_screen()
        T = 0
        player, level_x, level_y, quan = generate_level(load_level(level_name), T, level_name)
        camera = Camera((level_x, level_y))
        cursor = Cursor()
        pygame.mouse.set_visible(False)
        enemy_die = 0
        count_dies(enemy_die)
        W = 0

    for event in pygame.event.get():
        # проверка на выход из программы
        if event.type == pygame.QUIT:
            running = False

        # проверка на нажатие на клавиши
        elif event.type == pygame.KEYDOWN:
            player.go()
            p_x = player.rect.x
            p_y = player.rect.y
            player.animate()

            # проверка на нажатие на клавишу стрелка влево
            if event.key == pygame.K_LEFT:
                player.change_direction_on_l()
                player.animate()
                player.rect.x -= STEP
                cursor.rect.x -= STEP

            # проверка на нажатие на клавишу стрелка вправо
            if event.key == pygame.K_RIGHT:
                player.change_direction_on_r()
                player.animate()
                player.rect.x += STEP
                cursor.rect.x += STEP

            # проверка на нажатие на клавишу стрелка вверх
            if event.key == pygame.K_UP:
                player.rect.y -= STEP
                cursor.rect.y -= STEP

            # проверка на нажатие на клавишу стрелка вниз
            if event.key == pygame.K_DOWN:
                player.rect.y += STEP
                cursor.rect.y += STEP

            # проверка на пересечение игрока и группы Box
            if pygame.sprite.spritecollideany(player, box_group):
                player.rect.x = p_x
                player.rect.y = p_y

            if event.key == pygame.K_RETURN:
                kill_all()

                level_name = start_screen()
                T = 0
                player, level_x, level_y, quan = generate_level(load_level(level_name), T, level_name)
                camera = Camera((level_x, level_y))
                cursor = Cursor()
                pygame.mouse.set_visible(False)
                enemy_die = 0
                count_dies(enemy_die)
            if event.key == pygame.K_e:
                for i in enemys:
                    if pygame.sprite.spritecollideany(player, enemys_group):
                        i.hit1(player.rect.x, player.rect.y)
                    else:
                        i.hit2(player.rect.x, player.rect.y)
                    player.attack()
                    player.animate()
                    if i.health <= 0:
                        i.die()
                        enemy_die += 1
                        enemys.remove(i)
                        count_dies(enemy_die)

    camera.update(player)

    # проверка здоровья игрока
    if player.hp < 0:
        W = 0
        death_screen()

    # проверка на победу в игре
    if enemy_die >= quan:
        W = 0
        win_screen()

    for sprite in all_sprites:
        camera.apply(sprite)

    # включение автоматического движения врагов и автоматическй атаки игрока
    for enemy in enemys_group:
        enemy.go()
        enemy.e_attack()
        count_hp(player.hp)

    print(W)

    if pygame.sprite.spritecollideany(player, enemys_group):
        player.hp -= 0.15

    screen.fill(pygame.Color(0, 0, 0))
    tiles_group.draw(screen)
    player_group.draw(screen)
    enemys_group.draw(screen)
    cursor_group.draw(screen)
    count_dies(enemy_die)
    count_hp(player.hp)

    pygame.display.flip()

    clock.tick(FPS)

terminate()
