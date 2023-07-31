from settings import *
from random import choice
from gametimer import Timer


class Game:
    def __init__(self):
        self.surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        self.display_surface = pygame.display.get_surface()
        self.rect = self.surface.get_rect(topleft=(PADDING, PADDING))
        self.sprites = pygame.sprite.Group()

        # lines
        self.lines_surface = self.surface.copy()
        self.lines_surface.fill((0, 255, 0))
        self.lines_surface.set_colorkey((0, 255, 0))
        self.lines_surface.set_alpha(120)

        # tetronimo
        self.tetronimo = Tetromino(
            choice(list(TETROMINOS.keys())), self.sprites)

        # timer
        # self.timer = Timer()
        self.down_speed = UPDATE_START_SPEED
        self.down_speed_faster = self.down_speed * 0.3
        self.down_pressed = False
        self.timers = {
			'vertical move': Timer(self.down_speed, True, self.move_down),
			'horizontal move': Timer(MOVE_WAIT_TIME),
			'rotate': Timer(ROTATE_WAIT_TIME)
		}
        self.timers['vertical move'].activate()

    def timer_update(self):
        for t in self.timers.values():
            t.update()
    
    def move_down(self):
        self.tetronimo.move_down()

    def draw_grid(self):
        for col in range(1, COLUMNS):
            x = col * CELL_SIZE
            pygame.draw.line(self.lines_surface, LINE_COLOR,
                             (x, 0), (x, self.surface.get_height()), 1)

        for row in range(1, ROWS):
            y = row * CELL_SIZE
            pygame.draw.line(self.lines_surface, LINE_COLOR,
                             (0, y), (self.surface.get_width(), y))

        self.surface.blit(self.lines_surface, (0, 0))

    def input(self):
        keys= pygame.key.get_pressed()

        if not self.timers['horizontal move'].active:
            if keys[pygame.K_LEFT]:
                self.tetronimo.move_orizontal(-1)
                self.timers['horizontal move'].activate()
            if keys[pygame.K_RIGHT]:
                self.tetronimo.move_orizontal(+1)
                self.timers['horizontal move'].activate()

    def run(self):

        # update
        self.input()
        self.timer_update()
        self.sprites.update()
        
        # drawing
        self.surface.fill(GRAY)
        self.sprites.draw(self.surface)

        self.draw_grid()
        self.display_surface.blit(self.surface, (PADDING, PADDING))
        pygame.draw.rect(self.display_surface, LINE_COLOR, self.rect, 2, 2)


class Tetromino:
    def __init__(self, shape, group):

        # setup
        self.block_position = TETROMINOS[shape]['shape']
        self.color = TETROMINOS[shape]['color']

        # create block
        self.blocks = [Block(group, pos, self.color)
                       for pos in self.block_position]
        # self.shape = choice([k for k in TETROMINOS ])
    
    # collision

    def next_move_horizontal_collide(self, blocks, amount):
        collision_list = [block.horizontal_collide(int(block.pos.x + amount)) for block in self.blocks]
        return True if any(collision_list) else False
    
    def next_move_vertical_collide(self, blocks, amount):
        collision_list = [block.vertical_collide(int(block.pos.y + amount)) for block in self.blocks]
        return True if any(collision_list) else False

    # movement 
    def move_down(self):
        if not self.next_move_vertical_collide(self.blocks, 1):
            for blocks in self.blocks:
                blocks.pos.y += 1

    def move_orizontal(self, amount):
        if not self.next_move_horizontal_collide(self.blocks, amount):
            for blocks in self.blocks:
                blocks.pos.x += amount


class Block(pygame.sprite.Sprite):

    def __init__(self, group, pos, color):
        super().__init__(group)
        self.image = pygame.Surface((CELL_SIZE, CELL_SIZE))
        self.image.fill(color)

        # position
        self.pos = pygame.Vector2(pos) + BLOCK_OFFSET
        self.rect = self.image.get_rect(topleft=self.pos * CELL_SIZE)

    def horizontal_collide(self, x):
        if not 0 <= x < COLUMNS:
            return True
    
    def vertical_collide(self, y):
        if y >= ROWS:
            return True

    def update(self):
        self.rect.topleft = self.pos * CELL_SIZE