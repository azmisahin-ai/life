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
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QLabel,
    QLineEdit,
    QDoubleSpinBox,
)

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

        # Iterasyonlar için giriş kutusu
        self.iterations_label = QLabel("Iterations:")
        self.iterations_input = QLineEdit()
        layout.addWidget(self.iterations_label)
        layout.addWidget(self.iterations_input)

        # Programlet sayısı için kaydırıcı
        self.programlets_label = QLabel("Number of Programlets:")
        self.programlets_input = QLineEdit()
        layout.addWidget(self.programlets_label)
        layout.addWidget(self.programlets_input)

        # Mutasyon oranı için kaydırıcı
        self.mutation_rate_label = QLabel("Mutation Rate:")
        self.mutation_rate_input = QDoubleSpinBox()
        self.mutation_rate_input.setMinimum(0.0)
        self.mutation_rate_input.setMaximum(1.0)
        self.mutation_rate_input.setSingleStep(0.01)
        layout.addWidget(self.mutation_rate_label)
        layout.addWidget(self.mutation_rate_input)

        # Hedef fitness değeri için kaydırıcı
        self.target_fitness_label = QLabel("Target Fitness:")
        self.target_fitness_input = QDoubleSpinBox()
        self.target_fitness_input.setMinimum(0.0)
        self.target_fitness_input.setMaximum(1000.0)
        self.target_fitness_input.setSingleStep(0.1)
        layout.addWidget(self.target_fitness_label)
        layout.addWidget(self.target_fitness_input)

        # Start buttons
        self.start_simulation_button = QPushButton("Start Simulation")
        self.start_simulation_button.clicked.connect(self.start_simulation)
        layout.addWidget(self.start_simulation_button)

        self.start_test_button = QPushButton("Start Test")
        self.start_test_button.clicked.connect(self.start_test)
        layout.addWidget(self.start_test_button)

        self.central_widget = QWidget()
        self.central_widget.setLayout(layout)
        self.setCentralWidget(self.central_widget)

    def start_simulation(self):
        """
        # Simülasyon Fitness

        Bu, algoritmanın kendi içinde bir döngüde veya iterasyonda nasıl performans gösterdiğini ölçmek için kullanılır.
        Aalgoritmanın her bir iterasyonunda veya jenerasyonunda elde edilen fitness değerlerinin ortalamasıdır.
        Bu, algoritmanın zamanla nasıl geliştiğini veya değiştiğini görmek için kullanılır.
        """
        # Kullanıcının girdiği değerleri al
        iterations = int(self.iterations_input.text())
        num_programlets = int(self.programlets_input.text())
        mutation_rate = float(self.mutation_rate_input.value())
        target_fitness = float(self.target_fitness_input.value())

        # MainProgram instance'ı oluştururken kullanıcı girişlerini kullan
        self.app = MainProgram(
            iterations, num_programlets, mutation_rate, target_fitness
        )

        # Simülasyonu başlat
        fitness_history = self.app.start_simulation()
        plt.plot(fitness_history)
        plt.xlabel("Simulation Iterations")
        plt.ylabel("Average Simulation Fitness")
        plt.title("Fitness Simulation Progression")
        plt.show()

    def start_test(self):
        """
        # Test Fitness

        Bu, algoritmanın performansını ölçmek için kullanılır.
        Test fitness değeri, algoritmanın belirli bir görevi ne kadar iyi gerçekleştirebildiğini gösterir.

        """
        # Kullanıcının girdiği değerleri al
        iterations = int(self.iterations_input.text())
        num_programlets = int(self.programlets_input.text())
        mutation_rate = float(self.mutation_rate_input.value())
        target_fitness = float(self.target_fitness_input.value())

        # MainProgram instance'ı oluştururken kullanıcı girişlerini kullan
        self.app = MainProgram(
            iterations, num_programlets, mutation_rate, target_fitness
        )

        # Testi başlat
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
