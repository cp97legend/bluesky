import pygame as pg

dark_bg = (16, 22, 38, 230)
panel_bg = (28, 40, 65, 235)
panel_active = (49, 108, 191, 245)
panel_hover = (61, 78, 118, 245)
border = (175, 207, 255)
muted = (198, 214, 238)
white = (245, 248, 255)


class Menu:
    """
    Modernised pygame control menu with Chinese labels.
    """

    PAGES = [
        (
            "运行",
            [
                ("开始运行", "OP"),
                ("暂停", "HOLD"),
                ("快速前进", "FF"),
                ("快进 10 秒", "FF 0:0:10"),
                ("打开场景", "IC"),
                ("重新加载上次场景", "IC IC"),
                ("录制功能开发中", "ECHO 录制功能仍在开发中"),
                ("退出程序", "QUIT"),
            ],
        ),
        (
            "显示",
            [
                ("放大", "+"),
                ("缩小", "-"),
                ("向左平移", "PAN LEFT"),
                ("向右平移", "PAN RIGHT"),
                ("向上平移", "PAN UP"),
                ("向下平移", "PAN DOWN"),
                ("跳转到位置", "PAN;INSEDIT PAN "),
                ("航路点", "SWRAD WPT"),
                ("机场", "SWRAD APT"),
                ("卫星底图", "SWRAD SAT"),
                ("标签", "SWRAD LABEL"),
            ],
        ),
        (
            "交通",
            [
                ("创建飞机", "CRE;INSEDIT CRE "),
                ("高度", "ALT;INSEDIT ALT "),
                ("航向", "HDG;INSEDIT HDG "),
                ("速度", "SPD;INSEDIT SPD "),
                ("垂直速度", "V/S;INSEDIT VS "),
                ("目的地", "DEST;INSEDIT DEST "),
                ("冲突解脱", "ASAS;INSEDIT ASAS "),
                ("LNAV", "LNAV;INSEDIT LNAV "),
                ("VNAV", "VNAV;INSEDIT VNAV "),
            ],
        ),
        (
            "更多",
            [
                ("自定义 1", "ECHO <自定义 1>"),
                ("自定义 2", "ECHO <自定义 2>"),
                ("自定义 3", "ECHO <自定义 3>"),
                ("自定义 4", "ECHO <自定义 4>"),
                ("自定义 5", "ECHO <自定义 5>"),
                ("自定义 6", "ECHO <自定义 6>"),
                ("自定义 7", "ECHO <自定义 7>"),
                ("自定义 8", "ECHO <自定义 8>"),
            ],
        ),
    ]

    def __init__(self, win, x, y):
        self.win = win
        self.x = x
        self.y = y
        self.ipage = 0
        self.page_rects = []
        self.button_rects = []
        self.surface = None

        self.title_font = self._make_font(["Microsoft YaHei UI", "Microsoft YaHei", "SimHei", "Arial"], 22, True)
        self.page_font = self._make_font(["Microsoft YaHei UI", "Microsoft YaHei", "SimHei", "Arial"], 16, True)
        self.button_font = self._make_font(["Microsoft YaHei UI", "Microsoft YaHei", "SimHei", "Arial"], 15, False)
        self.small_font = self._make_font(["Microsoft YaHei UI", "Microsoft YaHei", "SimHei", "Arial"], 13, False)

        self.dx = 336
        self.dy = 292
        self.rect = pg.Rect(self.x, self.y, self.dx, self.dy)

    def _make_font(self, names, size, bold=False):
        for name in names:
            fontpath = pg.font.match_font(name)
            if fontpath:
                return pg.font.Font(fontpath, size)
        return pg.font.SysFont(None, size, bold=bold)

    def update(self):
        self.rect = pg.Rect(self.x, self.y, self.dx, self.dy)
        self.surface = pg.Surface((self.dx, self.dy), pg.SRCALPHA)
        self.surface.fill((0, 0, 0, 0))

        pg.draw.rect(self.surface, dark_bg, self.surface.get_rect(), border_radius=18)
        pg.draw.rect(self.surface, border, self.surface.get_rect(), width=1, border_radius=18)

        left_panel = pg.Rect(12, 12, 92, self.dy - 24)
        right_panel = pg.Rect(112, 12, self.dx - 124, self.dy - 24)

        pg.draw.rect(self.surface, panel_bg, left_panel, border_radius=14)
        pg.draw.rect(self.surface, panel_bg, right_panel, border_radius=14)

        title = self.title_font.render("控制面板", True, white)
        self.surface.blit(title, (26, 22))
        subtitle = self.small_font.render("点击按钮即可执行常用命令", True, muted)
        self.surface.blit(subtitle, (126, 24))

        self.page_rects = []
        top = 64
        for idx, (label, _) in enumerate(self.PAGES):
            rect = pg.Rect(20, top + idx * 48, 76, 38)
            color = panel_active if idx == self.ipage else panel_hover
            pg.draw.rect(self.surface, color, rect, border_radius=12)
            pg.draw.rect(self.surface, border, rect, width=1, border_radius=12)
            text = self.page_font.render(label, True, white)
            text_rect = text.get_rect(center=rect.center)
            self.surface.blit(text, text_rect)
            self.page_rects.append(rect)

        self.button_rects = []
        _, items = self.PAGES[self.ipage]
        grid_top = 58
        btn_w = 96
        btn_h = 34
        gap_x = 12
        gap_y = 10
        cols = 2

        for idx, (label, command) in enumerate(items):
            row = idx // cols
            col = idx % cols
            rect = pg.Rect(126 + col * (btn_w + gap_x), grid_top + row * (btn_h + gap_y), btn_w, btn_h)
            pg.draw.rect(self.surface, panel_hover, rect, border_radius=10)
            pg.draw.rect(self.surface, border, rect, width=1, border_radius=10)
            text = self.button_font.render(label, True, white)
            text_rect = text.get_rect(center=rect.center)
            self.surface.blit(text, text_rect)
            self.button_rects.append((rect, command))

        hint = self.small_font.render("支持 Ctrl+V 粘贴命令，输入 EXIT 可退出", True, muted)
        self.surface.blit(hint, (126, self.dy - 30))
        return self.surface

    def getcmd(self, mpos):
        local_x = mpos[0] - self.x
        local_y = mpos[1] - self.y

        for idx, rect in enumerate(self.page_rects):
            if rect.collidepoint((local_x, local_y)):
                self.ipage = idx
                return ""

        for rect, command in self.button_rects:
            if rect.collidepoint((local_x, local_y)):
                return command

        return ""
