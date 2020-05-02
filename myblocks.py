#!/usr/bin/env python3
#coding: utf-8
""" myblocks.py """

import sys
import math
import random
from enum import Enum
import pygame
from pygame.locals import *

WINDOW_RECT = Rect(0, 0, 600, 800)                  # ウィンドウのサイズ
FPS = 30                                            # ゲームのFPS
BLOCK_SET_X = 15                                     # ブロック配置数（横）
BLOCK_SET_Y = 10                                     # ブロック配置数（縦）
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

class GameStatus(Enum):
    """ ゲームの状態 """
    START = 1               # スタート画面
    PLAY = 2                # ゲーム中
    END = 3                 # ゲーム終了

class Block:
    """ ブロック　オブジェクト """
    def __init__(self, type, x, y):
        self.type = type
        # ブロックの位置とサイズ
        blockx = ((WINDOW_RECT.width - 20) / BLOCK_SET_X) * x + 10
        blocky = y * 35 + 10
        blockw = (WINDOW_RECT.width - 20) / BLOCK_SET_X - 5
        blockh = 30
        self.rect = Rect(blockx, blocky, blockw, blockh)
        # ブロックの色の設定（タイプ別）
        if self.type == 0:
            self.col = ColorRGB.green
        elif self.type == 1:
            self.col = ColorRGB.blue
        elif self.type == 2:
            self.col = ColorRGB.aqua
        elif self.type == 3:
            self.col = ColorRGB.red
        elif self.type == 4:
            self.col = ColorRGB.maroon
        elif self.type == 5:
            self.col = ColorRGB.yellow

    def draw(self, surfase):
        """ ブロックを描画 """
        pygame.draw.rect(surfase, self.col, self.rect)

class Paddle:
    """ パドル　オブジェクト """
    def __init__(self, width=3):
        self.width = width
        self.col = ColorRGB.yellow
        self.rect = Rect(WINDOW_RECT.width / 2 - width * 20, 750,\
                         width * 40, 20)
    def update(self):
        """ パドルの移動 """
        # パドルの位置設定
        self.rect.centerx = pygame.mouse.get_pos()[0]

    def draw(self, surfase):
        """ パドルを描画 """
        self.rect.width = self.width * 40
        pygame.draw.rect(surfase, self.col, self.rect)

class Ball:
    """ ボールオブジェクト """
    def __init__(self, speed, blocks, paddle, balls):
        self.blocks = blocks                            # ブロックの参照
        self.paddle = paddle                            # パドルの参照
        self.balls = balls                              # ボールグループの参照
        self.col = ColorRGB.lime                        # ボールの色
        self.rect = Rect(300, 400, 20, 20)              # ボールのサイズ
        self.speed = speed                              # ボールのスピード
        self.dir = random.randint(-45, 45) +270         # ボールの最初の移動方向
    def draw(self, surfase):
        """ ボールを描画 """
        pygame.draw.ellipse(surfase, self.col, self.rect)
    def move(self):
        """ ボールを動かす """
        outblocks = []          # ボールとぶつかってるブロック（ブロックの効果処理用）
        balladd = False         # ボールが増えるフラグ
        self.rect.centerx += math.cos(math.radians(self.dir)) * self.speed
        self.rect.centery += math.sin(math.radians(self.dir)) * self.speed
        # ブロックとの衝突
        # 衝突したブロックの効果
        outblocks = [x for x in self.blocks
                     if x.rect.colliderect(self.rect)]
        for block in outblocks:
            if block.type == 1:             # スピードアップ
                self.speed += 5
            elif block.type == 2:           # スピードダウン
                if self.speed > 10:
                    self.speed -= 5
            elif block.type == 3:           # パドルアップ
                if self.paddle.width < 5:
                    self.paddle.width += 1
            elif block.type == 4:           # パドルダウン
                if self.paddle.width > 2:
                    self.paddle.width -= 1
            elif block.type == 5:           # ボール増殖
                balladd = True

        # 衝突したブロック以外のブロックを抽出
        prevlen = len(self.blocks)
        self.blocks = [x for x in self.blocks
                       if not x.rect.colliderect(self.rect)]
        if len(self.blocks) != prevlen:
            self.dir *= -1

        # ボールの増殖
        if balladd:
            self.balls.append(Ball(15, self.blocks, self.paddle, self.balls))

        # パドルと衝突？
        if self.paddle.rect.colliderect(self.rect):
            self.dir = 90 + (self.paddle.rect.centerx - self.rect.centerx) \
                    / self.paddle.rect.width * 80
            self.dir *= -1
        # 壁と衝突？
        if self.rect.centerx < 0 or self.rect.centerx > WINDOW_RECT.width:
            self.dir = 180 - self.dir
        if self.rect.centery < 0:
            self.dir = -self.dir            

