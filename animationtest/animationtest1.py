#!/usr/bin/env python3
#coding: utf-8
""" animationtest.py アニメーション表示 """
import sys                          # 終了用
import os                           # ファイル保存、読み込み用
import pygame
from pygame.locals import *

WINDOW_RECT = Rect(0, 0, 300, 300)                  # ウィンドウのサイズ
FPS = 20                                            # ゲームのFPS

# 線とか背景とかの色
COLOR_BLACK = (0, 0, 0)
COLOR_GRAY = (128, 128, 128)
COLOR_SILVER = (192, 192, 192)
COLOR_SKYBRUE = (0, 255, 255)
COLOR_WHITE = (255, 255, 255)

def main():
    """ メイン処理 """
    pygame.init()                                       # pygameの初期化
    pygame.mixer.quit()                                 # CPU使用率を下げるため
    screen = pygame.display.set_mode(WINDOW_RECT.size)  # メインスクリーンの生成
    screen.fill(COLOR_SKYBRUE)
    pygame.display.set_caption("animationtest")         # タイトルバーの設定
    clock = pygame.time.Clock()                         # fps用

    # 画像ファイルの読み込み
    image = pygame.image.load(os.path.dirname(__file__) + "/anime1.png").convert()
    # 画像ファイルからキャラデータを取得(原寸)
    image1 = []
    image1.append(pygame.Surface((16, 16)))
    image1[0].blit(image, (0, 0), Rect(0, 0, 16, 16))
    image1.append(pygame.Surface((16, 16)))
    image1[1].blit(image, (0, 0), Rect(16, 0, 16, 16))
    image1.append(pygame.Surface((16, 16)))
    image1[2].blit(image, (0, 0), Rect(0, 16, 16, 16))
    # 画像ファイルからキャラデータを取得(3倍？)
    image2 = []
    image2.append(pygame.Surface((16, 16)))
    image2[0].blit(image, (0, 0), Rect(0, 0, 16, 16))
    image2[0] = pygame.transform.smoothscale(image2[0], (48, 48))
    image2.append(pygame.Surface((16, 16)))
    image2[1].blit(image, (0, 0), Rect(16, 0, 16, 16))
    image2[1] = pygame.transform.smoothscale(image2[1], (48, 48))
    image2.append(pygame.Surface((16, 16)))
    image2[2].blit(image, (0, 0), Rect(0, 16, 16, 16))
    image2[2] = pygame.transform.smoothscale(image2[2], (48, 48))

    framecount = 0

    # メインループ
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit(0)

        # 画像表示
        screen.blit(image1[0], (10, 10))
        screen.blit(image1[1], (30, 10))
        screen.blit(image1[2], (50, 10))

        if framecount // 10 == 0:
            screen.blit(image1[0], (20, 40))
            screen.blit(image2[0], (20, 100))
            screen.blit(image1[0], (20, 70))
            screen.blit(image2[0], (20, 150))
        elif framecount // 10 == 1:
            screen.blit(image1[1], (20, 40))
            screen.blit(image2[1], (20, 100))
            screen.blit(image1[2], (20, 70))
            screen.blit(image2[2], (20, 150))

        pygame.display.update()
        clock.tick(FPS)
        framecount += 1
        if framecount == 20:
            framecount = 0

if __name__ == '__main__':
    main()
