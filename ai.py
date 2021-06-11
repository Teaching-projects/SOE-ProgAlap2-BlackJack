from blackjack_logic import Game, Player_hand, Player
from random import randint, choice
import json


class Card_counter:
    """
    >>> c = Card_counter('Hi-Lo', 1)
    >>> c._counting(4)
    >>> c._count
    1.0
    >>> c = Card_counter('Omega II', 1)
    >>> c._counting(10)
    >>> c._count
    -2.0
    >>> c._counting(3)
    >>> c._count
    -1.0
    >>> c = Card_counter('Halves', 3)
    >>> c._counting(2)
    >>> c._count
    0.5
    >>> c._reset_count()
    >>> c._counting(10)
    >>> c._counting(9)
    >>> c._count
    -1.5
    >>> c.running_count([10, 5, 2, 3, 8, 7, 5])
    >>> c._count
    2.5
    >>> c._remaining_cards
    147
    >>> c._calculate_decks_remaining()
    2
    >>> c._calculate_true_count()
    1.25
    >>> c.calculate_bet(100, 3000)
    100
    >>> c._counting(5)
    >>> c._calculate_true_count()
    2.0
    >>> c.calculate_bet(100, 3000)
    100
    >>> c._counting(4)
    >>> c._calculate_true_count()
    2.5
    >>> c.calculate_bet(100, 3000)
    150
    >>> c.calculate_bet(100, 120)
    120
    """

    def __init__(self, system: str, decks: int) -> None:
        """Betölti a megadott lapszámlálási technikát, majd eltárolja azt.

        Args:
            system (str): A kiválasztott kártyaszámolási technika neve.
            decks (int): A paklik száma.
        """
        self._decks = decks
        self._reset_count()
        with open(f'data/counting_systems.json') as f:
            self._system = json.load(f)[system]

    def _reset_count(self) -> None:
        """Alaphelyzetbe állítja a számlálót."""
        self._count = 0
        self._remaining_cards = self._decks * 52

    def _counting(self, card_value: int) -> None:
        """A megadott kártya alapján változatatja a számláló értékét. Ha elfogyott a kártya, akkor ugye újra lesz keverve pakli és ilyenkor nullára állítja a számlálót.

        Args:
            card_value (int): Kártya értéke.
        """
        for count_value in list(self._system.keys()):
            if card_value in self._system[count_value]:
                self._count += float(count_value)
        self._remaining_cards -= 1
        if self._remaining_cards == 0:
            self._reset_count()

    def running_count(self, cards: list) -> None:
        """A lapszámolási technika alapján végigmegy a megadott kártyaértékeken.

        Args:
            card (list): A kártya értékek listája.
        """
        for card in cards:
            self._counting(card)

    def _calculate_decks_remaining(self) -> int:
        """Kiszámolja, hogy hány pakli van még hátra a következő keverésig.

        Returns:
            int: A hátralévő paklik száma.
        """
        return self._remaining_cards // 52

    def _calculate_true_count(self) -> int:
        """Kiszámolja a valódi értéket. Ha több paklival játszanak, akkor a számláló értékét el kell osztani a hátralévő paklik számával.

        Returns:
            int: A valódi érték.
        """
        decks_remaining = self._calculate_decks_remaining()
        if decks_remaining == 0:
            return self._count
        return self._count / decks_remaining

    def calculate_bet(self, min_bet: int, max_bet: int) -> int:
        """Kiszámolja az optimális tétet a valódi érték alapján.

        Args:
            min_bet (int): Minimum tét.
            max_bet (int): Maximum tét.

        Returns:
            int: Az optimális tét.
        """
        bet = (self._calculate_true_count() - 1) * min_bet
        if bet < min_bet:
            return min_bet
        elif bet > max_bet:
            return max_bet
        return round(bet)


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
        with open(f'data/basic_strategy.json') as f:
            self._strategy = json.load(f)

    def _search_move(self, hand_type: str, player: int, dealer: int) -> str:
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
            if player == card:
                row = index
        for index, card in enumerate(strategy['dealer']):
            if dealer == card:
                column = index
        return strategy['move'][row][column]

    def calculate_move(self, player_hand: Player_hand, dealer_card: tuple) -> str:
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
            move = self._search_move(
                'soft_hand', player_hand.get_score()-11, dealer_card[2])
            return 'h' if move == 'd' and 'd' not in moves else move
        else:
            move = self._search_move(
                'hard_hand', player_hand.get_score(), dealer_card[2])
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

    def set_card_counter(self, system: str, decks: int) -> None:
        """Beállítja a megadott lapszámolási technikát.

        Args:
            system (str): A lapszámolási technika neve.
            decks (int): A paklik száma.
        """
        self._is_card_counter = True
        self._card_counter = Card_counter(system, decks)

    def _stupid_bet_calculator(self, min_bet: int, max_bet: int) -> int:
        """Ez az AI nem érti a játékot és teljesen véletlenszerűen választja ki a tét méretét."""
        return randint(min_bet, max_bet)

    def _stupid_strategy(self, hand: Player_hand) -> str:
        """Ez az AI nem érti a játékot és teljesen véletlenszerűen hoz döntéseket."""
        return choice(hand.get_moves())

    def get_bet(self, min_bet: int, max_bet: int) -> int:
        """A játékos tétjének a meghatározását végzi el.

        Args:
            min_bet (int): Minimum tét.
            max_bet (int): Maximum tét.

        Returns:
            int: A játékos tétjének a nagysága.
        """
        return self._card_counter.calculate_bet(min_bet, max_bet) if self._is_card_counter else self._stupid_bet_calculator(min_bet, max_bet)

    def get_move(self, player_hand: Player_hand, dealer_card: tuple) -> str:
        """A játékos döntését adja meg.

        Args:
            player_hand (Player_hand): A játékos keze.
            dealer_card (int): Az osztó első lapja.

        Returns:
            str: A döntés rövidítve (h=hit, s=stand, d=double down, sp=split).
        """
        return self._strategy.calculate_move(player_hand, dealer_card) if self._is_basic_strategy else self._stupid_strategy(player_hand)

    def view_cards_on_the_table(self, cards: list) -> None:
        """Végignézi a kártya értékekeet, azaz megszámolja azokat.

        Args:
            cards (list): A kártya értékek listája.
        """
        self._card_counter.running_count(cards)


class Game_simulation(Game):
    """A szimuláció szsámára definiált Game osztály. A kártyaszámolást is "támogatja". """

    def __init__(self, player: Player, min_bet: int, max_bet: int, deck_count: int) -> None:
        """
        Args:
            player (Player): A megadott játékos, aki játszani fog.
            min_bet (int): Minimum tét.
            max_bet (int): Maximum tét.
            deck_count (int): A paklik száma.
        """
        super().__init__(player, min_bet, max_bet, deck_count)

    def get_cards_on_the_table(self) -> list:
        """Visszaadja az asztalon lévő kártyák értékeit.

        Returns:
            list: A kártya értékek listája.
        """
        cards = self._dealer.hand.get_card_values()
        cards.extend(self._player.main_hand.get_card_values())
        if self._player.main_hand.is_split_hand:
            cards.extend(self._player.split_hand.get_card_values())
        return cards


if __name__ == '__main__':
    import doctest
    doctest.testmod()
