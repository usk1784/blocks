#!/usr/bin/env python3
#coding: utf-8
""" dotedit.py """
import sys
import pygame
from pygame.locals import *

WINDOW_RECT = Rect(0, 0, 987, 631)                  # ウィンドウのサイズ
FPS = 30                                            # ゲームのFPS

# ユーザーイベント
USEREVENT_MENU = pygame.USEREVENT

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

class SubScreen:
    """ サブスクリーン\n
    サブスクリーンの基本クラス """
    def __init__(self, name, rect):
        self.name = name                            # サブスクリーンの画面名
        self.rect = rect                            # サブスクリーンのrect
        self.screen = pygame.Surface(rect.size)     # サブスクリーンのSurfaceオブジェクト
        self.screenlevel = 0                        # サブスクリーンの重なる順番
                                                    #   小さいほど下になる
        self.visible = True                         # サブスクリーンを表示するか？
        self.lock = False                           # サブスクリーンをロックするか？
    def update(self):
        """ サブスクリーンの更新 """
    def mouse_button_down(self, pos, button):
        """ ボタンが押されたときの処理 """
    def mouse_motion(self, pos, ref, buttons):
        """ マウスが移動したときの処理 """
    def draw(self, screen):
        """ サブスクリーンの描画 """
        self.screen.fill(COLOR_WHITE)
        pygame.draw.rect(self.screen, COLOR_BLACK, (0, 0, self.rect.width, self.rect.height), 6)
        screen.blit(self.screen, self.rect)

class SubScreenGroup:
    """ サブスクリーンクラスをまとめて管理する """
    def __init__(self):
        self.sub_screens = []               # サブスクリーンをリストで管理

    def append(self, subscreen):
        """ サブスクリーンオブジェクトを追加 """
        self.sub_screens.append(subscreen)

    def get_subscreen(self, name):
        """ サブスクリーンの取得 """
        for subscreen in self.sub_screens:
            if subscreen.name == name:
                return subscreen
        return None

    def get_subscreen_in_pos(self, pos):
        """ posが指しているサブスクリーンの取得\n
        サブスクリーンの名前とサブスクリーン上のposを返す\n
        サブスクリーンが無いときはNone（文字）を返す """
        for subscreen in self.sub_screens:
            if subscreen.rect.collidepoint(pos):
                # サブスクリーン上のposを計算
                sposx = pos[0] - subscreen.rect.x
                sposy = pos[1] - subscreen.rect.y
                return subscreen.name, sposx, sposy
        return "None", 0, 0

    def update(self):
        """ まとめて更新 """
        for subscreen in self.sub_screens:
            # 表示中かつロックされていない画面のみ更新
            if subscreen.visible and not subscreen.lock:
                subscreen.update()

    def event_handler(self, event):
        """ イベントハンドラー\n
        各サブスクリーンのイベント処理を実行する """
        # マウスがクリックされた時
        if event.type == MOUSEBUTTONDOWN:
            # クリックされたサブスクリーン名を取得
            name, posx, posy = self.get_subscreen_in_pos(event.pos)
            for subscreen in self.sub_screens:
                # 表示中かつロックされていない時だけ処理
                if subscreen.name == name and subscreen.visible and not subscreen.lock:
                    subscreen.mouse_button_down((posx, posy), event.button)
        # マウスが移動
        elif event.type == MOUSEMOTION:
            # クリックされたサブスクリーン名を取得
            name, posx, posy = self.get_subscreen_in_pos(event.pos)
            for subscreen in self.sub_screens:
                # 表示中かつロックされていない時だけ処理
                if subscreen.name == name and subscreen.visible and not subscreen.lock:
                    subscreen.mouse_motion((posx, posy), event.rel, event.buttons)
        # メニューバーの項目が押された時
        elif event.type == USEREVENT_MENU:
            if event.menu_type == "menu_clear":
                self.get_subscreen("EditScreen").cell_clear()


    def draw(self, screen):
        """ まとめて描画 """
        for subscreen in self.sub_screens:
            # 表示中の画面のみ描画
            if subscreen.visible:
                subscreen.draw(screen)

class MenuBar(SubScreen):
    """ メニューバー """
    def __init__(self, name, rect):
        super().__init__(name, rect)
        self.font = pygame.font.SysFont(None, 20)
        self.celheight = 40                             # 1個のセルのサイズ
        self.celwidth = 50                              # 1個のセルのサイズ
        self.cells = []                                 # メニュー項目のリスト
                                                        #  (name, rect)
        # メニュー項目の追加
        cellrect = Rect(5, 5, self.celwidth, self.celheight)        # セーブボタン
        self.cells.append(("save", cellrect))
        cellrect = Rect(57, 5, self.celwidth, self.celheight)       # ロードボタン
        self.cells.append(("load", cellrect))
        cellrect = Rect(109, 5, self.celwidth, self.celheight)      # ロードボタン
        self.cells.append(("clear", cellrect))

    def mouse_button_down(self, pos, button):
        """ ボタンが押されたときの処理 """
        if button == BUTTON_LEFT:
            # ボタンが押された項目のイベントを発行
            for cell in self.cells:
                if cell[1].collidepoint(pos):
                    if cell[0] in ["save", "load", "clear"]:
                        userevent = pygame.event.Event(USEREVENT_MENU,
                                                       {"menu_type": "menu_" + cell[0]})
                        pygame.event.post(userevent)

    def draw(self, screen):
        """ メニューバーの描画 """
        self.screen.fill(COLOR_GRAY)
        # メニュー項目の描画
        for cell in self.cells:
            pygame.draw.rect(self.screen, COLOR_SILVER, cell[1])            # セルの色
            self.screen.blit(self.font.render(cell[0], True, COLOR_BLACK),  # 項目名
                             (cell[1].left + 5, 10))
            # マウスカーソルが項目上にある場合は、枠を描画する
            posx, posy = pygame.mouse.get_pos()
            if cell[1].collidepoint((posx - self.rect.left, posy - self.rect.top)):
                pygame.draw.rect(self.screen, COLOR_BLACK, cell[1], 3)          # セルの枠
        # メニューバーの枠
        pygame.draw.rect(self.screen, COLOR_BLACK,
                         (0, 0, self.rect.width, self.rect.height), 5)
        # メニューバーをメイン画面に描画
        screen.blit(self.screen, self.rect)

