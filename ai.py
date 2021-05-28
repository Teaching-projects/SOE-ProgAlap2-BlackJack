from black_jack import Player
import json

class AI(Player):
    """
    >>> ai = AI(1000)
    >>> ai.system('hi-lo')
    >>> ai.count(4)
    >>> ai._card_counting_count
    1.0
    >>> ai.reset_count()
    >>> ai.system('omega_ii')
    >>> ai.count(10)
    >>> ai._card_counting_count
    -2.0
    >>> ai.count(3)
    >>> ai._card_counting_count
    -1.0
    >>> ai.reset_count()
    >>> ai.system('halves')
    >>> ai.count(2)
    >>> ai._card_counting_count
    0.5
    """
    def __init__(self, chips: int) -> None:
        super().__init__(chips)
        self._card_counting_system = None
        self._card_counting_count = 0

    def stupid_ai(self) -> None:
        """Ez az AI nem érti a játékot és teljesen véletlenszerűen hoz döntéseket."""
        pass

    def system(self, system_name:str) -> None:
        """Betölti a megadott lapszámlálási technikát."""
        with open(f'basic_data/{system_name}.json') as f:
            self._card_counting_system = json.load(f)

    def reset_count(self) -> None: 
        """Alaphelyzetbe állítja a számlálót."""
        self._card_counting_count = 0

    def count(self, card:int) -> None:
        """A megadott kártya alapján változatatja a számláló értékét."""
        for count_value in list(self._card_counting_system.keys()): 
            if card in self._card_counting_system[count_value]: self._card_counting_count += float(count_value)

if __name__ == '__main__': 
    import doctest
    doctest.testmod()