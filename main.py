import os
import sys
import pygame

pygame.init()
pygame.key.set_repeat(200, 70)

FPS = 60
WIDTH = 800
HEIGHT = 600
STEP = 50

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

player = None
enemys = []
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
box_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
enemys_group = pygame.sprite.Group()
cursor_group = pygame.sprite.Group()
btn1_group = pygame.sprite.Group()
btn2_group = pygame.sprite.Group()


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


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    repeat_map = [line.replace('.', '*') for line in level_map]
    level_map += repeat_map
    # и подсчитываем максимальную длину
    max_width = WIDTH // tile_width + 1
    # print(list(map(lambda x: x.ljust(max_width, '.'), level_map)))
    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '*'), level_map))


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

def count_hp(hp):
    text = 'Здоровья осталось:'
    font = pygame.font.Font(None, 30)
    string_rendered = font.render(text, 1, pygame.Color('white'))
    intro_rect = string_rendered.get_rect()
    text_coord = 480
    intro_rect.top = text_coord
    intro_rect.x = 10
    screen.blit(string_rendered, intro_rect)
    text = str(hp)
    string_rendered = font.render(text, 1, pygame.Color('white'))
    intro_rect = string_rendered.get_rect()
    #text_coord = 630
    intro_rect.top = text_coord
    intro_rect.x = 220
    screen.blit(string_rendered, intro_rect)


def generate_level(level, t):
    new_player, x, y = None, None, None
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
    return new_player, x, y


def terminate():
    pygame.quit()
    sys.exit()


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

    lev1_image = load_image('уровень 1.png', (228, 60))
    lev1 = pygame.sprite.Sprite()
    lev1.image = lev1_image
    lev1.rect = lev1.image.get_rect()
    lev1.rect.x, lev1.rect.y = 50, 100
    btn1_group.add(lev1)

    lev2_image = load_image('уровень 2.png', (228, 60))
    lev2 = pygame.sprite.Sprite()
    lev2.image = lev2_image
    lev2.rect = lev2.image.get_rect()
    lev2.rect.x, lev2.rect.y = 50, 300
    btn2_group.add(lev2)

    btn1_group.draw(screen)
    btn2_group.draw(screen)
    cursor = Cursor()

    while True:
        cursor.rect.x, cursor.rect.y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.sprite.spritecollideany(cursor, btn1_group):
                cursor.kill()
                return 'levelex.txt'
            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.sprite.spritecollideany(cursor, btn2_group):
                cursor.kill()
                return 'levelex1.txt'
        screen.blit(fon, (0, 0))
        btn1_group.draw(screen)
        btn2_group.draw(screen)
        cursor_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


p_images = ['player\\Wraith_01_Moving Forward_001', 'player\\Wraith_01_Moving Forward_002',
            'player\\Wraith_01_Moving Forward_003', 'player\\Wraith_01_Moving Forward_004',
            'player\\Wraith_01_Moving Forward_005', 'player\\Wraith_01_Moving Forward_006',
            'player\\Wraith_01_Moving Forward_007', 'player\\Wraith_01_Moving Forward_008',
            'player\\Wraith_01_Moving Forward_009', 'player\\Wraith_01_Moving Forward_010',
            'player\\Wraith_01_Moving Forward_011']

p_attack = ['Wraith_01_Casting Spells_000', 'Wraith_01_Casting Spells_003', 'Wraith_01_Casting Spells_006',
            'Wraith_01_Casting Spells_009', 'Wraith_01_Casting Spells_012', 'Wraith_01_Casting Spells_015',
            'Wraith_01_Casting Spells_017']

tile_images = {'wall': load_image('box.png', (80, 80)), 'empty': load_image('grass.png', (80, 80))}
player_images_r = [load_image(i + '.png', (97, 139)) for i in p_images]
player_images_l = [load_image(i + '(1).png', (97, 139)) for i in p_images]
p_attack_images = [load_image('attack\\' + i + '.png', (97, 139)) for i in p_attack]
monster_image = load_image('monster.png', (50, 70))

tile_width = tile_height = 80


class Cursor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(cursor_group, all_sprites)
        self.image = load_image("cursor.png")
        rect = self.image.get_rect()
        self.rect = pygame.Rect(rect.x, rect.y, 50, 50)
        self.rect.x, self.rect.y = pygame.mouse.get_pos()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        self.health = 100
        super().__init__(enemys_group, all_sprites)
        self.image = monster_image
        self.step = 1
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)

    def hit(self, x, y):
        if x - 100 <= self.rect.x <= x + 200 and y - 100 <= self.rect.y <= y + 200:
            print('aaaaaaaaaaaaaaaaaa')
            self.health -= 10

    def go(self):
        x_step = self.rect.x - player.rect.x
        y_step = self.rect.y - player.rect.y
        x_step = x_step if x_step <= self.step else self.step
        y_step = y_step if y_step <= self.step else self.step
        self.rect.x -= x_step
        self.rect.y -= y_step

    def die(self):
        self.kill()


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        print(11111111)
        super().__init__(player_group, all_sprites)
        self.directions = player_images_r
        self.attacking = p_attack_images
        self.cadr = 0
        self.hp = 200
        self.is_attack = False
        self.attack_cadr = 0
        self.image = self.directions[self.cadr]
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)

    def animate(self):
        if self.is_attack and self.attack_cadr < 7:
            self.image = self.attacking[self.attack_cadr]

        else:
            self.cadr = (self.cadr + 1) % 11
            self.image = self.directions[self.cadr]
        if self.attack_cadr == 7:
            self.is_attack = False
            self.attack_cadr = 0

    def go(self):
        self.is_attack = False

    def change_direction_on_r(self):
        self.directions = player_images_r

    def change_direction_on_l(self):
        self.directions = player_images_l

    def attack(self):
        self.is_attack = True
        self.attack_cadr += 1


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


level_name = start_screen()

T = 0
player, level_x, level_y = generate_level(load_level(level_name), T)
camera = Camera((level_x, level_y))
cursor = Cursor()
pygame.mouse.set_visible(False)
enemy_die = 0
count_dies(enemy_die)

running = True

while running:
    cursor.rect.x, cursor.rect.y = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            player.go()
            p_x = player.rect.x
            p_y = player.rect.y
            player.animate()
            if event.key == pygame.K_LEFT:
                player.change_direction_on_l()
                player.animate()
                player.rect.x -= STEP
                cursor.rect.x -= STEP
            if event.key == pygame.K_RIGHT:
                player.change_direction_on_r()
                player.animate()
                player.rect.x += STEP
                cursor.rect.x += STEP
            if event.key == pygame.K_UP:
                player.rect.y -= STEP
                cursor.rect.y -= STEP
            if event.key == pygame.K_DOWN:
                player.rect.y += STEP
                cursor.rect.y += STEP
            if pygame.sprite.spritecollideany(player, box_group) or pygame.sprite.spritecollideany(player, enemys_group):
                player.rect.x = p_x
                player.rect.y = p_y
        elif event.type == pygame.MOUSEBUTTONDOWN and pygame.sprite.spritecollideany(cursor, enemys_group):
            for i in enemys:
                i.hit(player.rect.x, player.rect.y)
                player.attack()
                player.animate()
                if i.health <= 0:
                    i.die()
                    enemy_die += 1
                    enemys.remove(i)
                    count_dies(enemy_die)
                    print('умерло противников:', enemy_die)

    camera.update(player)

    for sprite in all_sprites:
        camera.apply(sprite)

    # for enemy in enemys_group:
    #     enemy.go()

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
