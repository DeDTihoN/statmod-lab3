import random


class CoinGame:
    def __init__(self, players, rounds, win_combo):
        """
        Ініціалізація гри.
        :param players: Кількість гравців.
        :param rounds: Кількість підкидань монети.
        :param win_combo: Комбінація для виграшу.
        """
        self.players = players
        self.rounds = rounds
        self.win_combo = win_combo

    def toss_coin(self):
        """Імітує підкидання монети."""
        return random.choice(["Орел", "Решка"])

    def play(self):
        """Моделює гру і підраховує виграш для кожного гравця."""
        results = {player: 0 for player in range(1, self.players + 1)}
        costs = {player: 0 for player in range(1, self.players + 1)}

        for player in range(1, self.players + 1):
            previous_toss = None
            for _ in range(self.rounds):
                costs[player] += 1
                current_toss = self.toss_coin()
                if previous_toss == self.win_combo[0] and current_toss == self.win_combo[1]:
                    results[player] += 5
                previous_toss = current_toss

        return results, costs


def main():
    players = int(input("Введіть кількість гравців: "))
    rounds = int(input("Введіть кількість підкидань монети: "))

    # Правило 1: Орел - Решка
    print("\nГра за правилом 1: Орел - Решка")
    game1 = CoinGame(players, rounds, win_combo=["Орел", "Решка"])
    results1, costs1 = game1.play()
    for player in range(1, players + 1):
        print(f"Гравець {player}: виграш {results1[player]} доларів, витрати {costs1[player]} доларів.")

    # Правило 2: Орел - Орел
    print("\nГра за правилом 2: Орел - Орел")
    game2 = CoinGame(players, rounds, win_combo=["Орел", "Орел"])
    results2, costs2 = game2.play()
    for player in range(1, players + 1):
        print(f"Гравець {player}: виграш {results2[player]} доларів, витрати {costs2[player]} доларів.")


if __name__ == "__main__":
    main()
