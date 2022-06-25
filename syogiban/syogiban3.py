#!/usr/bin/env python3
#coding: utf-8
""" 将棋盤の作成。棋譜を並べる用 """
""" Ver3.0 : 2がうまく行かないので、ほぼ作り変え（汗 """
""" 将棋の内部処理と画面の表示処理を分けることに """
from operator import index, truediv
import sys                          # 終了用
import os                           # ファイル保存、読み込み用
import numpy as np                  # 配列処理用
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
KOMA_FU = 0                         # 歩
KOMA_KY = 1                         # 香車
KOMA_KE = 2                         # 桂馬
KOMA_GI = 3                         # 銀
KOMA_KA = 4                         # 角
KOMA_HI = 5                         # 飛車
KOMA_KI = 6                         # 金
KOMA_OU = 7                         # 王
KOMA_TO = 8                         # と
KOMA_NY = 9                         # 成香
KOMA_NK = 10                        # 成桂
KOMA_NG = 11                        # 成銀
KOMA_UM = 12                        # 馬
KOMA_RY = 13                        # 龍
KOMA_FU_G = 20                      # 歩（後手）
KOMA_KY_G = 21                      # 香車（後手）
KOMA_KE_G = 22                      # 桂馬（後手）
KOMA_GI_G = 23                      # 銀（後手）
KOMA_KA_G = 24                      # 角（後手）
KOMA_HI_G = 25                      # 飛車（後手）
KOMA_KI_G = 26                      # 金（後手）
KOMA_OU_G = 27                      # 王（後手）
KOMA_TO_G = 28                      # と（後手）
KOMA_NY_G = 29                      # 成香（後手）
KOMA_NK_G = 30                      # 成桂（後手）
KOMA_NG_G = 31                      # 成銀（後手）
KOMA_UM_G = 32                      # 馬（後手）
KOMA_RY_G = 33                      # 龍（後手）
KOMA_SENTAKU = 100                  # 選択された駒
KOMA_MU = 200                       # 駒無し
KOMA_KABE = 999                     # 壁

HKOMA_MU = 34                       # 表示用の駒無し

MASU_SYURUI_SYOGUMASU = 0           # 選択中のマスの種類判別用
MASU_SYURUI_KOMAOKIBA = 1
MASU_SYURUI_KOMADAIMASU = 2

MODE_RECT1 = Rect(110, 30, 120, 30)         # 駒を並べるラベル
MODE_RECT2 = Rect(230, 30, 120, 30)         # 将棋を指すラベル
SENTEGOTE_RECT1 = Rect(685, 65, 75, 30)     # 先手ラベル
SENTEGOTE_RECT2 = Rect(10, 65, 75, 30)      # 後手ラベル
SYOGIBAN_RECT = Rect(115, 100, 540, 540)    # 将棋盤内
KOMAOKIBA_RECT = Rect(10, 660, 452, 64)     # 駒置き場


def index_rect(index):
    """ 将棋のマス（index）からRect情報を返す """
    posx = 659 - (9 - (index % 9)) * (MASU_SIZE - 4)
    posy = index // 9 * (MASU_SIZE - 4) + 103

    return Rect(posx, posy, MASU_SIZE - 5, MASU_SIZE - 5)

