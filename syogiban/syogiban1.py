#!/usr/bin/env python3
#coding: utf-8
""" 将棋盤の作成。棋譜を並べる用 """

import sys                          # 終了用
import os                           # ファイル保存、読み込み用
import pygame
from pygame.locals import *

# 定数
WINDOW_RECT = Rect(0, 0, 775, 800)      # ウィンドウのサイズ
FPS = 10                                # ゲームのFPS
MASU_SIZE =64                           # マスのサイズ
BAN_SIZE = 9                            # 将棋盤のサイズ（9x9マス）
COLOR_BLACK = (0, 0, 0)                 # 線とか背景とかの色
COLOR_GRAY = (128, 128, 128)
COLOR_SILVER = (192, 192, 192)
COLOR_TEAL = (0, 128, 128)
COLOR_GOLDENROD = (218, 165 ,32)
COLOR_YELLOW = (255, 255, 0)
COLOR_WHITE = (255, 255, 255)
KOMA_MU = 14                        # 駒番号（無し）
KOMA_FU = 0                         # 歩
KOMA_KY = 1                         # 香車
KOMA_KE = 2                         # 桂馬
KOMA_GI = 3                         # 銀
KOMA_KI = 4                         # 金
KOMA_KA = 5                         # 角
KOMA_HI = 6                         # 飛車
KOMA_OU = 7                         # 王
KOMA_TO = 8                         # と
KOMA_NY = 9                         # 成香
KOMA_NK = 10                        # 成桂
KOMA_NG = 11                        # 成銀
KOMA_UM = 12                        # 馬
KOMA_RY = 13                        # 龍

MODE_RECT1 = Rect(110, 30, 120, 30)         # 駒を並べるラベル
MODE_RECT2 = Rect(230, 30, 120, 30)         # 将棋を指すラベル
SENTEGOTE_RECT1 = Rect(685, 65, 75, 30)     # 先手ラベル
SENTEGOTE_RECT2 = Rect(10, 65, 75, 30)      # 後手ラベル
SYOGIBAN_RECT = Rect(115, 100, 540, 540)    # 将棋盤内
KOMAOKIBA_RECT = Rect(10, 660, 452, 64)     # 駒置き場

def suzidann_rect(suzi, dan):
    """ 将棋のマス（筋、段）からRect情報を返す """
    posx = 659 - suzi * (MASU_SIZE - 4)
    posy = (dan - 1) * (MASU_SIZE - 4) + 103

    return Rect(posx, posy, MASU_SIZE - 5, MASU_SIZE - 5)

class SyogiMasu(pygame.sprite.Sprite):
    """ 将棋のマスクラス """
    def __init__(self, suzi, dan, koma, imgkoma):
        # 初期処理
        pygame.sprite.Sprite.__init__(self)             # スプライトの初期化？
        self.suzi = suzi                                # マスのx座標（９〜１）
        self.dan = dan                                  # マスのy座標（一〜九）
        self.koma = koma                                # 駒の種類
        self.sentegote = True                           # コマの向き（先手か後手か）
        self.sentaku = False                            # マスが選択されているか
        self.imgkoma = imgkoma.copy()                   # 駒イメージ（全種類）
        self.image = self.imgkoma[self.koma].copy()     # 表示する駒イメージ
        self.rect = suzidann_rect(self.suzi, self.dan)  # 表示位置

    def update(self):
        # マス上の駒の向きを設定
        if self.koma < KOMA_MU:
            if not self.sentegote:
                self.image = pygame.transform.flip(self.imgkoma[self.koma].copy(), False, True)

    def masuclick(self, pos, button, syougiban):
        # マスがクリックされた時
        if self.rect.collidepoint(pos):
            if button == BUTTON_LEFT or button == BUTTON_RIGHT:
                if syougiban.sentaku:
                    self.koma = syougiban.sentaku_koma
                    # 左ボタンだったら成る
                    if button == BUTTON_RIGHT and self.koma < KOMA_KI:
                        self.koma = self.koma + 8
                    elif button == BUTTON_RIGHT and KOMA_KI < self.koma < KOMA_OU:
                        self.koma = self.koma + 7
                    self.image = self.imgkoma[self.koma]
                    self.sentegote = syougiban.sentegote
                    syougiban.sentaku = False
                else:
                    # 非選択状態でマスをクリックすると駒を消す
                    self.koma = KOMA_MU
                    self.image = self.imgkoma[KOMA_MU]


