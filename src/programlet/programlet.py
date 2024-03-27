# src/programlet/programlet.py
import random
import numpy as np


class TestModule:
    """
    Performansını test etmek ve istatistiksel analizleri
    """

    @staticmethod
    def run_test(programlets):
        # Rasgele bir test senaryosu oluştur
        test_scenario = [random.uniform(0, 1) for _ in range(len(programlets))]

        # Test senaryosunu kullanarak programletlerin performansını değerlendir
        total_fitness = sum(
            [p.fitness * test_scenario[i] for i, p in enumerate(programlets)]
        )
        average_fitness = total_fitness / len(programlets)

        return average_fitness


class Programlet:
    """
    Programletler kendilerini çoğaltma, değiştirme ve test etme yeteneklerini içerir.

    Özellikler:
    Eşleştirme ve Uyarlama Algoritmalarının
    """

    def __init__(self, fitness):
        self.fitness = fitness

    def mutate(self):
        """
        Programcıkların çoğalma ve adaptasyon süreçlerine uygun algoritmalar.
        """
        self.fitness += random.uniform(-0.1, 0.1)


class MainProgram:
    """
    Ana program,
    programcıkların çoğalmasını, istatistiksel analizleri, müdahale kabiliyetini ve test süreçlerini yönetir.
    """

    def start_simulation(self):
        num_programlets = 20
        iterations = 50
        programlets = [Programlet(random.random()) for _ in range(num_programlets)]
        fitness_history = []

        for i in range(iterations):
            new_programlets = []
            for j in range(num_programlets):
                partner_index = random.randint(0, num_programlets - 1)
                if j != partner_index:
                    avg_fitness = (
                        programlets[j].fitness + programlets[partner_index].fitness
                    ) / 2
                    new_programlet = Programlet(avg_fitness)
                    new_programlet.mutate()
                    new_programlets.append(new_programlet)

            # Programletlerin güncellenmesi
            programlets.extend(new_programlets)
            programlets.sort(key=lambda x: x.fitness, reverse=True)
            programlets = programlets[:num_programlets]

            # Fitness geçmişine değer ekleme
            avg_fitness = np.mean([p.fitness for p in programlets])
            fitness_history.append(avg_fitness)

        return fitness_history

    def start_test(self):
        num_programlets = 20
        programlets = [Programlet(random.random()) for _ in range(num_programlets)]
        fitness_history = []

        # Rasgele bir test senaryosu oluştur
        test_scenario = [random.uniform(0, 1) for _ in range(num_programlets)]

        for _ in range(50):  # Her bir test için 50 iterasyon yapalım
            for i in range(num_programlets):
                programlets[i].fitness *= test_scenario[i]

            # Fitness geçmişine değer ekleme
            avg_fitness = np.mean([p.fitness for p in programlets])
            fitness_history.append(avg_fitness)

        return fitness_history


if __name__ == "__main__":
    main = MainProgram()
    test_fitness_history = main.start_test()
    main_fitness_history = main.start_simulation()
    print("test_fitness_history", test_fitness_history)
    print("main_fitness_history", main_fitness_history)
