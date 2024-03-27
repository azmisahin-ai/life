# src/programlet/app.py
"""
Bu yazılım projesi, etkileşimli bir sistem oluşturan bir ana program ve ona bağlı programlara dayanmaktadır.

Programcıklar, adaptasyon ve evrim gibi süreçleri simüle eden bir yapıda,
belirli koşullara göre çoğalacak, değişecek ve test edilecektir.

Bu proje,
yapay yaşam ve evrimsel algoritmaların bir kombinasyonunu kullanarak karmaşık sistemleri modellemeyi amaçlamaktadır.
"""

import sys
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget

from programlet import MainProgram


class Application(QMainWindow):
    """
    Veri Görselleştirme ve İzleme Arayüzü
    Sonuçları görselleştirmek ve sistem performansını izlemek için arayüz.
    """

    def __init__(self):
        super().__init__()

        self.app = MainProgram()

        self.setWindowTitle("Program Simulation")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.start_button = QPushButton("Start Simulation")
        self.start_button.clicked.connect(self.start_simulation)
        layout.addWidget(self.start_button)

        # ...
        self.test_button = QPushButton("Start Test")
        self.test_button.clicked.connect(self.start_test)
        layout.addWidget(self.test_button)

        self.central_widget = QWidget()
        self.central_widget.setLayout(layout)
        self.setCentralWidget(self.central_widget)

        # app
        self.app = MainProgram()

    def start_simulation(self):
        # Görselleştirme
        fitness_history = self.app.start_simulation()
        plt.plot(fitness_history)
        plt.xlabel("Iterations")
        plt.ylabel("Average Fitness")
        plt.title("Fitness Progression")
        plt.show()

    def start_test(self):
        # Görselleştirme
        fitness_history = self.app.start_test()
        plt.plot(fitness_history)
        plt.xlabel("Iterations")
        plt.ylabel("Average Fitness")
        plt.title("Fitness Progression")
        plt.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Application()
    window.show()
    sys.exit(app.exec_())
