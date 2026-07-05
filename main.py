import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont
from ui_main import TextAnalyzer

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("TextAnalyzer")
    app.setApplicationVersion("1.0")
    app.setFont(QFont("Segoe UI", 10))
    window = TextAnalyzer()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()