class EditScreen(SubScreen):
    """ エディタ部の画面 """
    def __init__(self, name, rect):
        super().__init__(name, rect)
        self.editcelx = 32              # 32 x 32 のドット絵を書く
        self.editcely = 32
        self.celsize = 15               # 1個のセルのサイズ
        self.drawcol1 = COLOR_BLACK     # クリックした場所に塗る色１
        self.drawcol2 = COLOR_WHITE     # クリックした場所に塗る色２
        self.cells = []                 # １ドット情報のリスト
                                        # １ドットは (color, rect)
        # 全セルのRectと色（白）を設定
        self.cell_clear()

        self.rect = rect
        self.rect.size = (self.editcelx * self.celsize + 6, self.editcely * self.celsize + 6)
        self.screen = pygame.Surface(self.rect.size)

    def mouse_button_down(self, pos, button):
        """ ボタンが押されたときの処理 """
        for cell in self.cells:
            # ボタンが押されたセルの色を変更
            if cell[1].collidepoint(pos):
                if button == BUTTON_LEFT:
                    cell[0] = self.drawcol1
                elif button == BUTTON_RIGHT:
                    cell[0] = self.drawcol2

    def mouse_motion(self, pos, ref, buttons):
        """ マウスが移動したときの処理 """
        for cell in self.cells:
            # ボタンが押されたセルの色を変更
            if cell[1].collidepoint(pos):
                if buttons[0]:
                    cell[0] = self.drawcol1
                elif buttons[2]:
                    cell[0] = self.drawcol2

    def draw(self, screen):
        """ エディタ部の描画 """
        self.screen.fill(COLOR_BLACK)

        # セルの描画
        for cell in self.cells:
            pygame.draw.rect(self.screen, cell[0], cell[1])                 # セルの色
            pygame.draw.rect(self.screen, COLOR_GRAY, cell[1], 1)           # セルの枠
        # 真ん中に線を引く
        pygame.draw.line(self.screen, COLOR_BLACK, (self.rect.centerx - self.rect.left, 0),
                         (self.rect.centerx - self.rect.left, self.rect.bottom), 2)
        pygame.draw.line(self.screen, COLOR_BLACK, (0, self.rect.centery - self.rect.top),
                         (self.rect.width, self.rect.centery - self.rect.top), 2)

        # エディタ部をメイン画面に描画
        screen.blit(self.screen, self.rect)

    def cell_clear(self):
        """ 全セルのクリア """
        self.cells.clear()
        # 全セルのRectと色（白）を設定
        for i in range(self.editcelx):
            for j in range(self.editcely):
                cellrect = Rect(i * self.celsize +3, j * self.celsize + 3,
                                self.celsize, self.celsize)
                self.cells.append([COLOR_WHITE, cellrect])


class MsgScreen(SubScreen):
    """ メッセージの画面（デバック用？） """
    def __init__(self, name, rect):
        super().__init__(name, rect)
        self.font = pygame.font.SysFont(None, 30)
        self.msgs = []
    def draw(self, screen):
        """ メッセージ画面の描画 """
        self.screen.fill(COLOR_WHITE)
        pygame.draw.rect(self.screen, COLOR_BLACK, (0, 0, self.rect.width, self.rect.height), 6)
        #メッセージの表示
        for i, msg in enumerate(self.msgs):
            self.screen.blit(self.font.render(msg, True, COLOR_BLACK), (5, i * 20 + 5))

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
    subscreengroup.append(MenuBar("MenuBar", Rect(5, 5, WINDOW_RECT.width - 10, 50)))
    subscreengroup.append(EditScreen("EditScreen", Rect(5, 60, 486, 486)))
    subscreengroup.append(SubScreen("PalettScreen", Rect(5, 551, 486, 75)))
    subscreengroup.append(SubScreen("ViewScreen", Rect(496, 60, 486, 486)))
    msgscreen = MsgScreen("MsgScreen", Rect(496, 551, 486, 75))     # デバッグ用画面
    subscreengroup.append(msgscreen)
#    msgscreen.visible = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit(0)
            else:
                # イベント処理
                subscreengroup.event_handler(event)

        # サブ画面の更新
        subscreengroup.update()

        # デバック情報の表示設定
        if msgscreen.visible:
            msgscreen.msgs.clear()
            msgscreen.msgs.append('mouse pos(x, y):%s, %s' % pygame.mouse.get_pos())
            msgscreen.msgs.append('%s pos(x, y):%s, %s' % \
                                  subscreengroup.get_subscreen_in_pos(pygame.mouse.get_pos()))

        screen.fill(COLOR_SILVER)

        # サブ画面の描画
        subscreengroup.draw(screen)

        pygame.display.update()
        clock.tick(FPS)


if __name__ == '__main__':
    main()
