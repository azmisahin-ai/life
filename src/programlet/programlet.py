# src/programlet/programlet.py
import random
import numpy as np


class TestModule:
    """
    Programletlerin performansını test etmek ve istatistiksel analizler yapmak için kullanılır.
    """

    @staticmethod
    def run_test(programlets):
        """
        Verilen programletler listesini kullanarak bir test senaryosu oluşturur
        ve her bir programletin performansını değerlendirir.

        Args:
            programlets (list): Test edilecek programletlerin listesi.

        Returns:
            float: Ortalama performans.
        """
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
    - Fitness: Programletin performansını ölçen bir sayı.
    """

    def __init__(self, fitness):
        """
        Yeni bir programlet oluşturur.

        Args:
            fitness (float): Programletin başlangıç fitness değeri.
        """
        self.fitness = fitness

    def mutate(self, mutation_rate):
        """
        Programletin fitness değerini mutasyona uğratır.

        Args:
            mutation_rate (float): Mutasyon oranı. Fitness değerini değiştirecek olan aralık.
        """
        self.fitness += random.uniform(-mutation_rate, mutation_rate)


class MainProgram:
    """
    Ana program, programcıkların çoğalmasını, istatistiksel analizleri, müdahale kabiliyetini
    ve test süreçlerini yönetir.

    Özellikler:
    - iterations: Simülasyonun kaç kez çalıştırılacağı.
    - num_programlets: Başlangıçta yaratılacak programlet sayısı.
    - mutation_rate: Mutasyon oranı. Programletlerin fitness değerlerindeki değişimin büyüklüğü.
    - target_fitness: Hedeflenen fitness değeri.
    """

    def __init__(self, iterations, num_programlets, mutation_rate, target_fitness):
        """
        Yeni bir ana program oluşturur.

        Args:
            iterations (int): Simülasyonun kaç kez çalıştırılacağı.
            num_programlets (int): Başlangıçta yaratılacak programlet sayısı.
            mutation_rate (float): Mutasyon oranı. Programletlerin fitness değerlerindeki değişimin büyüklüğü.
            target_fitness (float): Hedeflenen fitness değeri.
        """
        self.iterations = iterations
        self.num_programlets = num_programlets
        self.mutation_rate = mutation_rate  # Başlangıç mutasyon oranı
        self.target_fitness = target_fitness  # Hedef fitness değeri

    def start_simulation(self):
        """
        Programın ana simülasyonunu başlatır.

        Returns:
            tuple: (fitness_history, mutation_rates) tuple'ı.
            fitness_history: her iterasyonda ortalama fitness değerlerinin listesi,
            mutation_rates: her iterasyonda mutasyon oranlarının listesi.
        """
        # Başlangıçta rastgele programletler oluşturulur
        programlets = [Programlet(random.random()) for _ in range(self.num_programlets)]
        fitness_history = []  # Fitness geçmişi için boş bir liste oluşturulur
        mutation_rates = []  # Mutasyon oranları geçmişi için boş bir liste oluşturulur

        # Ana simülasyon döngüsü başlar
        for i in range(self.iterations):
            new_programlets = []  # Her iterasyonda oluşturulan yeni programletler için boş bir liste oluşturulur
            # Her bir programlet için çiftleşme işlemi yapılır
            for j in range(self.num_programlets):
                partner_index = random.randint(
                    0, self.num_programlets - 1
                )  # Rastgele bir partner seçilir
                if j != partner_index:  # Aynı programletle çiftleşme yapılmaz
                    # Seçilen iki programletin fitness değerlerinin ortalaması alınarak yeni bir programlet oluşturulur
                    avg_fitness = (
                        programlets[j].fitness + programlets[partner_index].fitness
                    ) / 2
                    new_programlet = Programlet(avg_fitness)
                    # Yeni programlet mutasyona uğratılır
                    new_programlet.mutate(self.mutation_rate)
                    new_programlets.append(
                        new_programlet
                    )  # Oluşturulan yeni programlet listeye eklenir

            # Yeni programletler populasyona eklenir
            programlets.extend(new_programlets)
            # Populasyon sıralanır ve en iyi programletler seçilir
            programlets.sort(key=lambda x: x.fitness, reverse=True)
            programlets = programlets[: self.num_programlets]

            # Fitness geçmişine ortalama fitness değeri eklenir
            avg_fitness = np.mean([p.fitness for p in programlets])
            fitness_history.append(avg_fitness)

            # Mutasyon oranları geçmişine mevcut mutasyon oranı eklenir
            mutation_rates.append(self.mutation_rate)

            # Mutasyon oranı güncellenir
            self.update_mutation_rate(avg_fitness)

        return fitness_history, mutation_rates

    def update_mutation_rate(self, avg_fitness):
        """
        Ortalama fitness değerine göre mutasyon oranını günceller.

        Args:
            avg_fitness (float): Ortalama fitness değeri.
        """
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
        """
        Test sürecini başlatır.

        Returns:
            list: Her iterasyonda ortalama fitness değerlerinin listesi.
        """
        programlets = [Programlet(random.random()) for _ in range(self.num_programlets)]
        fitness_history = []

        # Rasgele bir test senaryosu oluştur
        test_scenario = [random.uniform(0, 1) for _ in range(self.num_programlets)]

        for _ in range(self.iterations):  # Her bir test için belirli bir yapıyı uygula
            for i in range(self.num_programlets):
                programlets[i].fitness *= test_scenario[i]

            # Fitness geçmişine değer ekleme
            avg_fitness = np.mean([p.fitness for p in programlets])
            fitness_history.append(avg_fitness)

        return fitness_history


if __name__ == "__main__":
    iterations = 50
    num_programlets = 20
    mutation_rate = 0.1  # Başlangıç mutasyon oranı
    target_fitness = 1.0  # Hedef fitness değeri
    main = MainProgram(iterations, num_programlets, mutation_rate, target_fitness)
    test_fitness_history = main.start_test()
    main_fitness_history = main.start_simulation()
    print("test_fitness_history", test_fitness_history)
    print("main_fitness_history", main_fitness_history)
