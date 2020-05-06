#!/usr/bin/env python3
#coding: utf-8
""" dotedit.py """
import sys
import pygame
from pygame.locals import *

WINDOW_RECT = Rect(0, 0, 987, 631)                  # ウィンドウのサイズ
FPS = 30                                            # ゲームのFPS

# 線とか背景とかの色
COLOR_BLACK = (0, 0, 0)
COLOR_GRAY = (128, 128, 128)
COLOR_SILVER = (192, 192, 192)
COLOR_WHITE = (255, 255, 255)

# パレットの色(そのうち設定ファイルとかから取得するようになるかも？)
PALETTE = {
    "black" : (0, 0, 0), "navy" : (0, 0, 128), "blue" : (0, 0, 255),
    "green" : (0, 128, 0), "teal" : (0, 128, 128), "lime" : (0, 255, 0),
    "aqua" : (0, 255, 255), "maroon" : (128, 0, 0), "purple" : (128, 0, 128),
    "olive" : (128, 128, 0), "gray" : (128, 128, 128), "silver" : (192, 192, 192),
    "red" : (255, 0, 0), "fuchsia" : (255, 0, 255), "yellow" : (255, 255, 0),
    "white" : (255, 255, 255)}

class SubScreen():
    """ サブスクリーン """
    def __init__(self, name, rect, level=0):
        self.name = name                            # サブスクリーンの画面名
        self.rect = rect                            # サブスクリーンのrect
        self.screen = pygame.Surface(rect.size)     # サブスクリーンのSurfaceオブジェクト
        self.screenlevel = level                    # サブスクリーンの重なる順番
                                                    #   小さいほど下になる
        self.visible = True                         # サブスクリーンを表示するか？
        self.lock = False                           # サブスクリーンをロックするか？
    def update(self):
        """ サブスクリーンの更新 """
    def draw(self, screen):
        """ サブスクリーンの描画 """
        self.screen.fill(COLOR_WHITE)
        pygame.draw.rect(self.screen, COLOR_BLACK, (0, 0, self.rect.width, self.rect.height), 6)
        screen.blit(self.screen, self.rect)

class SubScreenGroup():
    """ サブスクリーンクラスをまとめて管理する """
    def __init__(self):
        self.sub_screens = []

    def append(self, subscreen):
        """ サブスクリーンオブジェクトを追加 """
        self.sub_screens.append(subscreen)

    def update(self):
        """ まとめて更新 """
        for subscreen in self.sub_screens:
            # 表示中かつロックされていない画面のみ更新
            if subscreen.visible and not subscreen.lock:
                subscreen.update()

    def draw(self, screen):
        """ まとめて描画 """
        for subscreen in self.sub_screens:
            # 表示中の画面のみ描画
            if subscreen.visible:
                subscreen.draw(screen)

class MsgScreen(SubScreen):
    """ メッセージの画面（デバック用？） """
    def __init__(self, name, rect):
        super().__init__(name, rect)
        self.font = pygame.font.SysFont(None, 30)
    def draw(self, screen):
        """ 画像全体の描画 """
        self.screen.fill(COLOR_WHITE)
        pygame.draw.rect(self.screen, COLOR_BLACK, (0, 0, self.rect.width, self.rect.height), 6)
        # マウスの位置を表示
        msg = 'mouse pos(x, y):%s, %s' % pygame.mouse.get_pos()
        self.screen.blit(self.font.render(msg, True, COLOR_BLACK), (5, 5))


        screen.blit(self.screen, self.rect)

def main():
    """ メイン処理 """
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_RECT.size)
    pygame.display.set_caption("dotedit")
    clock = pygame.time.Clock()

    # サブスクリーングループ
    subscreengroup = SubScreenGroup()
    # サブスクリーンを生成しグループに追加
    subscreengroup.append(SubScreen("MenuBar", Rect(5, 5, WINDOW_RECT.width - 10, 50)))
    subscreengroup.append(SubScreen("EditScreen", Rect(5, 60, 486, 486)))
    subscreengroup.append(SubScreen("PalettScreen", Rect(5, 551, 486, 75)))
    subscreengroup.append(SubScreen("ViewScreen", Rect(496, 60, 486, 486)))
    subscreengroup.append(MsgScreen("MsgScreen", Rect(496, 551, 486, 75)))

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit(0)

        subscreengroup.update()

        screen.fill(COLOR_SILVER)

        subscreengroup.draw(screen)

        pygame.display.update()
        clock.tick(FPS)


if __name__ == '__main__':
    main()
