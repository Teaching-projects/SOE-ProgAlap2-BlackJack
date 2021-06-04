from blackjack_logic import Game, Player_hand, Player
from random import randint, choice
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

    def calculate_bet(self): return 30

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
    >>> h = Player_hand()
    >>> h.add_card(('♥', '4', 4))
    >>> h.add_card(('♠', '4', 4))
    >>> s.calculate_move(h,('♦', 'Q', 10))
    'h'
    >>> h.add_card(('♠', '9', 9))
    >>> s.calculate_move(h,('♦', 'Q', 10))
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
        """A stratégiának megfelelő döntést hozza meg a játékos keze alapján. Figyelembe véve azt, hogy egyzser lehet splitelni és ha a kéz splitelve van akkor nem lehet duplázni.
        
        Args:
            player_hand (Player_hand): A játékos keze.
            dealer_card (int): Az osztó első lapja.

        Returns:
            str: A döntés rövidítve (h=hit, s=stand, d=double down, sp=split).
        """
        moves = player_hand.get_moves()
        if 'sp' in moves: 
            return self._search_move('pair_splitting', player_hand.get_card_values()[0], dealer_card[2])
        elif player_hand.is_in_ace() and player_hand.is_soft(): 
            move = self._search_move('soft_hand', player_hand.get_score()-11, dealer_card[2])
            return 'h' if move == 'd' and 'd' not in moves else move
        else: 
            move = self._search_move('hard_hand', player_hand.get_score(), dealer_card[2])
            return 'h' if move == 'd' and 'd' not in moves else move

class AI(Player):
    def __init__(self, chips: int) -> None:
        """A döntéseket és a tét nagyságát fogja eldönteni a megadott paraméterek alapján.

        Args:
            chips (int): Zseton, amivel játszik a játékos.
        """
        super().__init__(chips)
        self._is_basic_strategy = False
        self._is_card_counter = False

    def set_basic_strategy(self) -> None:
        """Beállítja az alapstratégiát."""
        self._is_basic_strategy = True 
        self._strategy = Strategy()

    def set_card_counter(self, system:str) -> None:
        """Beállítja a megadott lapszámolási technikát.

        Args:
            system (str): A lapszámolási technika neve.
        """
        self._is_card_counter = True
        self._card_counter = Card_counter(system)

    def _stupid_bet_calculator(self, min_bet:int, max_bet:int) -> int:
        """Ez az AI nem érti a játékot és teljesen véletlenszerűen választja ki a tét méretét."""
        return randint(min_bet, max_bet)
    
    def _stupid_strategy(self, hand:Player_hand) -> str:
        """Ez az AI nem érti a játékot és teljesen véletlenszerűen hoz döntéseket."""
        return choice(hand.get_moves())
        
    def get_bet(self, min_bet:int, max_bet:int) -> int:
        """A játékos tétjének a meghatározását végzi el.
        
        Returns:
            int: A játékos tétjének a nagysága.
        """
        return self._card_counter.calculate_bet() if self._is_card_counter else self._stupid_bet_calculator(min_bet, max_bet)

    def get_move(self, player_hand:Player_hand, dealer_card:tuple) -> str:
        """A játékos döntését adja meg.
        
        Args:
            player_hand (Player_hand): A játékos keze.
            dealer_card (int): Az osztó első lapja.

        Returns:
            str: A döntés rövidítve (h=hit, s=stand, d=double down, sp=split).
        """
        return self._strategy.calculate_move(player_hand, dealer_card) if self._is_basic_strategy else self._stupid_strategy(player_hand)

    def view_game_status(self): pass

class Game_simulation(Game):
    def __init__(self, min_bet: int, max_bet: int, deck_count: int) -> None:
        super().__init__(min_bet, max_bet, deck_count)

if __name__ == '__main__': 
    import doctest
    doctest.testmod()
