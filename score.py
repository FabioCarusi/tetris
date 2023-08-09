from settings import *
from os.path import join

class Score:
    def __init__(self):
        self.surface = pygame.Surface(
            (SIDEBAR_WIDTH, GAME_HEIGHT * SCORE_HEIGHT_FRACTION - PADDING)
        )
        self.rect = self.surface.get_rect(
            bottomright=(WINDOW_WIDTH - PADDING, WINDOW_HEIGHT - PADDING)
        )
        self.display_surface = pygame.display.get_surface()

        # font
        self.font = pygame.font.Font(join('graphics', 'RussoOne.ttf'), 30)

        # increment
        self.increment_height = self.surface.get_height() /3

    def display_text(self, pos, text):
        

    def run(self):
        self.surface.fill(GRAY)
        for i, text in enumerate(['Score', 'Level', 'Lines']):
            x = self.surface.get_width() / 2
            y = self.increment_height / 2 + i * self.increment_height
            self.display_text((x, y), text)

        self.display_surface.blit(self.surface, self.rect)
