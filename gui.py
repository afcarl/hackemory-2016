import pygame
from pygame.locals import *
import random
import time
import datetime
import pyowm

rr = random.randrange

pygame.init()

WIDTH, HEIGHT = 852, 1568

FONT_FAM = 'monospace'
SMALL_FONT, MEDIUM_FONT, LARGE_FONT = 16, 25, 36
BUFFER = 5

# add objects here to update them every cycle
SCREEN_OBJECTS = set()


class RectangleObject:
    def __init__(self, x, y, width, height, color=(255, 255, 255), line_width=5):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.color = color
        self.line_width = line_width

    def update(self):
        draw_rect(self.x, self.y, self.width, self.height, self.color, self.line_width)


class TextObject:
    """ Text object with custom "update" method """

    def __init__(self, x, y, size='s', text=None, color=(255, 255, 255), get_text=None):
        if size.lower() in ['s', 'small']: self.font_size = SMALL_FONT 
        elif self.lower() in ['m', 'medium']: self.font_size = MEDIUM_FONT
        elif self.lower in ['l', 'large']: self.font_size = LARGE_FONT
        else:
            try:
                self.font_size = int(size)
            except:
                raise ValueError('Inappropriate argument for "size": {}'.format(size))

        self.font = pygame.font.SysFont(FONT_FAM, self.font_size)

        self.x, self.y = x, y
        self.color = color
        self.text = text
        self.get_text = get_text

    def update(self, text=None):
        if self.text is None and self.get_text is not None:
            text = self.get_text()
        
        draw_text(self.x, self.y, self.text if text is None else text, color=self.color, font=self.font)


class TextList:
    def __init__(self, x, y, color=(255, 255, 255)):
        self.x, self.y = x, y
        self.color = color

    def update(self, text=None) 


def rand_color():
    return (rr(0, 256), rr(0, 256), rr(0, 256))


def toggle_fullscreen():
    """ Turn fullscreen mode on or off """
    
    screen = pygame.display.get_surface()
    tmp = screen.convert()
    caption = pygame.display.get_caption()
    cursor = pygame.mouse.get_cursor()

    w, h = screen.get_width(), screen.get_height()
    flags = screen.get_flags()
    bits = screen.get_bitsize()

    pygame.display.quit()
    pygame.display.init()

    screen = pygame.display.set_mode((w, h), flags ^ FULLSCREEN, bits)
    screen.blit(tmp, (0, 0))
    pygame.display.set_caption(*caption)
    
    pygame.key.set_mods(0)

    pygame.mouse.set_cursor(*cursor)

    return screen


def draw_text(x, y, text, color=(255, 255, 255), font=SMALL_FONT):
    """ Draw text at position (x, y) """

    if text is None:
        return
    
    screen = pygame.display.get_surface()
    screen.blit(font.render(text, True, color), (x, y))


def draw_rect(x, y, width, height, color=(255, 255, 255), line_width=5):
    """ Draw rectangle of dimensions (width, height) at position (x, y) """
    
    screen = pygame.display.get_surface()
    pygame.draw.rect(screen, color, (x, y, width, height), line_width)


def rand_block(dim=32):
    """ Draws a random square """

    draw_rect(rr(0, WIDTH-dim), rr(0, HEIGHT-dim), dim, dim)


def running():
    """ Method for actually running the display """
    
    for e in pygame.event.get():
        if e.type is QUIT or (e.type is KEYDOWN and e.key == K_ESCAPE):
            return False

    rand_block(rr(10, 100))

    screen = pygame.display.get_surface()
    screen.fill((0, 0, 0))

    for screen_object in SCREEN_OBJECTS:
        screen_object.update()
    
    pygame.display.flip()
    
    return True

if __name__ == '__main__':
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('this is a test')
    
    toggle_fullscreen()

    owm = pyowm.OWM('53f077b99bbb682c5db7f3906eaa1cde')
    
    observation = owm.weather_at_place('Atlanta,us')
    w = observation.get_weather()

    SCREEN_OBJECTS.add(TextObject(BUFFER, BUFFER, text='Current Time'))
    SCREEN_OBJECTS.add(TextObject(BUFFER, BUFFER + (BUFFER + SMALL_FONT), get_text=lambda: time.strftime('%H:%M:%S')))
    SCREEN_OBJECTS.add(TextObject(BUFFER, BUFFER + 2 * (BUFFER + SMALL_FONT), get_text=lambda: repr(observation.get_weather().get_temperature('fahrenheit')['temp']) + ' degrees'))

    while running():
        time.sleep(1 // 10) # update at 10 Hz
