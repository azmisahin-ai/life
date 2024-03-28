# src/programlet/app.py
"""
Bu yazılım projesi, etkileşimli bir sistem oluşturan bir ana program ve ona bağlı programlara dayanmaktadır.

Programcıklar, adaptasyon ve evrim gibi süreçleri simüle eden bir yapıda,
belirli koşullara göre çoğalacak, değişecek ve test edilecektir.

Bu proje,
yapay yaşam ve evrimsel algoritmaların bir kombinasyonunu kullanarak karmaşık sistemleri modellemeyi amaçlamaktadır.
"""

import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QGraphicsView,
    QGraphicsScene,
    QLabel,
    QLineEdit,
    QDoubleSpinBox,
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from programlet import MainProgram


class Application(QMainWindow):
    """
    Veri Görselleştirme ve İzleme Arayüzü
    Sonuçları görselleştirmek ve sistem performansını izlemek için arayüz.
    """

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Program Simulation")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        # Iterasyonlar için giriş kutusu
        self.iterations_label = QLabel("Iterations (e.g., 50):")
        self.iterations_input = QLineEdit()
        layout.addWidget(self.iterations_label)
        layout.addWidget(self.iterations_input)

        # Programlet sayısı için giriş kutusu
        self.programlets_label = QLabel("Number of Programlets (e.g., 20):")
        self.programlets_input = QLineEdit()
        layout.addWidget(self.programlets_label)
        layout.addWidget(self.programlets_input)

        # Mutasyon oranı için kaydırıcı
        self.mutation_rate_label = QLabel(
            "Mutation Rate (between 0.0 and 1.0)(e.g., 0.1):"
        )
        self.mutation_rate_input = QDoubleSpinBox()
        self.mutation_rate_input.setMinimum(0.0)
        self.mutation_rate_input.setMaximum(1.0)
        self.mutation_rate_input.setSingleStep(0.01)
        layout.addWidget(self.mutation_rate_label)
        layout.addWidget(self.mutation_rate_input)

        # Hedef fitness değeri için kaydırıcı
        self.target_fitness_label = QLabel("Target Fitness (e.g., 1.0)(e.g., 1.0:")
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

        self.graph_view = QGraphicsView()
        layout.addWidget(self.graph_view)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def start_simulation(self):
        iterations_text = self.iterations_input.text()
        programlets_text = self.programlets_input.text()

        # Giriş kutularının boş olup olmadığını kontrol et
        if not iterations_text or not programlets_text:
            print("Please enter both iterations and number of programlets.")
            return

        iterations = int(iterations_text)
        num_programlets = int(programlets_text)
        mutation_rate = float(self.mutation_rate_input.value())
        target_fitness = float(self.target_fitness_input.value())

        self.app = MainProgram(
            iterations, num_programlets, mutation_rate, target_fitness
        )

        fitness_history = self.app.start_simulation()
        self.plot_graph(
            fitness_history,
            "Simulation Iterations",
            "Average Simulation Fitness",
            "Fitness Simulation Progression",
        )

    def start_test(self):
        """
        # Test Fitness

        Bu, algoritmanın performansını ölçmek için kullanılır.
        Test fitness değeri, algoritmanın belirli bir görevi ne kadar iyi gerçekleştirebildiğini gösterir.

        """
        iterations_text = self.iterations_input.text()
        programlets_text = self.programlets_input.text()

        # Giriş kutularının boş olup olmadığını kontrol et
        if not iterations_text or not programlets_text:
            print("Please enter both iterations and number of programlets.")
            return

        iterations = int(iterations_text)
        num_programlets = int(programlets_text)
        mutation_rate = float(self.mutation_rate_input.value())
        target_fitness = float(self.target_fitness_input.value())

        self.app = MainProgram(
            iterations, num_programlets, mutation_rate, target_fitness
        )

        fitness_history = self.app.start_test()
        self.plot_graph(
            fitness_history,
            "Test Iterations",
            "Average Test Fitness",
            "Fitness Test Progression",
        )

    def plot_graph(self, data, x_label, y_label, title):
        scene = QGraphicsScene()
        scene.setSceneRect(0, 0, 800, 400)

        figure = Figure()
        canvas = FigureCanvas(figure)
        ax = figure.add_subplot(111)

        ax.plot(data)
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.set_title(title)

        scene.addWidget(canvas)
        self.graph_view.setScene(scene)


if __name__ == "__main__":
    application = QApplication(sys.argv)
    window = Application()
    window.show()
    sys.exit(application.exec_())
