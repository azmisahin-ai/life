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

    def mutate(self, mutation_rate):
        """
        Programcıkların çoğalma ve adaptasyon süreçlerine uygun algoritmalar.
        """
        self.fitness += random.uniform(-mutation_rate, mutation_rate)


class MainProgram:
    """
    Ana program,
    programcıkların çoğalmasını, istatistiksel analizleri, müdahale kabiliyetini ve test süreçlerini yönetir.
    """

    def __init__(self):
        self.iterations = 50
        self.num_programlets = 20
        self.mutation_rate = 0.1  # Başlangıç mutasyon oranı
        self.target_fitness = 1.0  # Hedef fitness değeri

    def start_simulation(self):
        programlets = [Programlet(random.random()) for _ in range(self.num_programlets)]
        fitness_history = []
        mutation_rates = []

        for i in range(self.iterations):
            new_programlets = []
            for j in range(self.num_programlets):
                partner_index = random.randint(0, self.num_programlets - 1)
                if j != partner_index:
                    avg_fitness = (
                        programlets[j].fitness + programlets[partner_index].fitness
                    ) / 2
                    new_programlet = Programlet(avg_fitness)
                    new_programlet.mutate(self.mutation_rate)
                    new_programlets.append(new_programlet)

            # Programletlerin güncellenmesi
            programlets.extend(new_programlets)
            programlets.sort(key=lambda x: x.fitness, reverse=True)
            programlets = programlets[: self.num_programlets]

            # Fitness geçmişine değer ekleme
            avg_fitness = np.mean([p.fitness for p in programlets])
            fitness_history.append(avg_fitness)

            # Mutasyon oranlarını izleme
            mutation_rates.append(self.mutation_rate)

            # Mutasyon oranını güncelleme
            self.update_mutation_rate(avg_fitness)

        return fitness_history, mutation_rates

    def update_mutation_rate(self, avg_fitness):
        # Eğer ortalama fitness artarsa, mutasyon oranını azaltmak için bir faktör uygula
        if avg_fitness > self.target_fitness:
            self.mutation_rate *= (
                0.9  # Örneğin, mevcut mutasyon oranını %10 azaltabiliriz
            )
        # Eğer ortalama fitness düşerse, mutasyon oranını artırmak için bir faktör uygula
        else:
            self.mutation_rate *= (
                1.1  # Örneğin, mevcut mutasyon oranını %10 artırabiliriz
            )

    def start_test(self):
        programlets = [Programlet(random.random()) for _ in range(self.num_programlets)]
        fitness_history = []

        # Rasgele bir test senaryosu oluştur
        test_scenario = [random.uniform(0, 1) for _ in range(self.num_programlets)]

        for _ in range(50):  # Her bir test için 50 iterasyon yapalım
            for i in range(self.num_programlets):
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