class KomaokibaMasu(pygame.sprite.Sprite):
    """ 駒置き場の駒 """
    def __init__(self, koma, imgkoma):
        # 初期処理
        pygame.sprite.Sprite.__init__(self)         # スプライトの初期化？
        self.koma = koma                            # 駒の種類
        self.sentaku = False                        # マスが選択されているか
        self.imgkoma = imgkoma.copy()               # 駒イメージ（全種類）
        self.image = self.imgkoma[self.koma].copy() # 表示する駒イメージ
        self.rect = Rect(13 + (MASU_SIZE - 8) * koma, 663, MASU_SIZE - 10, MASU_SIZE -5)  # 表示位置

    def masuclick(self, pos, button, syougiban):
        # 駒がクリックされた時
        if button == BUTTON_LEFT and self.rect.collidepoint(pos):
            # 右クリックされた駒を選択状態にする
            pygame.draw.rect(syougiban.screen, COLOR_TEAL, self.rect, 0)
            self.sentaku = True
            syougiban.sentaku = True
            syougiban.sentaku_koma = self.koma
        else:
            pygame.draw.rect(syougiban.screen, COLOR_WHITE, self.rect, 0)
            self.sentaku = False


class komadaimasu(pygame.sprite.Sprite):
    """ 駒台の駒 """
    def __init__(self, koma, imgkoma, sentegote):
        # 初期処理
        pygame.sprite.Sprite.__init__(self)             # スプライトの初期化？
        self.font = pygame.font.SysFont("Noto Sans CJK JP", 15)     # 文字表示用フォント
        self.koma = koma                                # 駒の種類
        self.komakazu = 0                               # 駒の枚数
        self.sentaku = False                            # マスが選択されているか
        self.imgkoma = imgkoma.copy()                   # 駒イメージ（全種類）
        self.sentegote = sentegote                      # 先手か後手か
        if not self.sentegote:
            self.rect = Rect(12, 120 + MASU_SIZE * koma, MASU_SIZE + 10, MASU_SIZE)      # 表示位置
        else:
            self.rect = Rect(687, 110 + MASU_SIZE * koma, MASU_SIZE + 10, MASU_SIZE)     # 表示位置
        self.image = pygame.Surface((self.rect.width, self.rect.height))     # 表示する駒イメージ

    def update(self):
        # マス上の駒の向きを設定
        if self.koma < KOMA_MU:
            self.image.fill(COLOR_WHITE)
            if self.sentegote:
                self.image.fill(COLOR_WHITE)
                self.image.blit(self.imgkoma[self.koma], (0, 0))
            else:
                self.image.fill(COLOR_WHITE)
                self.image.blit(pygame.transform.flip(self.imgkoma[self.koma], False, True), (0, 0))

            # コマの数を表示
            text = self.font.render("x" + str(self.komakazu).zfill(2), True, COLOR_BLACK)
            self.image.blit(text, (47, 15))

    def masuclick(self, pos, button, syougiban):
        # マスがクリックされた時
        if self.rect.collidepoint(pos) and button == BUTTON_LEFT:
            # 右クリックだと増加
            self.komakazu += 1
            if self.komakazu > 20:
                self.komakazu = 20
            syougiban.sentaku = False
        elif self.rect.collidepoint(pos) and button == BUTTON_RIGHT:
            # 左クリックだと減少
            self.komakazu -= 1
            if self.komakazu < 0:
                self.komakazu = 0
            syougiban.sentaku = False

