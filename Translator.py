import sys
import os
from PyQt5.QtWidgets import (QApplication, QWidget, QTextEdit, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QComboBox)
from PyQt5.QtCore import Qt, QTimer, QPoint
from googletrans import Translator

class GoogleTranslateUI(QWidget):
    def __init__(self):
        super().__init__()

        # 翻訳器の初期化
        self.translator = Translator()

        # タイマーの設定
        self.timer = QTimer(self)
        self.timer.setInterval(500)  # 0.5秒後に翻訳を実行
        self.timer.timeout.connect(self.translateText)

        # ウィジェットの設定
        self.initUI()

        # ウィンドウの位置を読み込む
        self.loadWindowPosition()

    def initUI(self):
        self.setWindowTitle('Google Translate風 翻訳アプリ')
        self.setGeometry(100, 100, 1000, 500)

        # スタイルシートの適用
        self.setStyleSheet("""
            QWidget {
                background-color: #f5f5f5;
            }
            QTextEdit {
                font-size: 16px;
                padding: 10px;
                border: 1px solid #dfe1e5;
                border-radius: 5px;
                background-color: white;
            }
            QPushButton {
                font-size: 18px;
                padding: 10px 20px;
                background-color: #1a73e8;
                color: white;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #1558b0;
            }
            QComboBox {
                font-size: 16px;
                padding: 5px;
                border: 1px solid #dfe1e5;
                border-radius: 5px;
                background-color: white;
            }
        """)

        # 翻訳元と翻訳先の言語を選択するドロップダウンメニュー
        self.fromLanguage = QComboBox(self)
        self.fromLanguage.addItem("自動検出", 'auto')
        self.fromLanguage.addItem("英語", 'en')
        self.fromLanguage.addItem("日本語", 'ja')

        self.toLanguage = QComboBox(self)
        self.toLanguage.addItem("日本語", 'ja')
        self.toLanguage.addItem("英語", 'en')

        # 翻訳元のテキスト入力エリア
        self.inputText = QTextEdit(self)
        self.inputText.setPlaceholderText("ここに翻訳したいテキストを入力してください")
        self.inputText.textChanged.connect(self.startTranslation)

        # 翻訳結果の表示エリア
        self.outputText = QTextEdit(self)
        self.outputText.setReadOnly(True)
        self.outputText.setPlaceholderText("ここに翻訳結果が表示されます")

        # コピーボタン
        self.copyButton = QPushButton("コピー", self)
        self.copyButton.clicked.connect(self.copyText)
        self.copyButton.setVisible(False)  # 初期は非表示

        # レイアウト設定
        layout = QVBoxLayout()
        topLayout = QHBoxLayout()
        topLayout.addWidget(QLabel("翻訳元:"))
        topLayout.addWidget(self.fromLanguage)
        topLayout.addWidget(QLabel("翻訳先:"))
        topLayout.addWidget(self.toLanguage)

        layout.addLayout(topLayout)
        layout.addWidget(self.inputText)
        layout.addWidget(self.outputText)
        layout.addWidget(self.copyButton, alignment=Qt.AlignRight)

        self.setLayout(layout)

    def loadWindowPosition(self):
        # 位置を保存しているファイルを読み込む
        position_file = "window_position.txt"
        if os.path.exists(position_file):
            with open(position_file, "r") as f:
                x, y = map(int, f.readline().strip().split(","))
                self.move(QPoint(x, y))

    def saveWindowPosition(self):
        # 現在のウィンドウの位置をファイルに保存する
        position_file = "window_position.txt"
        with open(position_file, "w") as f:
            f.write(f"{self.x()},{self.y()}")

    def closeEvent(self, event):
        self.saveWindowPosition()  # ウィンドウが閉じられる前に位置を保存
        event.accept()

    def startTranslation(self):
        # タイマーをスタート（入力があった場合）
        self.timer.start()

    def translateText(self):
        # タイマーを停止
        self.timer.stop()

        # 入力されたテキストを取得
        text = self.inputText.toPlainText()
        if not text:
            self.outputText.clear()
            self.copyButton.setVisible(False)
            return

        # 翻訳元と翻訳先の言語を取得
        from_lang = self.fromLanguage.currentData()
        to_lang = self.toLanguage.currentData()

        try:
            # 翻訳を実行
            result = self.translator.translate(text, src=from_lang, dest=to_lang)
            self.outputText.setText(result.text)

            # コピーボタンを表示
            self.copyButton.setVisible(True)
        except Exception as e:
            self.outputText.setText(f"エラーが発生しました: {e}")
            self.copyButton.setVisible(False)

    def copyText(self):
        # 翻訳結果をクリップボードにコピー
        clipboard = QApplication.clipboard()
        clipboard.setText(self.outputText.toPlainText())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GoogleTranslateUI()
    window.show()
    sys.exit(app.exec_())
