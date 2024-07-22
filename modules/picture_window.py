from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PySide6.QtCore import QSize


class ChartDisplayWindow(QWidget):
    def __init__(self, html, data):
        super().__init__()
        self.setWindowTitle("Chart Display")
        self.setMinimumSize(QSize(800, 600))
        self.html = html
        self.data = data

        self.setStyleSheet('''
            QWidget {
                background-color: rgb(40, 44, 52);
                color: rgb(221, 221, 221);
                font: 10pt "Arial";
            }
            QPushButton {
                background-color: rgb(52, 59, 72);
                border: 2px solid rgb(52, 59, 72);
                border-radius: 5px;
                padding: 5px;
                color: rgb(221, 221, 221);
            }
            QPushButton:hover {
                background-color: rgb(61, 70, 86);
                border: 2px solid rgb(61, 70, 86);
            }
            QPushButton:pressed {
                background-color: rgb(43, 50, 61);
                border: 2px solid rgb(43, 50, 61);
            }
        ''')

        main_layout = QVBoxLayout()
        button_layout = QHBoxLayout()

        self.webEngineView = QWebEngineView()
        main_layout.addWidget(self.webEngineView)

        # 调整 HTML 内容的颜色
        html1 = f'''
        <html>
        <head>
            <style>
                body {{
                    background-color: rgb(40, 44, 52);
                    color: rgb(221, 221, 221);
                }}
            </style>
        </head>
        </html>
        '''
        self.webEngineView.setHtml(html1)
        self.webEngineView.setHtml(self.html)

        self.export_data_button = QPushButton("导出股票数据")
        self.export_table_button = QPushButton("导出表格文件")

        button_layout.addWidget(self.export_data_button)
        button_layout.addWidget(self.export_table_button)

        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        self.export_data_button.clicked.connect(self.export_data)
        self.export_table_button.clicked.connect(self.export_table)

    def export_data(self):
        # todo 实现导出股票数据的逻辑
        print("导出股票数据")

    def export_table(self):
        # todo 实现导出表格文件的逻辑
        print("导出表格文件")