class SyogiBan:
    """ 将棋盤メインクラス """
    def __init__(self):
        # 初期処理
        pygame.init()                                               # pygameの初期化
        clock = pygame.time.Clock()                                 # fps用
        self.screen = pygame.display.set_mode(WINDOW_RECT.size)     # メインスクリーンの生成
        self.screen.fill(COLOR_SILVER)                              # メインスクリーンを灰色にする
        pygame.display.set_caption("将棋盤")                        # タイトルバーの設定
        self.font = pygame.font.SysFont("Noto Sans CJK JP", 20)     # 文字表示用フォント

        # 画像ファイルの読み込み
        # 駒
        image = pygame.image.load(os.path.dirname(__file__) + "/data/syogi_koma.png").convert()
        image_array = pygame.surfarray.array3d(image)
        self.koma = []
        count = 0
        for y in range(0, 256, 128):
            for x in range(0, 1024, 128):
                self.koma.append(pygame.surfarray.make_surface(
                                    image_array[x:x + 128, y:y + 128]))
                self.koma[count] = pygame.transform.scale(self.koma[count], (MASU_SIZE - 10, MASU_SIZE - 10))
                colorkey = self.koma[count].get_at((0, 0))
                self.koma[count].set_colorkey(colorkey)
                count += 1
    
        self.koma[KOMA_MU].fill(COLOR_GOLDENROD)    # 駒なしは盤の色で塗りつぶす

        # マスオブジェクトの生成
        group_masu = pygame.sprite.RenderUpdates()
        for suzi in range(1, 10):
            for dan in range(1, 10):
                group_masu.add(SyogiMasu(suzi, dan, KOMA_MU, self.koma))

        # 駒置き場の駒生成
        group_komaokiba = pygame.sprite.RenderUpdates()
        for i in range(KOMA_FU, KOMA_TO):
            group_komaokiba.add(KomaokibaMasu(i, self.koma))

        # 駒台の駒生成
        group_komadaimasu = pygame.sprite.RenderUpdates()
        for i in range(KOMA_FU, KOMA_OU):
            group_komadaimasu.add(komadaimasu(i, self.koma, True))      # 先手用
        for i in range(KOMA_FU, KOMA_OU):
            group_komadaimasu.add(komadaimasu(i, self.koma, False))     # 後手用

        self.mode = True                # 並べる（True）指す（False）
        self.sentegote = True           # 先手（True）　後手（False）
        self.sentaku = False            # 選択中のマスがあるか？
        self.sentaku_koma = KOMA_MU     # 選択中の駒

        # 下絵の描画
        # 盤
        pygame.draw.rect(self.screen, COLOR_GOLDENROD, SYOGIBAN_RECT, 0)
        pygame.draw.rect(self.screen, COLOR_BLACK, SYOGIBAN_RECT, 2)
        for num in range(160, 640, 60):
            pygame.draw.line(self.screen, COLOR_BLACK, (115, num), (655, num), 2)
            pygame.draw.line(self.screen, COLOR_BLACK, (num + 15, 100), (num + 15, 640), 2)
        # 座標
        text = self.font.render("９　　８　　７　　６　　５　　４　　３　　２　　１", True, COLOR_BLACK)
        self.screen.blit(text, (135, 75))
        text = self.font.render("一", True, COLOR_BLACK)
        self.screen.blit(text, (658, 110))
        text = self.font.render("ニ", True, COLOR_BLACK)
        self.screen.blit(text, (658, 170))
        text = self.font.render("三", True, COLOR_BLACK)
        self.screen.blit(text, (658, 230))
        text = self.font.render("四", True, COLOR_BLACK)
        self.screen.blit(text, (658, 290))
        text = self.font.render("五", True, COLOR_BLACK)
        self.screen.blit(text, (658, 350))
        text = self.font.render("六", True, COLOR_BLACK)
        self.screen.blit(text, (658, 410))
        text = self.font.render("七", True, COLOR_BLACK)
        self.screen.blit(text, (658, 470))
        text = self.font.render("八", True, COLOR_BLACK)
        self.screen.blit(text, (658, 530))
        text = self.font.render("九", True, COLOR_BLACK)
        self.screen.blit(text, (658, 590))
        # 駒台
        # 後手の駒台
        pygame.draw.rect(self.screen, COLOR_WHITE, (10, 100, 80, 540), 0)
        pygame.draw.rect(self.screen, COLOR_BLACK, (10, 100, 80, 540), 2)
        # 先手の駒台
        pygame.draw.rect(self.screen, COLOR_WHITE, (685, 100, 80, 540), 0)
        pygame.draw.rect(self.screen, COLOR_BLACK, (685, 100, 80, 540), 2)
        # モード
        pygame.draw.rect(self.screen, COLOR_BLACK, (110, 30, 240, 30), 2)
        # 駒置き場
        pygame.draw.rect(self.screen, COLOR_WHITE, KOMAOKIBA_RECT, 0)
        pygame.draw.rect(self.screen, COLOR_BLACK, KOMAOKIBA_RECT, 2)

        # メインループ
        while True:
            for event in pygame.event.get():
                # 終了処理
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit(0)
                # マウスがクリックされた時
                if event.type == MOUSEBUTTONDOWN:
                    # モードのクリック
                    if MODE_RECT1.collidepoint(event.pos):
                        self.mode = True
                    elif MODE_RECT2.collidepoint(event.pos):
                        self.mode = False
                    # 先手後手クリック
                    elif SENTEGOTE_RECT1.collidepoint(event.pos):
                        self.sentegote = True
                    elif SENTEGOTE_RECT2.collidepoint(event.pos):
                        self.sentegote = False

                    tmpsentaku = False          # 選択されたマスがあるかの確認用

                    # 将棋盤内のマスクリック
                    for sprite in group_masu:
                        sprite.masuclick(event.pos, event.button, self)
                        if sprite.sentaku:
                            tmpsentaku = True
                    # 駒置き場のクリック
                    for sprite in group_komaokiba:
                        sprite.masuclick(event.pos, event.button, self)
                        if sprite.sentaku:
                            tmpsentaku = True
                    # 駒台のクリック
                    for sprite in group_komadaimasu:
                        sprite.masuclick(event.pos, event.button, self)
                        if sprite.sentaku:
                            tmpsentaku = True
                    
                    self.sentaku = tmpsentaku

            self.draw()
            group_masu.update()
            group_masu.draw(self.screen)
            group_komaokiba.draw(self.screen)
            group_komadaimasu.update()
            group_komadaimasu.draw(self.screen)

            pygame.display.update()
            clock.tick(FPS)

    def draw(self):
        # 先手後手の表示
        if self.sentegote:
            pygame.draw.rect(self.screen, COLOR_BLACK, SENTEGOTE_RECT2, 2)
            text = self.font.render("▽後手", True, COLOR_WHITE)
            self.screen.blit(text, (15, 65))
            pygame.draw.rect(self.screen, COLOR_BLACK, SENTEGOTE_RECT1, 2)
            text = self.font.render("▲先手", True, COLOR_BLACK)
            self.screen.blit(text, (690, 65))
        else:
            pygame.draw.rect(self.screen, COLOR_BLACK, SENTEGOTE_RECT2, 2)
            text = self.font.render("▽後手", True, COLOR_BLACK)
            self.screen.blit(text, (15, 65))
            pygame.draw.rect(self.screen, COLOR_BLACK, SENTEGOTE_RECT1, 2)
            text = self.font.render("▲先手", True, COLOR_WHITE)
            self.screen.blit(text, (690, 65))

        # モード
        if self.mode:
            text = self.font.render("駒を並べる", True, COLOR_BLACK)
            self.screen.blit(text, (120, 30))
            text = self.font.render("将棋を指す", True, COLOR_WHITE)
            self.screen.blit(text, (240, 30))
        else:
            text = self.font.render("駒を並べる", True, COLOR_WHITE)
            self.screen.blit(text, (120, 30))
            text = self.font.render("将棋を指す", True, COLOR_BLACK)
            self.screen.blit(text, (240, 30))




if __name__ == '__main__':
    SyogiBan()

