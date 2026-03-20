""" Documentation window for the QTGL version of BlueSky."""
from PyQt6.QtCore import QUrl, QFileInfo
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLabel
try:
    from PyQt6.QtWebEngineWidgets import QWebEngineView as QWebView
    from PyQt6.QtWebEngineCore import QWebEnginePage as QWebPage


    class DocView(QWebView):
        def __init__(self, parent=None):
            super().__init__(parent)
            class DocPage(QWebPage):
                def acceptNavigationRequest(self, url, navtype, ismainframe):
                    if navtype == self.NavigationType.NavigationTypeLinkClicked:
                        if url.url()[:6].lower() == 'stack:':
                            stack(url.url()[6:].lower())
                            return False
                    return True
            self.docpage = DocPage()
            self.setPage(self.docpage)
except ImportError:
    DocView = None

import bluesky as bs
from bluesky.stack import stack


class DocWindow(QWidget):
    app = None

    def __init__(self, app):
        super().__init__()
        self.vlayout  = QVBoxLayout()
        self.backbtn = QPushButton('返回')
        self.closebtn = QPushButton('关闭')
        if DocView is not None:
            self.view = DocView()
            self.backbtn.clicked.connect(self.view.back)
        else:
            self.view = QLabel('BlueSky 无法初始化内置文档浏览器。\n' +
                '这通常意味着当前 Qt / WebEngine 安装不完整。\n' +
                '如果还没有安装，可以尝试执行：\n\n' +
                '    pip install PyQtWebEngine\n\n' +
                '或者使用你常用的 Python 包管理器安装相应组件。')
        self.vlayout.setContentsMargins(1, 1, 1, 1)
        self.vlayout.setSpacing(1)
        self.vlayout.addWidget(self.view)
        hlayout = QHBoxLayout()
        buttonbox = QWidget()
        buttonbox.setLayout(hlayout)
        self.vlayout.addWidget(buttonbox)
        hlayout.addWidget(self.closebtn)
        hlayout.addWidget(self.backbtn)
        self.closebtn.clicked.connect(self.hide)
        self.setLayout(self.vlayout)
        self.setWindowTitle('BlueSky 帮助文档')

    def show_cmd_doc(self, cmd):
        if not cmd:
            cmd = 'Command-Reference'
        if not isinstance(self.view, QLabel):
            fname = bs.resource(f'html/{cmd.lower()}.html').as_posix()
            self.view.load(QUrl.fromLocalFile(QFileInfo(fname).absoluteFilePath()))
