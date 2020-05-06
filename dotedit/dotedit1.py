#!/usr/bin/env python3
#coding: utf-8
""" dotedit.py """
import sys
import pygame
from pygame.locals import *

WINDOW_RECT = Rect(0, 0, 987, 631)                 # ウィンドウのサイズ
FPS = 30                                            # ゲームのFPS

class ColorRGB:
    """ カラーRGB """
    black = (0, 0, 0)
    navy = (0, 0, 128)
    blue = (0, 0, 255)
    green = (0, 128, 0)
    teal = (0, 128, 128)
    lime = (0, 255, 0)
    aqua = (0, 255, 255)
    maroon = (128, 0, 0)
    purple = (128, 0, 128)
    olive = (128, 128, 0)
    gray = (128, 128, 128)
    silver = (192, 192, 192)
    red = (255, 0, 0)
    fuchsia = (255, 0, 255)
    yellow = (255, 255, 0)
    white = (255, 255, 255)

class MenuBar():
    """ メニューバー """
    def __init__(self, rect):
        self.rect = rect
        self.screen = pygame.Surface(rect.size)
    def draw(self, screen):
        """ メニューバーの描画 """
        self.screen.fill(ColorRGB.white)
        pygame.draw.rect(self.screen, ColorRGB.black, (0, 0, self.rect.width, self.rect.height), 6)
        screen.blit(self.screen, self.rect)

class EditScreen():
    """ 画面内の画面 """
    def __init__(self, rect):
        self.editcelx = 32              # 32 x 32 のドット絵を書く
        self.editcely = 32
        self.celsize = 15               # 1個のセルのサイズ
        self.drawcol = (ColorRGB.black) # クリックした場所に塗る色
        # 全セルに白を設定
        self.cells = [[ColorRGB.white for x in range(self.editcelx)] for y in range(self.editcely)]

        self.rect = rect
        self.rect.size = (self.editcelx * self.celsize + 6, self.editcely * self.celsize + 6)
        self.screen = pygame.Surface(self.rect.size)

    def draw(self, screen):
        """ エディタ部の描画 """
        self.screen.fill(ColorRGB.white)
        pygame.draw.rect(self.screen, ColorRGB.black, (0, 0, self.rect.width, self.rect.height), 6)

        # セルの描画
        for i, celll in enumerate(self.cells):
            for j, cell in enumerate(celll):
                cellrect = Rect(i * self.celsize +3, j * self.celsize + 3,
                                self.celsize, self.celsize)
                pygame.draw.rect(self.screen, cell, cellrect)               # セルの色
                pygame.draw.rect(self.screen, ColorRGB.gray, cellrect, 1)   # セルの枠
        # 真ん中に線を引く
        pygame.draw.line(self.screen, ColorRGB.black, (self.rect.centerx - self.rect.left, 0),
                         (self.rect.centerx - self.rect.left, self.rect.bottom), 2)
        pygame.draw.line(self.screen, ColorRGB.black, (0, self.rect.centery - self.rect.top),
                         (self.rect.width, self.rect.centery - self.rect.top), 2)

        screen.blit(self.screen, self.rect)

class PaletteScreen():
    """ パレット """
    def __init__(self, rect):
        self.rect = rect
        self.screen = pygame.Surface(rect.size)
        self.palett = [x for x in list(vars(ColorRGB).values()) if isinstance(x, tuple)]
        self.selectcol = self.palett[0]

    def draw(self, screen):
        """ パレットの描画 """
        self.screen.fill(ColorRGB.gray)
        pygame.draw.rect(self.screen, ColorRGB.black, (0, 0, self.rect.width, self.rect.height), 6)

        # 選択中の色表示
        pygame.draw.rect(self.screen, self.selectcol, (10, 10, 55, 55))
        # パレットの色表示
        for i, j in enumerate(self.palett):
            pygame.draw.rect(self.screen, j, (70 + (i % 8) * 30, 10 + (i // 8) * 30, 25, 25))
            pygame.draw.rect(self.screen, ColorRGB.black,
                             (70 + (i % 8) * 30, 10 + (i // 8) * 30, 25, 25), 2)

        screen.blit(self.screen, self.rect)

class ViewScreen():
    """ 画像全体の画面 """
    def __init__(self, rect):
        self.rect = rect
        self.screen = pygame.Surface(rect.size)
    def draw(self, screen):
        """ 画像全体の描画 """
        self.screen.fill(ColorRGB.white)
        pygame.draw.rect(self.screen, ColorRGB.black, (0, 0, self.rect.width, self.rect.height), 6)
        screen.blit(self.screen, self.rect)

class MsgScreen():
    """ メッセージの画面（デバック用？） """
    def __init__(self, rect):
        self.rect = rect
        self.screen = pygame.Surface(rect.size)
        self.font = pygame.font.SysFont(None, 30)
    def draw(self, screen):
        """ 画像全体の描画 """
        self.screen.fill(ColorRGB.white)
        pygame.draw.rect(self.screen, ColorRGB.black, (0, 0, self.rect.width, self.rect.height), 6)
        msg = 'mouse pos(x, y):%s, %s' % pygame.mouse.get_pos()
        self.screen.blit(self.font.render(msg, True, ColorRGB.black), (5, 5))
        screen.blit(self.screen, self.rect)

def main():
    """ メイン処理 """
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_RECT.size)
    pygame.display.set_caption("dotedit")
    clock = pygame.time.Clock()

    menubar = MenuBar(Rect(5, 5, WINDOW_RECT.width - 10, 50))
    editscreen = EditScreen(Rect(5, 60, 300, 200))
    palettescreen = PaletteScreen(Rect(5, 551, 486, 75))
    viewscreen = ViewScreen(Rect(496, 60, 486, 486))
    msgscreen = MsgScreen(Rect(496, 551, 486, 75))

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit(0)

        screen.fill(ColorRGB.silver)

        menubar.draw(screen)
        editscreen.draw(screen)
        palettescreen.draw(screen)
        viewscreen.draw(screen)
        msgscreen.draw(screen)

        pygame.display.update()
        clock.tick(FPS)

if __name__ == '__main__':
    main()