class SyogiEngine():
    """ 将棋エンジンクラス """
    """ 将棋の盤面、駒の管理？ルールの判断？など？ """
    """ 将棋盤のマスは１次元の配列で管理 """
    """ 配列は０〜１０９
        ０〜９と１００〜１０９ は壁
        １０、２０，３０...９０ も壁
        １１〜１９から９１〜９９までが将棋盤のマスに対応 """

    def __init__(self):
        # 初期処理
        # 空の将棋盤（9＊9と壁）の作成
        self.setsyogiban()

        # 駒台作成
        # indexが0~6（歩〜金）で駒の数が入る
        self.komadai_sente = np.zeros(7, int)
        self.komadai_gote = np.zeros(7, int)

        self.mode = True                # 並べる（True）指す（False）
        self.sentegote = True           # 先手（True）　後手（False）

    def setsyogiban(self, haiti = None):
        # 将棋盤に駒をセットする（全マス）
        # haitiにリストがない場合は全マスクリア
        # haitiはリスト（1次元）
        if haiti == None:
            self.syogiban = np.full(110, 999, int)
            for index in range(10, 100):
                if (index % 10) != 0:
                    self.syogiban[index] = 200
        else:
            # haitiを将棋盤にセット
            return


    def getsyogiban(self):
        # 将棋盤の状態をリストで返す(壁の中のみ返す)

        retsyogiban = np.empty(81, int)
        count = 0

        for index in range(10, 100):
            if self.syogiban[index] != KOMA_KABE:

                retsyogiban[count] = self.syogiban[index]

                count += 1
        
        return retsyogiban

    def getsyogiban2(self):
        # 将棋盤の状態をリストで返す(壁の中のみ返す)
        # リストは2次元配列で返す

        retsyogiban = np.empty((9, 9), int)
        count = 0

        for index in range(10, 100):
            if self.syogiban[index] != KOMA_KABE:

                retsyogiban[count // 9, count % 9] = self.syogiban[index]

                count += 1

        return retsyogiban

    def setsyogimasu(self, zahyo, koma):
        # マスに駒をセットする（駒を並べるモード中）
        # 座標は１次元時のインデックスで指定

        if self.mode:   # 駒を並べるときのみ実行

            #座標からインデックスの計算
            index = (zahyo // 9 + 1) * 10 + zahyo % 9 + 1

            # 駒の設定
            self.syogiban[index] = koma

    def suzidann_index(suzi, dan):
        """ 将棋のマス（筋、段）からIndexを計算する """
        tmpx = 9 - suzi
        index = (dan - 1) * 9 + tmpx

        return index

    def index_suzidann(index):
        """ Indexから筋段を計算する """
        dan = index // 9 + 1
        suzi = 9 - (index % 9)

        return suzi, dan


class SyogiMasu(pygame.sprite.Sprite):
    """ 将棋のマスクラス """
    def __init__(self, index, imgkoma):
        # 初期処理
        pygame.sprite.Sprite.__init__(self, self.containers)             # スプライトの初期化？
        self.index = index                              # マスのインデックス
        self.koma = HKOMA_MU                            # 駒の種類
        self.images = imgkoma.copy()
        self.image = self.images[self.koma]             # 表示する駒イメージ
        self.rect = index_rect(self.index)              # 表示位置

    def update(self, syougiban):

        # 選択状態の表示
        if syougiban.sentaku and syougiban.sentaku_masu_syurui == MASU_SYURUI_SYOGUMASU\
                                            and self.index == syougiban.sentaku_masu_index:
            self.image.fill(COLOR_TEAL)
        else:
            self.image.fill(COLOR_GOLDENROD)


        if self.koma != KOMA_MU:
            # copyだと駒が重なって描画されたのでblit（多分、透過部分の描画処理はスルーされる？）
#            self.image = imgkoma[self.koma].copy()
            self.image.blit(self.images[self.koma].copy(), (0,0))
        else:
            self.image = self.images[HKOMA_MU].copy()


    def masuclick(self, button, syougiban):
        # 駒を並べるのとき
        if syougiban.mode:
            if button == BUTTON_LEFT or button == BUTTON_RIGHT:
                if syougiban.sentaku:
                    tmpkoma = syougiban.sentaku_koma
                    # 左ボタンだったら成る
                    if button == BUTTON_RIGHT and syougiban.sentaku_koma < KOMA_KI:
                        tmpkoma = tmpkoma + 8
                    # 後手なら後手の駒に
                    if not syougiban.sentegote:
                        tmpkoma = tmpkoma + 20

                    # 将棋エンジンに駒をセットする
                    syougiban.syogiengine.setsyogimasu(self.index, tmpkoma)
                else:
                    # 非選択状態でマスをクリックすると駒を消す
                    # 将棋エンジンに駒をセットする
                    syougiban.syogiengine.setsyogimasu(self.index, KOMA_MU)
        else:   # 将棋を指すの時
            if not syougiban.sentaku:   # 選択中の駒が無い時
                if self.koma != KOMA_MU:# マスに駒があったら選択中にする。
                    syougiban.sentaku = True
                    syougiban.sentaku_koma = self.koma
                    syougiban.sentaku_masu_syurui = MASU_SYURUI_SYOGUMASU
                    syougiban.sentaku_masu_index = self.index
            else:                       # 選択中の駒がある時
                # 自分のマスが選択中だった時
                if syougiban.sentaku_masu_syurui == MASU_SYURUI_SYOGUMASU\
                                                    and self.index == syougiban.sentaku_masu_index:
                    # 選択を解除
                    syougiban.sentaku = False





class KomaokibaMasu(pygame.sprite.Sprite):
    """ 駒置き場の駒 """
    def __init__(self, koma, imgkoma):
        # 初期処理
        pygame.sprite.Sprite.__init__(self, self.containers)         # スプライトの初期化？
        self.koma = koma                            # 駒の種類
        self.imgkoma = imgkoma.copy()               # 駒イメージ（全種類）
        self.image = self.imgkoma[self.koma].copy() # 表示する駒イメージ
        self.rect = Rect(13 + (MASU_SIZE - 8) * koma, 665, MASU_SIZE - 10, MASU_SIZE -5)  # 表示位置

    def update(self, syougiban):

        # 選択状態を表示
        if syougiban.sentaku and syougiban.sentaku_masu_syurui == MASU_SYURUI_KOMAOKIBA\
                                            and self.koma == syougiban.sentaku_masu_index:
            self.image.fill(COLOR_TEAL)
        else:
            self.image.fill(COLOR_GOLDENROD)

        self.image.blit(self.imgkoma[self.koma].copy(),(0,0)) # 表示する駒イメージ


    def masuclick(self, button, syougiban):
        # 駒がクリックされた時
        # 駒を並べる状態のときのみ実行
        if button == BUTTON_LEFT and syougiban.mode:
            if syougiban.sentaku and syougiban.sentaku_masu_syurui == MASU_SYURUI_KOMAOKIBA\
                                                and self.koma == syougiban.sentaku_masu_index:
                # すでに選択されていたら選択解除
                syougiban.sentaku = False
            else:
                # 右クリックされた駒を選択状態にする
                syougiban.sentaku = True
                syougiban.sentaku_koma = self.koma
                syougiban.sentaku_masu_syurui = MASU_SYURUI_KOMAOKIBA
                syougiban.sentaku_masu_index = self.koma


class KomadaiMasu(pygame.sprite.Sprite):
    """ 駒台の駒 """
    def __init__(self, koma, imgkoma, sentegote):
        # 初期処理
        pygame.sprite.Sprite.__init__(self, self.containers)             # スプライトの初期化？
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

    def update(self, syougiban):
        # マス上の駒の向きを設定
        if self.koma < KOMA_MU:
            self.image.fill(COLOR_GOLDENROD)
            if self.sentegote:
                self.image.blit(self.imgkoma[self.koma].copy(), (0, 0))
            else:
                self.image.blit(pygame.transform.flip(self.imgkoma[self.koma].copy(), False, True), (0, 0))

            # コマの数を表示
            text = self.font.render("x" + str(self.komakazu).zfill(2), True, COLOR_BLACK)
            self.image.blit(text, (47, 15))

    def masuclick(self, button, syougiban):
        # マスがクリックされた時
        if syougiban.mode:
            if button == BUTTON_LEFT:
                # 右クリックだと増加
                self.komakazu += 1
                if self.komakazu > 20:
                    self.komakazu = 20
                syougiban.sentaku = False
            elif button == BUTTON_RIGHT:
                # 左クリックだと減少
                self.komakazu -= 1
                if self.komakazu < 0:
                    self.komakazu = 0
                syougiban.sentaku = False

class MousePoint(pygame.sprite.Sprite):
    """ マウスポインター用のスプライト
        マウスがどのマスを指しているかの判定用（衝突判定で判断） """
    def __init__(self):
        # 初期処理
        pygame.sprite.Sprite.__init__(self, self.containers)             # スプライトの初期化？
        self.rect = Rect(0,0,1,1)               # 表示位置
        self.image = pygame.Surface((1, 1))     # 表示する駒イメージ
        self.image.fill(COLOR_BLACK)
        colorkey = self.image.get_at((0, 0))    # 透明のスプライト
        self.image.set_colorkey(colorkey)

    def update(self, syougiban):
        # マウスの位置に移動
        pos = pygame.mouse.get_pos()
        self.rect.x = pos[0]
        self.rect.y = pos[1]


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
        image = pygame.image.load(os.path.dirname(__file__) + "/data/syogi_koma3.png").convert()
        image_array = pygame.surfarray.array3d(image)
        self.koma_img = []
        count = 0
        for y in range(0, 256, 128):
            for x in range(0, 1024, 128):
                self.koma_img.append(pygame.surfarray.make_surface(
                                    image_array[x:x + 128, y:y + 128]))
                self.koma_img[count] = pygame.transform.scale(self.koma_img[count], (MASU_SIZE - 10, MASU_SIZE - 10))
                colorkey = self.koma_img[count].get_at((0, 0))
                self.koma_img[count].set_colorkey(colorkey)

                count += 1
        # 後手側の駒を設定（上下逆にした画像をコピー）
        # 無理やり定数に合わせるように画像をコピー
        self.koma_img = self.koma_img + [0, 1, 2, 3]
        self.koma_img = self.koma_img + self.koma_img

        # 後手の駒を上下逆にする
        for index in range(20, 34):
            self.koma_img[index] = pygame.transform.flip(self.koma_img[index], False, True)


        self.koma_img[HKOMA_MU].fill(COLOR_GOLDENROD)    # 駒なしは盤の色で塗りつぶす

        # 将棋エンジンの生成
        self.syogiengine = SyogiEngine()
        self.syogiban = self.syogiengine.getsyogiban()
        self.mode = True                # 並べる（True）指す（False）
        self.sentegote = True           # 先手（True）　後手（False）
        self.sentaku = False            # 選択中のマスがあるか？
        self.sentaku_koma = KOMA_MU     # 選択中の駒
        self.sentaku_masu_syurui = 0    # 選択中のマスの種類
        self.sentaku_masu_index = 0     # 選択中のマスのインデックス

        self.group_byouga = pygame.sprite.RenderUpdates()   # 描画用のスプライトグループ
        self.group_masu = pygame.sprite.Group()             # 将棋盤マスグループ
        self.group_komaokiba = pygame.sprite.Group()        # 駒置き場グループ
        self.group_komadaimasu = pygame.sprite.Group()      # 駒台グループ

        SyogiMasu.containers = self.group_byouga, self.group_masu
        KomaokibaMasu.containers = self.group_byouga, self.group_komaokiba
        KomadaiMasu.containers = self.group_byouga, self.group_komadaimasu

        MousePoint.containers = self.group_byouga

        # マスオブジェクトの生成
        for index in range(0, 81):
            SyogiMasu(index, self.koma_img)

        # 駒置き場の駒生成
        for i in range(KOMA_FU, KOMA_TO):
            KomaokibaMasu(i, self.koma_img)

        # 駒台の駒生成
        for i in range(KOMA_FU, KOMA_OU):
            KomadaiMasu(i, self.koma_img, True)      # 先手用
        for i in range(KOMA_FU, KOMA_OU):
            KomadaiMasu(i, self.koma_img, False)     # 後手用

        self.mouse_point = MousePoint()

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
        pygame.draw.rect(self.screen, COLOR_GOLDENROD, (10, 100, 80, 540), 0)
        pygame.draw.rect(self.screen, COLOR_BLACK, (10, 100, 80, 540), 2)
        # 先手の駒台
        pygame.draw.rect(self.screen, COLOR_GOLDENROD, (685, 100, 80, 540), 0)
        pygame.draw.rect(self.screen, COLOR_BLACK, (685, 100, 80, 540), 2)
        # モード
        pygame.draw.rect(self.screen, COLOR_BLACK, (110, 30, 240, 30), 2)
        # 駒置き場
        pygame.draw.rect(self.screen, COLOR_GOLDENROD, KOMAOKIBA_RECT, 0)
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
                        # 選択状態をクリア
                        self.sentaku = False
                        self.sentaku_koma = KOMA_MU
                    elif MODE_RECT2.collidepoint(event.pos):
                        self.mode = False
                        # 選択状態をクリア
                        self.sentaku = False
                        self.sentaku_koma = KOMA_MU
                        # 将棋を指すときは先手から
                        self.sentegote = True
                    # 先手後手クリック
                    if self.mode: #先手後手は駒を並べる時だけ変更可
                        if SENTEGOTE_RECT1.collidepoint(event.pos):
                            self.sentegote = True
                        elif SENTEGOTE_RECT2.collidepoint(event.pos):
                            self.sentegote = False

                    # 将棋盤内のマスクリック
                    clicksprite = pygame.sprite.spritecollide(self.mouse_point, self.group_masu, False)
                    if clicksprite:
                        clicksprite[0].masuclick(event.button, self)

                    # 駒置き場のクリック
                    clicksprite = pygame.sprite.spritecollide(self.mouse_point, self.group_komaokiba, False)
                    if clicksprite:
                        clicksprite[0].masuclick(event.button, self)

                    # 駒台のクリック
                    clicksprite = pygame.sprite.spritecollide(self.mouse_point, self.group_komadaimasu, False)
                    if clicksprite:
                        clicksprite[0].masuclick(event.button, self)

            self.update()
            self.draw()
            self.group_byouga.update(self)
            self.group_byouga.draw(self.screen)

            pygame.display.update()
            clock.tick(FPS)

    def update(self):
        # 将棋エンジンから駒の配置を取得
        self.syogiban = self.syogiengine.getsyogiban()

        index = 0

        for sprite in self.group_masu:
            sprite.koma = self.syogiban[index]
            index += 1


    def draw(self):
        # 先手後手の表示
        pygame.draw.rect(self.screen, COLOR_SILVER, SENTEGOTE_RECT2, 0)
        pygame.draw.rect(self.screen, COLOR_SILVER, SENTEGOTE_RECT1, 0)
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
        pygame.draw.rect(self.screen, COLOR_SILVER, (112, 32, 235, 26), 0)
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

