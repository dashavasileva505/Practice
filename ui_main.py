import sys
import re
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QShortcut
from PyQt5.QtGui import QKeySequence
from PIL import Image


class TextAnalyzer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Текстовый анализатор")
        self.setMinimumSize(800, 550)
        self.setStyleSheet("background-color: #FFF7E6;")
        self._create_ui()
        self._connect_signals()
        self._setup_shortcuts()

    def _create_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)

        left_widget = QWidget()
        left_layout = QVBoxLayout()
        left_widget.setLayout(left_layout)

        label = QLabel("Введите текст для анализа:")
        label.setFont(QFont("Segoe UI", 11))
        left_layout.addWidget(label)

        self.text_input = QTextEdit()
        self.text_input.setStyleSheet("background-color: #A8B58A;")
        self.text_input.setPlaceholderText("Вставьте сюда любой текст...")
        self.text_input.setMinimumHeight(150)
        left_layout.addWidget(self.text_input)

        self.analyze_button = QPushButton("Анализировать")
        self.analyze_button.setStyleSheet("""
            QPushButton {
                background-color: #F7C8D3;
                color: white;
                border-radius: 8px;
                padding: 8px;
            }
        """)
        self.analyze_button.setFont(QFont("Segoe UI", 10))
        left_layout.addWidget(self.analyze_button)

        group = QGroupBox("Результаты")
        group_layout = QVBoxLayout()

        self.words_label = QLabel("Слова: 0")
        self.chars_label = QLabel("Буквы: 0")
        self.sentences_label = QLabel("Предложения: 0")
        self.density_label = QLabel("Плотность: 0")

        for lbl in [self.words_label, self.chars_label, self.sentences_label, self.density_label]:
            lbl.setFont(QFont("Segoe UI", 10))
            group_layout.addWidget(lbl)

        group.setLayout(group_layout)
        left_layout.addWidget(group)
        left_layout.addStretch()

        right_widget = QWidget()
        right_layout = QVBoxLayout()
        right_widget.setLayout(right_layout)

        self.image_label = QLabel("Обложка книги")
        self.image_label.setStyleSheet("""
            background-color: #ffff99;
            border: 2px dashed #331a00;
            border-radius: 8px;
        """)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumHeight(200)
        self.image_label.setStyleSheet("""
            background-color: #f5f5f5;
            border: 2px dashed #aaaaaa;
            border-radius: 8px;
        """)
        right_layout.addWidget(self.image_label)

        self.load_image_button = QPushButton("Загрузить обложку")
        self.load_image_button.setStyleSheet("""
            QPushButton {
                background-color: #A8B58A;
                color: white;
                border-radius: 8px;
                padding: 8px;
            }
        """)
        right_layout.addWidget(self.load_image_button)

        self.export_button = QPushButton("Экспорт в CSV")
        self.export_button.setStyleSheet("""
            QPushButton {
                background-color: #331a00;
                color: white;
                border-radius: 8px;
                padding: 8px;
            }
        """)
        right_layout.addWidget(self.export_button)

        right_layout.addStretch()

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setSizes([450, 300])
        main_layout.addWidget(splitter)

    def _connect_signals(self):
        self.analyze_button.clicked.connect(self._analyze_text)
        self.load_image_button.clicked.connect(self._load_image)
        self.export_button.clicked.connect(self._export_csv)

    def _analyze_text(self):
        text = self.text_input.toPlainText()
        if not text.strip():
            QMessageBox.information(self, "Нет текста", "Введите текст для анализа.")
            return

        words = len(re.findall(r'\b\w+\b', text))
        chars = len(re.findall(r'[а-яА-Яa-zA-Z]', text))
        sentences = len(re.split(r'[.!?]+', text)) - 1
        density = round(words / chars, 3) if chars > 0 else 0

        self.words_label.setText(f"Слова: {words}")
        self.chars_label.setText(f"Буквы: {chars}")
        self.sentences_label.setText(f"Предложения: {sentences}")
        self.density_label.setText(f"Плотность: {density}")

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self,
            "Выход",
            "Вы уверены, что хотите выйти?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def _load_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите изображение",
            "",
            "Изображения (*.png *.jpg *.jpeg *.bmp)"
        )
        if not file_path:
            return
        try:
            image = Image.open(file_path).convert("RGBA")
            image.thumbnail((250, 250), Image.LANCZOS)
            qimage = QImage(image.tobytes(), image.width, image.height, QImage.Format_RGBA8888)
            pixmap = QPixmap.fromImage(qimage)
            self.image_label.setPixmap(pixmap)
            self.image_label.setStyleSheet("background-color: transparent; border: none;")
        except Exception as error:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить изображение:\n{error}")

    def _export_csv(self):
        import csv
        from datetime import datetime

        text = self.text_input.toPlainText()
        if not text.strip():
            QMessageBox.warning(self, "Нет текста", "Сначала введите текст и выполните анализ.")
            return

        words = self.words_label.text()
        chars = self.chars_label.text()
        sentences = self.sentences_label.text()
        density = self.density_label.text()

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Сохранить CSV",
            f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            "CSV files (*.csv)"
        )

        if not file_path:
            return

        try:
            with open(file_path, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                writer.writerow(["Параметр", "Значение"])
                writer.writerow(["Слова", words.split(":")[1].strip()])
                writer.writerow(["Буквы", chars.split(":")[1].strip()])
                writer.writerow(["Предложения", sentences.split(":")[1].strip()])
                writer.writerow(["Плотность", density.split(":")[1].strip()])
                writer.writerow(["Текст", text[:100] + "..." if len(text) > 100 else text])

            QMessageBox.information(self, "Успех", f"Результаты сохранены в {file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить: {e}")

    def _setup_shortcuts(self):
        shortcut_analyze = QShortcut(QKeySequence("Ctrl+Return"), self)
        shortcut_analyze.activated.connect(self._analyze_text)
        shortcut_analyze.setContext(Qt.ApplicationShortcut)

        shortcut_analyze2 = QShortcut(QKeySequence("Ctrl+Enter"), self)
        shortcut_analyze2.activated.connect(self._analyze_text)
        shortcut_analyze2.setContext(Qt.ApplicationShortcut)