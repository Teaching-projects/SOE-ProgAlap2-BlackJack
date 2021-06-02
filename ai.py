from blackjack import Player_hand, Player
import json

class Card_counter:
    """
    >>> c = Card_counter('hi-lo')
    >>> c.count(4)
    >>> c._count
    1.0
    >>> c.reset_count()
    >>> c = Card_counter('omega_ii')
    >>> c.count(10)
    >>> c._count
    -2.0
    >>> c.count(3)
    >>> c._count
    -1.0
    >>> c.reset_count()
    >>> c = Card_counter('halves')
    >>> c.count(2)
    >>> c._count
    0.5
    """
    def __init__(self, system) -> None:
        """Betölti a megadott lapszámlálási technikát, majd eltárolja azt. Illetve létrehoz egy számlálót.

        Args:
            system (str): A kiválasztott kártyaszámolási technika neve.
        """
        self._count = 0
        with open(f'basic_data/{system}.json') as f:
            self._system = json.load(f)

    def reset_count(self) -> None: 
        """Alaphelyzetbe állítja a számlálót."""
        self._count = 0

    def count(self, card:int) -> None:
        """A megadott kártya alapján változatatja a számláló értékét.
        
        Args:
            card (int): Kártya értéke.
        """
        for count_value in list(self._system.keys()): 
            if card in self._system[count_value]: self._count += float(count_value)

    def calculate_bet(self): pass

class Strategy:
    """
    >>> s = Strategy()
    >>> h = Player_hand()
    >>> h.add_card(('♥', '3', 3))
    >>> h.add_card(('♣', '3', 3))
    >>> s.calculate_move(h,('♣', '7', 7))
    'sp'
    >>> h = Player_hand()
    >>> h.add_card(('♣', 'A', 11))
    >>> h.add_card(('♣', '8', 8))
    >>> s.calculate_move(h,('♣', '2', 2))
    's'
    >>> h = Player_hand()
    >>> h.add_card(('♥', 'A', 11))
    >>> h.add_card(('♠', '4', 4))
    >>> h.add_card(('♦', '2', 2))
    >>> h.add_card(('♣', '5', 5))
    >>> s.calculate_move(h,('♣', '7', 7))
    'h'
    >>> h = Player_hand()
    >>> h.add_card(('♦', '10', 10))
    >>> h.add_card(('♣', '10', 10))
    >>> s.calculate_move(h,('♣', '8', 8))
    's'
    >>> h = Player_hand()
    >>> h.add_card(('♠', '6', 6))
    >>> h.add_card(('♠', '10', 10))
    >>> h.get_score()
    16
    >>> s.calculate_move(h,('♦', '4', 4))
    's'
    """
    def __init__(self) -> None:
        """Betölti a kiválasztott stratégiát, majd eltárolja azt."""
        with open(f'basic_data/basic_strategy.json') as f:
            self._strategy = json.load(f)
    
    def _search_move(self, hand_type:str, player:int, dealer:int) -> str:
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

    def calculate_move(self, player_hand:Player_hand, dealer_card:tuple) -> str:
        """A stratégiának megfelelő döntést hozza meg a játékos keze alapján.
        
        Args:
            player_hand (Player_hand): A játékos keze.
            dealer_card (int): Az osztó első lapja.

        Returns:
            str: A döntés rövidítve (h=hit, s=stand, d=double down, sp=split).
        """
        if player_hand.pair(): return self._search_move('pair_splitting', player_hand.get_card_values()[0], dealer_card[2])
        elif player_hand.in_ace() and player_hand.soft(): return self._search_move('soft_hand', player_hand.get_score()-11, dealer_card[2])
        else: return self._search_move('hard_hand', player_hand.get_score(), dealer_card[2])

class AI(Player):
    def __init__(self, chips: int, system:str, basic_strategy_mode:bool) -> None:
        """A döntéseket és a tét nagyságát fogja eldönteni a megadott paraméterek alapján.

        Args:
            chips (int): Zseton, amivel játszik a játékos.
            system (str): Ha a szimulációban lesz lapszámolási technika, akkor annak a neve, ha nem, akkor ennek az értéke 'random', vagyis véletlenszerűen lesz kiválasztva a tét.
            basic_strategyi (bool): Azt adja meg, hogy a szimuláció használja-e a basic strategy nevezetű stratégiát.
        """
        super().__init__(chips)
        self._basic_strategy_ = basic_strategy_mode
        self._card_counter = system != 'random'
        self._strategy = Strategy() if basic_strategy_mode else self._stupid_strategy()
        self._counter = Card_counter(system) if self._card_counter else self._stupid_bet_calculator()

    def _stupid_bet_calculator(self) -> int:
        """Ez az AI nem érti a játékot és teljesen véletlenszerűen választja ki a tét méretét."""
        pass
    
    def _stupid_strategy(self) -> str:
        """Ez az AI nem érti a játékot és teljesen véletlenszerűen hoz döntéseket."""
        pass
        
    def get_bet(self) -> int:
        """A játékos tétjének a meghatározását végzi el.
        
        Returns:
            int: A játékos tétjének a nagysága.
        """
        return self._counter.calculate_bet() if self._card_counter else self._stupid_bet_calculator()

    def get_move(self, player_hand:Player_hand, dealer_card:tuple) -> str:
        """A játékos döntését adja meg.
        
        Args:
            player_hand (Player_hand): A játékos keze.
            dealer_card (int): Az osztó első lapja.

        Returns:
            str: A döntés rövidítve (h=hit, s=stand, d=double down, sp=split).
        """
        return self._strategy.calculate_move(player_hand, dealer_card) if self._basic_strategy_ else self._stupid_strategy()

if __name__ == '__main__': 
    import doctest
    doctest.testmod()
