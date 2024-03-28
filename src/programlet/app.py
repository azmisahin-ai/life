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
        self.iterations = 50
        self.num_programlets = 20
        self.mutation_rate = 0.1  # Başlangıç mutasyon oranı
        self.target_fitness = 1.0  # Hedef fitness değeri
        self.app = MainProgram(self.iterations, self.num_programlets, self.mutation_rate, self.target_fitness)

    def start_simulation(self):
        """
        Simülasyon Fitness Değeri:
        Bu, algoritmanın kendi içinde bir döngüde veya iterasyonda nasıl performans gösterdiğini ölçmek için kullanılır.
        Aalgoritmanın her bir iterasyonunda veya jenerasyonunda elde edilen fitness değerlerinin ortalamasıdır.
        Bu, algoritmanın zamanla nasıl geliştiğini veya değiştiğini görmek için kullanılır.
        """
        fitness_history = self.app.start_simulation()
        plt.plot(fitness_history)
        plt.xlabel("Simulation Iterations")
        plt.ylabel("Average Simulation Fitness")
        plt.title("Fitness Simulation Progression")
        plt.show()

    def start_test(self):
        """
        Test Fitness Değeri:
        Bu, algoritmanın performansını ölçmek için kullanılır.
        Test fitness değeri, algoritmanın belirli bir görevi ne kadar iyi gerçekleştirebildiğini gösterir.
        """
        fitness_history = self.app.start_test()
        plt.plot(fitness_history)
        plt.xlabel("Test Iterations")
        plt.ylabel("Average Test Fitness")
        plt.title("Fitness Test Progression")
        plt.show()


if __name__ == "__main__":
    application = QApplication(sys.argv)
    window = Application()
    window.show()
    sys.exit(application.exec_())
