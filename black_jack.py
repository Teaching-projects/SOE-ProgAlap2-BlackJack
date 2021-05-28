import json
from random import shuffle

class Card:
    """
    >>> c1 = Card('♥', '7', 7)
    >>> c1.get_value()
    7
    >>> c2 = Card('♠', 'K', 10)
    >>> c2.get_value()
    10
    """
    def __init__(self, suit:str, name:str, value:int) -> None:
        """Egy egyszerű francia kártya tulajdonságait definiáló osztály.

        Args:
            suit (str): A kártya színe.
            name (str): A kártya neve.
            value (int): A kártya értéke
        """
        self.suit = suit
        self.name = name
        self._value = value

    def get_value(self):
        return self._value

class Deck: 
    def __init__(self, deck_count:int) -> None:
        """Egy francia kártya paklit definiáló osztály.

        Args:
            deck_count (int): A paklik száma.
        """
        self._deck = []
        self._deck_count = deck_count
        self._deck_init()

    def _deck_init(self) -> None:
        """Összekever annyi paklit amennyit megadtunk."""
        for i in range(self.deck_count): self._deck.extend(self._make_a_deck())
        self.shuffle()

    def _make_a_deck(self) -> list:
        """Egy 52 lapos paklit hoz létre."""
        deck = []
        with open('basic_data/cards.json') as f:
            data = json.load(f)
        for suit in data['suits']:
            for name in data['values'].keys(): deck.append(Card(suit, name, data['values'][name]))
        return deck
        
    def shuffle(self) -> None:
        """Megkeveri a paklit."""
        shuffle(self._deck)

    def _get_a_card(self) -> Card:
        """Kivesz egy kártyát a pakliból."""
        card = self._deck[0]
        self._deck.pop(0)
        return card

    def deal_card(self) -> None:
        """Ha a elfogyott a pakli akkor újra keveri a kiment kártyákat és abból vesz egyet,
        ha van még kártya, akkor onnan vesz el."""
        if len(self._deck) == 0: 
            self._deck_init()
            self._get_a_card()
        else: self._get_a_card()

class Hand:
    """
    >>> h = Hand()
    >>> h.add_card(Card('♥', 'Q', 10))
    >>> h.add_card(Card('♥', '4', 4))
    >>> h.get_score()
    14
    >>> h.add_card(Card('♣', '2', 2))
    >>> h.get_score()
    16
    >>> h.blackjack()
    False
    >>> h.bust()
    False
    >>> h.reset()
    >>> h.add_card(Card('♥', 'J', 10))
    >>> h.add_card(Card('♣', 'A', 11))
    >>> h.blackjack()
    True
    >>> h.get_score()
    21
    >>> h.add_card(Card('♦', '2', 2))
    >>> h.get_score()
    21
    >>> h.reset()
    >>> h.add_card(Card('♣', 'K', 10))
    >>> h.add_card(Card('♦', '9', 9))
    >>> h.add_card(Card('♦', 'A', 11))
    >>> h.get_score()
    20
    >>> h.add_card(Card('♥', '3', 3))
    >>> h.get_score()
    23
    >>> h.bust()
    True
    """
    def __init__(self) -> None:
        """A kézben lévő kártyákat definiálja."""
        self.reset()
    
    def reset(self) -> None:
        """Alaphelyzetbe állítja az osztályt"""
        self._cards = []
        self._score = 0

    def _ace_value(self, card_values:list) -> None: 
        """Az ász értéke lehet 1 vagy 11. akkor tekintendő az Ász értéke 1-nek,
        ha a lapok összértéke az Ász 11-es értékével számolva meghaladná a 21-et.
        
        Args:
            card_values (list): A kártyák értékei.
        """
        if self.bust() and 11 in card_values: self._score -= 10

    def _sum_score(self) -> None:
        """Összeadja a kézben lévő kártyák értékét, figyelembe véve az előnyösebb ász értéket."""
        card_values = [card.get_value() for card in self._cards]
        self._score = sum(card_values)
        self._ace_value(card_values)

    def add_card(self, card:Card) -> None:
        """Felvesz egy kártyát a kézbe, ha a kezében lévő érték kisebb, mint 21.

        Args:
            card (Card): Egy kártya, ami a kézbe kerül.
        """
        if self._score < 21: self._cards.append(card)
        self._sum_score()

    def blackjack(self) -> bool:
        """Megnézi, hogy a kéz értéke 21-e.

        Returns: 
            bool: Ha 21 a kézben lévő első két kártya értéke, akkor Blackjack van és True-val tér vissza,
            különben meg False értékkel.
        """
        return self._score == 21 and len(self._cards) == 2

    def bust(self) -> bool:
        """Ha a lapok értéke meghaladja a 21-et"""
        return self._score > 21

    def get_score(self) -> int:
        """A kézben lévő érték.

        Returns: 
            int: A kézben lévő kártyák értékének az összegével tér vissza.
        """
        return self._score

class Player:
    def __init__(self, chips:int) -> None:
        self._chips = chips
        self._bet = None
        self._hand = Hand()

    def place_bet(self, bet:int) -> int:
        """A játékos megadja a tétet.
        
        Returns:
            int: A tét, amivel a játékos játszik."""
        self._chips -= bet
        return bet

    def hit(self, card:Card): 
        """A játékos tetszőleges számú lapot kérhet mindaddig, amíg a lapjainak összértéke meg nem haladja a 21-et."""
        self._hand.add_card(card)

    def stand(self): 
        """A játékos ekkor nem kér több lapot, mert úgy ítéli meg, hogy megfelelő lapjai vannak a játék megnyerésére."""
        pass

    def double(self): 
        """Ha a játékos úgy ítéli meg, hogy az első két lapja elég erős ahhoz,
        hogy egy harmadik lappal megnyerje a játékot, akkor a Double bemondásával a tétet duplázza.
        A játékos a Double bemondása után már csak egy lapot kap, további lapot nem kérhet."""
        pass

    def split(self):
        """Ha a játékos első két lapja egy párt alkot (például 5–5 vagy Q–Q), akkor ezt kettéoszthatja,
        ezzel két „kezet” hoz létre, valamint mindkettőre azonos tétet tehet meg, azaz a tét duplázódik.
        Mindkét lapra külön leosztás szerint kérhet lapot."""
        pass

class Game:
    def __init__(self, rounds:int, chips:int, min_bet:int, max_bet:int, deck_count:int) -> None:
        self._deck = Deck(deck_count)
        self._dealer_hand = Hand()
        self._dealer_score = 0
        self._player = None

    def check_game(self): pass

    def setup(self) -> None:
        self._player.hit(self._deck.deal_card())
        self._dealer_hand(self._deck.deal_card())
        self._player.hit(self._deck.deal_card())
    
    def round(self) -> None:
        self.setup()

if __name__ == '__main__':
    import doctest
    doctest.testmod()