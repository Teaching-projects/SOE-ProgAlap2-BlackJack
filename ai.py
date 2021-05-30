from black_jack import Player
import json

class AI(Player):
    """    
    >>> ai = AI(1000, 'hi-lo', True)
    >>> ai._count(4)
    >>> ai._card_counting_count
    1.0
    >>> ai._reset_count()
    >>> ai._system('omega_ii')
    >>> ai._count(10)
    >>> ai._card_counting_count
    -2.0
    >>> ai._count(3)
    >>> ai._card_counting_count
    -1.0
    >>> ai._reset_count()
    >>> ai._system('halves')
    >>> ai._count(2)
    >>> ai._card_counting_count
    0.5
    >>> ai.hand.add_card(('♥', '3', 3))
    >>> ai.hand.add_card(('♣', '3', 3))
    >>> ai.get_move(('♣', '7', 7))
    'sp'
    >>> ai.hand.reset()
    >>> ai.hand.add_card(('♣', 'A', 11))
    >>> ai.hand.add_card(('♣', '8', 8))
    >>> ai.get_move(('♣', '2', 2))
    's'
    >>> ai.hand.reset()
    >>> ai.hand.add_card(('♥', 'A', 11))
    >>> ai.hand.add_card(('♠', '4', 4))
    >>> ai.hand.add_card(('♦', '2', 2))
    >>> ai.hand.add_card(('♣', '5', 5))
    >>> ai.get_move(('♣', '7', 7))
    'h'
    >>> ai.hand.reset()
    >>> ai.hand.add_card(('♦', '10', 10))
    >>> ai.hand.add_card(('♣', '10', 10))
    >>> ai.get_move(('♣', '8', 8))
    's'
    """
    def __init__(self, chips: int, system:str, basic_strategy_mode:bool) -> None:
        super().__init__(chips)
        self._card_counting_count = 0
        self._basic_strategy_mode = basic_strategy_mode
        self._bet_calculator_system = system
        self._basic_strategy() if basic_strategy_mode else self._stupid_strategy()
        self._stupid_bet_calculator() if system == 'random' else self._system(system)

    def _stupid_bet_calculator(self) -> int:
        """Ez az AI nem érti a játékot és teljesen véletlenszerűen választja ki a tét méretét."""
        pass

    def _system(self, system_name:str) -> None:
        """Betölti a megadott lapszámlálási technikát.
        
        Args:
            system_name (str): A kiválasztott kártyaszámolási technika neve.
        """
        with open(f'basic_data/{system_name}.json') as f:
            self._card_counting_system = json.load(f)

    def _reset_count(self) -> None: 
        """Alaphelyzetbe állítja a számlálót."""
        self._card_counting_count = 0

    def _count(self, card:int) -> None:
        """A megadott kártya alapján változatatja a számláló értékét.
        
        Args:
            card (int): Kártya értéke.
        """
        for count_value in list(self._card_counting_system.keys()): 
            if card in self._card_counting_system[count_value]: self._card_counting_count += float(count_value)

    def _calculate_bet_with_card_counting_system(self) -> int: 
        pass
    
    def _stupid_strategy(self) -> str:
        """Ez az AI nem érti a játékot és teljesen véletlenszerűen hoz döntéseket."""
        pass

    def _basic_strategy(self) -> None:
        """Betölti a kiválasztott stratégiát, majd eltárolja azt."""
        with open(f'basic_data/basic_strategy.json') as f:
            self._strategy = json.load(f)

    def _search_move(self, hand_type:str, player:int, dealer:int):
        """A stratégiának megfelelő döntést keresi meg, a megadott kéz és kártya értékek alapján.
        
        Args:
            hand_type (str): A kiválasztott kártyaszámolási technika neve.
            player (int): A stratégiának megfelelő érték, ami a játékoshoz tartozik.
            dealer (int): Az osztó első lapja.

        Returns:
            str: A döntés rövidítve (h=hit, s=stand, d=double down, sp=split).
        """
        row = 0
        column = 0
        strategy = self._strategy[hand_type]
        for index, card in enumerate(strategy['player']):
            if player == card: row = index
        for index, card in enumerate(strategy['dealer']):
            if dealer == card: column = index
        return strategy['move'][row][column]

    def _calculate_move_with_basic_strategy(self, dealer_card:tuple) -> str:
        """A stratégiának megfelelő döntést hozza meg a játékos keze alapján.
        
        Args:
            dealer_card (int): Az osztó első lapja.

        Returns:
            str: A döntés rövidítve (h=hit, s=stand, d=double down, sp=split).
        """
        if self.hand.pair(): return self._search_move('pair_splitting', self.hand.get_card_values()[0], dealer_card[2])
        elif self.hand.soft_hand(): return self._search_move('soft_hand', self.hand.get_score()-11, dealer_card[2])
        else: return self._search_move('hard_hand', self.hand.get_score(), dealer_card[2])
        
    def get_bet(self) -> int:
        """A játékos tétjének a meghatározását végzi el.
        
        Returns:
            int: A játékos tétjének a nagysága.
        """
        return self._stupid_bet_calculator() if self._bet_calculator_system == 'random' else self._calculate_bet_with_card_counting_system()

    def get_move(self, dealer_card:tuple) -> str:
        """A játékos döntését adja meg.
        
        Args:
            dealer_card (int): Az osztó első lapja.

        Returns:
            str: A döntés rövidítve (h=hit, s=stand, d=double down, sp=split).
        """
        return self._calculate_move_with_basic_strategy(dealer_card) if self._basic_strategy_mode else self._stupid_strategy()

if __name__ == '__main__': 
    import doctest
    doctest.testmod()