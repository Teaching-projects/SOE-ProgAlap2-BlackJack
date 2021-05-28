from black_jack import Player
import json

class AI(Player):
    def __init__(self, chips: int) -> None:
        super().__init__(chips)
        self._card_counting_system = None
        self._card_counting_count = 0

    def stupid_ai(self) -> None:
        """Ez az ai nem érti a játékot és teljesen véletlenszerűen hoz döntéseket."""
        pass

    def hi_lo_system(self) -> None:
        with open('basic_data/hi-lo_system.json') as f:
            self._cardcounting_system = json.load(f)

if __name__ == '__main__': pass