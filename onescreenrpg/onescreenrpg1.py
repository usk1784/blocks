#!/usr/bin/env python3
#coding: utf-8
""" １画面で完結するRPGを目指すーその１マップの表示 """

import sys                          # 終了用
import os                           # ファイル保存、読み込み用
import pygame
from pygame.locals import *

WINDOW_RECT = Rect(0, 0, 1110, 900)                                     # ウィンドウのサイズ
FPS = 20                                                                # ゲームのFPS
MAPCHIP_FILENAME = os.path.dirname(__file__) + "/data/mapchip.png"      # マップチップファイル名
CHIP_SIZE = (32, 32)                                                    # 各チップのサイズ（ドット）
MAP_SIZA = (25, 20)                                                     # マップのサイズ（横,縦）
# 線とか背景とかの色
COLOR_BLACK = (0, 0, 0)
COLOR_GRAY = (128, 128, 128)
COLOR_SILVER = (192, 192, 192)
COLOR_SKYBRUE = (0, 255, 255)
COLOR_WHITE = (255, 255, 255)

class Map:
    """ マップクラス \n
    マップデータの読み込み、マップの表示など """
    # マップデータ
    mapdata = [[3, 3, 2, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [3, 3, 2, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [3, 3, 2, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [2, 2, 2, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [2, 2, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 4, 4, 4, 0, 0, 0, 0, 0, 0, 4],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 4, 4, 4, 4, 0, 0, 4, 4],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 4, 4],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 4],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 4, 4],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 4, 4, 4]]

    def __init__(self, screen):
        # 画像ファイル(マップチップ)の読み込み
        self.mapchip = pygame.image.load(MAPCHIP_FILENAME).convert()
        self.mapchiplist = []

        # マップチップの分割
        for chiptop in range(0, self.mapchip.get_width(), CHIP_SIZE[0]):
            mapchip = pygame.Surface(CHIP_SIZE)
            mapchip.blit(self.mapchip, (0, 0), (chiptop, 0, CHIP_SIZE[0], CHIP_SIZE[1]))
            self.mapchiplist.append(mapchip)

        # 画像の表示
        screen.blit(self.mapchip, (10, 10))

        for row in range(MAP_SIZA[1]):
            for col in range(MAP_SIZA[0]):
                if self.mapdata[row][col] < len(self.mapchiplist):    # マップチップに無いデータは表示しない
                    screen.blit(self.mapchiplist[self.mapdata[row][col]],\
                                (300 + col * 32, 10 + row * 32))



class OneScreenRPG:
    """ OneScreenRPGメインクラス """

    def __init__(self):
        # 初期処理
        pygame.init()                                       # pygameの初期化
        clock = pygame.time.Clock()                         # fps用
        self.screen = pygame.display.set_mode(WINDOW_RECT.size)  # メインスクリーンの生成
        self.screen.fill(COLOR_BLACK)
        pygame.display.set_caption("OneScreenRPG")          # タイトルバーの設定

        # マップオブジェクトの生成
        self.map = Map(self.screen)

        # メインループ
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit(0)

            pygame.display.update()
            clock.tick(FPS)

if __name__ == '__main__':
    OneScreenRPG()