def main():
    """ メインルーチン """
    pygame.init()                                           # pygameの初期化
    surfase = pygame.display.set_mode(WINDOW_RECT.size)     # ウィンドウの表示
    pygame.display.set_caption(u"ブロック崩し")
    fpsclock = pygame.time.Clock()
    blocks = []
    balls = []
    paddle = None

    myfont = pygame.font.SysFont(None, 80)
    mess_start = myfont.render("Click Game Start!", True, ColorRGB.yellow)
    mess_clear = myfont.render("        Cleared!", True, ColorRGB.yellow)
    mess_over = myfont.render("      Game Over!", True, ColorRGB.yellow)

    gamesta = GameStatus.START

    while True:                 # メインループ

        for event in pygame.event.get():        # イベント処理
            if event.type == QUIT:              # ゲーム終了
                pygame.quit()
                sys.exit(0)
            elif gamesta == GameStatus.START:   # スタート画面
                if event.type == MOUSEBUTTONUP: # クリックしたらゲームスタート
                    gamesta = GameStatus.PLAY
            elif gamesta == GameStatus.END:     # 終了画面
                if event.type == MOUSEBUTTONUP: # クリックしたらスタート画面
                    gamesta = GameStatus.START
                    paddle = None               # 各オブジェクトのクリア
                    balls.clear()
                    blocks.clear()

        # ゲームロジック
        if gamesta == GameStatus.START:
            if paddle is None:                                  # ゲームスタート時、1回のみオブジェクト作成
                # パドルの生成
                paddle = Paddle()
                # ボールの生成
                balls.append(Ball(15, blocks, paddle, balls))
                #ブロックの生成
                for y in range(BLOCK_SET_Y):
                    for x in range(BLOCK_SET_X):
                        # ブロックの種類
                        blocktype = random.randint(0, 10)
                        if blocktype <= 5:                  # ただのブロック5割出現設定
                            blocktype = 0
                        else:
                            blocktype = blocktype - 5
                        blocks.append(Block(blocktype, x, y))

        elif gamesta == GameStatus.PLAY:
            # ゲームプレイ画面
            # パドルの位置設定
            paddle.update()
            # ボールの移動
            for ball in balls:
                ball.blocks = blocks
                ball.move()
                blocks = ball.blocks
                balls = ball.balls
            # 画面外に落ちたボール以外を取得
            balls = [x for x in balls
                     if  x.rect.y < 810]
            # ゲームクリア判定
            if len(blocks) == 0 or len(balls) == 0:
                gamesta = GameStatus.END

        # 画面表示
        surfase.fill((0, 0, 0))                         # 画面のクリア
        for block in blocks:                            # ブロックの表示
            block.draw(surfase)
        paddle.draw(surfase)                            # パドルの表示
        for ball in balls:                              # ボールの表示
            ball.draw(surfase)
        if gamesta == GameStatus.START:                 # スタート、エンドの文字の表示
            surfase.blit(mess_start, (55, 600))
        elif gamesta == GameStatus.END and len(balls) == 0:
            surfase.blit(mess_over, (55, 600))
            surfase.blit(mess_start, (55, 650))
        elif gamesta == GameStatus.END and len(blocks) == 0:
            surfase.blit(mess_clear, (55, 600))
            surfase.blit(mess_start, (55, 650))

        pygame.display.update()
        fpsclock.tick(FPS)

if __name__ == '__main__':
    main()
